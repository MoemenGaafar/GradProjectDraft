from experience_manager import ExperienceManager

em = ExperienceManager(state_file = "initial_state.json", \
        scene_file = "scenes.json", plot_file = "plot.json", players_file= "players_data.json", choices_file='player_choices_sheet.csv')

em.set_player_role(0, 'Red')
em.set_player_role(1, 'Wolf')
print(em.get_first_scene(0))
print(em.get_first_scene(1))
em.apply_choice_postconditions("Red1", "Bird", "Give")
print(em.get_next_scene(0))
#print(em.validate_choices("Wolf1", "Bunny"))
#em.apply_choice_postconditions("Wolf1", "Bunny", "Ignore")
#em.apply_choice_postconditions("Red1", "Bird", "Ignore")
#print(em.get_next_scene(0))
#print(em.validate_choices("Red_Meets_Bunny", "Bunny"))
#em.apply_choice_postconditions("Red_Meets_Bunny", "Bunny", "Help")
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#print(em.validate_choices("Bunny_Calls_Hunter", "Hunter"))
#em.apply_choice_postconditions("Bunny_Calls_Hunter", "Hunter", "Ignore")
#
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#print(em.get_next_scene(0))
#
##print(em.get_next_scene(1))
##print(em.get_next_scene(0))
#

# print(em.get_next_scene(0))
# print(em.get_next_scene(1))
# print(em.get_next_scene(0))
# 
# print(em.get_next_scene(0))
# print(em.get_next_scene(1))
# print(em.get_next_scene(0))

#print(em.validate_choices("Red_Meets_Wolf_Fight", "Fight"))
#em.apply_choice_postconditions("Red_Meets_Wolf_Fight", "Fight", "No")

# print(em.get_next_scene(0))
# print(em.get_next_scene(1))
# print(em.get_next_scene(0))
# 
# print(em.get_next_scene(0))
# print(em.get_next_scene(1))
# print(em.get_next_scene(0))

#em.apply_choice_postconditions("Common_Scene", "Restaurant", "Open")
#print(em.get_next_scene(0))
#print(em.get_next_scene(1))
#print(em.get_next_scene(1))
#print(em.get_next_scene(1))
#em.end_narrative()
#print('\nFor Plot:', em.gamestate.plot['progression'])
#print("Wolf scenes:", em.gamestate.players[1].get_scenes(), '\n')