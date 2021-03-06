from collections import deque
from copy import deepcopy
from em_functionalities import *
from abstract_helpers import Problem, Node, solution
from treelib import Tree
from enum import Enum

class SearchType(Enum):
    VALIDATION = 0
    PLANNING = 1

class EM_Search_Problem(Problem):

    def __init__(self, search_type, state_file="initial_state.json", scene_file="scenes.json", 
            plot_file="plot.json", players_file="players_data.json", init_state=None):

        self.viewed_scenes = []
        self.deadends = []
        self.search_type = search_type

        if init_state is None:
            self.init_state = get_initial_gamestate(state_file, scene_file, 
            plot_file, players_file)
            roles = list(self.init_state.players_data['characters'].keys())
            for i in range(2):
                self.init_state.players[i].set_role(roles[i])
                scene = get_first_scene(i, self.init_state)
                self.viewed_scenes.append(scene[1])
        else:
            self.init_state = deepcopy(init_state)

    def actions(self, state):
        def get_actions(player_id, state):
            actions = []
            next_menu = get_next_menu(scenes[player_id], state)
            if next_menu != 'None':
                for choice in next_menu[2]:
                    actions.append(('menu', [next_menu[0], next_menu[1], choice], player_id))
            else:
                next_scenes = []

                if self.search_type == SearchType.VALIDATION:
                    next_scenes.append(get_next_scene(player_id, state))
                elif self.search_type == SearchType.PLANNING:
                    next_scenes.extend([scene for scene in get_all_next_scenes(player_id, state) if type(scene) == tuple])
                
                for next_scene in next_scenes:
                    if next_scene[1] == 'wait_scene' or next_scene[1] == 'end_scene':
                        continue
                    actions.append(('scene', next_scene))
                    self.viewed_scenes.append(next_scene[1])
            return actions

        # actions are either scene transitions or player choices
        all_actions = []
        scenes = get_current_scenes(state)
        no_actions_found = []

        for i in range(2):
            copy_state = deepcopy(state)
            actions = get_actions(i, copy_state)

            if len(actions) == 0:
                no_actions_found.append((i, copy_state))
            else:
                all_actions.extend(actions)
                sample_action = actions[0]
                if sample_action[0] == 'scene' and len(sample_action[1][0]) > 1: 
                    # In case it's a multiplayer scene, it's the same action for both so break
                    break
                if sample_action[0] == 'menu' and scenes[0] == scenes[1]:
                    # In case we're in a multiplayer scene, menus are only considered once so break
                    break
        if len(all_actions) == 0:
            for no_action_state in no_actions_found:
                player_id = no_action_state[0]
                copy_state = no_action_state[1]
                actions = get_actions(1-player_id, copy_state)
                all_actions.extend(actions)
                if len(actions) > 0:
                    sample_action = actions[0]
                    if sample_action[0] == 'scene' and len(sample_action[1][0]) > 1: 
                        # In case it's a multiplayer scene, it's the same action for both so break
                        break
                    if sample_action[0] == 'menu' and scenes[0] == scenes[1]:
                        # In case we're in a multiplayer scene, menus are only considered once so break
                        break
        
#        print('actions', all_actions)
        return all_actions
    
    def result(self, state, action):
        if action[0] == 'menu':
            apply_choice_postconditions(action[1][0], action[1][1], action[1][2], state)
        elif action[0] == 'scene':
            apply_scene_postconditions(action[1][1], action[1][0], state)
        return state

    def goal_test(self, state):
        return all_players_ended(state)
    
    def step_cost(self, state, action):
        if action[0] == 'menu':
            return 0
        elif action[0] == 'scene':
            error = get_error(action[1][1], action[1][0][0], state)
            return error
        

class EM_Searcher:        
    
    def __init__(self, state_file="initial_state.json", scene_file="scenes.json",
                plot_file="plot.json", players_file="players_data.json"):
        self.solutions = []
        self.state_file = state_file
        self.scene_file = scene_file
        self.plot_file = plot_file
        self.players_file = players_file
    
    def dfs(self, problem):
        solutions = []
        frontier = deque([Node.root(problem.init_state)])
        while frontier:
            node = frontier.pop()
            actions = problem.actions(node.state)

            if len(actions) == 0:
                problem.deadends.append(solution(node))

            for action in actions:
                child = Node.child(problem, node, action)
                if action[0] == 'scene':
                    child.state.players[action[1][0][0]].increment_beat_count()
                    child.state.players[action[1][0][0]].add_scene(action[1][1])
                    if len(action[1][0]) == 2:
                        child.state.players[action[1][0][1]].increment_beat_count()
                        child.state.players[action[1][0][1]].add_scene(action[1][1])
                if problem.goal_test(child.state):
                    solutions.append(solution(child))
                else:
                    frontier.append(child)
        return solutions

    def validate(self, init_state=None):
        problem = EM_Search_Problem(SearchType.PLANNING, state_file=self.state_file, scene_file=self.scene_file,
                plot_file=self.plot_file, players_file=self.players_file, init_state=init_state)
        self.solutions = self.dfs(problem)

        unique_viewed_scenes = list(set(problem.viewed_scenes))
        unviewed_scenes = []
        for label in problem.init_state.scenes_list:
            if label not in unique_viewed_scenes:
                unviewed_scenes.append(label)

        if len(unviewed_scenes) == 0:
            print("There are no unreachable scenes\n")
        else:
            print("Unreachable scenes are", unviewed_scenes, '\n')

        if len(problem.deadends) == 0:
            print("No deadends detected!\n")
        else:
            print("The following scenarios lead to deadend:\n")
            for deadend in problem.deadends:
                print(deadend, '\n')
        
        return self.solutions
    
    def plan(self, init_state=None):
        problem = EM_Search_Problem(SearchType.PLANNING, init_state=init_state)
        self.solutions = self.dfs(problem)
        return self.solutions
    
    def visulaize_solutions(self):
        parents = []
        for sol in self.solutions:
            sol = sol[0]
            if sol[0] not in [p[0] for p in parents]:
                tree = Tree()
                tree.create_node(str(sol[0]), str(sol[0]))
                parents.append((sol[0], tree))
            else:
                tree = [p[1] for p in parents if p[0] == sol[0]][0]

            for i in range(1, len(sol)):
                try:
                 tree.create_node(str(sol[i]), str(sol[i]), parent=str(sol[i-1]))
                except:
                    continue

        for tree in parents:
            tree[1].show()