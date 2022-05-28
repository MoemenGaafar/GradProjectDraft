from math import floor

import PySimpleGUI as sg
import json
from em_search import EM_Searcher
import pandas as pd
from em_functionalities import parse_entry

sg.theme('DarkPurple4')


def load_file(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


# Load files
state_file = "initial_state.json"
scene_file = "scenes.json"
plot_file = "plot.json"
players_file = "players_data.json"

scenes_list = load_file(scene_file)
players_data = load_file(players_file)
plot = load_file(plot_file)
initial_state = load_file(state_file)

# Save all state features so far
features = []


def read_features():
    for feature in initial_state:
        if feature not in features:
            features.append(feature)
    for scene in scenes_list:
        for feature in scenes_list[scene]["preconditions"]:
            if feature not in features:
                features.append(feature)
        for feature in scenes_list[scene]["postconditions"]:
            if feature not in features:
                features.append(feature)
        for menu in scenes_list[scene]["menus"]:
            for choice in scenes_list[scene]["menus"][menu]:
                for feature in scenes_list[scene]["menus"][menu][choice]:
                    if feature not in features:
                        features.append(feature)


read_features()


def open_players():
    chars = []
    first_scenes = []
    players_data["players_count"] = 2
    for char in players_data["characters"]:
        chars.append(char)
        first_scenes.append(players_data["characters"][char]["first scene"])
    while len(chars) < 2:
        chars.append('Enter name')
        first_scenes.append('Enter scene')

    button_size = (11, 2)
    textbox_size = (14, 2)
    layout = [[sg.Text('Characters:', justification='r')],
              [sg.InputText(key='-char1-', size=textbox_size, default_text=str(chars[0])), sg.Text('First Scene: '),
               sg.InputText(key='-char1scene-', size=textbox_size,
                            default_text=str(first_scenes[0]))],
              [sg.InputText(key='-char2-', size=textbox_size, default_text=str(chars[1])), sg.Text('First Scene: '),
               sg.InputText(key='-char2scene-', size=textbox_size,
                            default_text=str(first_scenes[1]))],
              [sg.Button("Save", size=button_size), sg.Button("Cancel", size=button_size),
               sg.Button("Next (Scenes)", size=button_size)]]

    window = sg.Window("Players", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12), modal=True,
                       element_justification='c')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event in ('Save', 'Next (Scenes)'):
            if values['-char1-'] == "" or values['-char2-'] == "" or values['-char1scene-'] == "" or values[
                '-char2scene-'] == "":
                sg.popup("One or more field is missing", font=("Georgia", 12))
                continue
            players_data["characters"] = {}
            players_data["characters"][values['-char1-']] = {"first scene": values['-char1scene-']}
            players_data["characters"][values['-char2-']] = {"first scene": values['-char2scene-']}
            if values['-char1scene-'] not in scenes_list:
                scenes_list[values['-char1scene-']] = {"player count": 1, "player": [chars[0]], "preconditions": {},
                                                       "postconditions": {}, "menus": {}, "scene number": ['*'],
                                                       "end scene": 0}
            if values['-char2scene-'] not in scenes_list:
                scenes_list[values['-char2scene-']] = {"player count": 1, "player": [chars[1]], "preconditions": {},
                                                       "postconditions": {}, "menus": {}, "scene number": ['*'],
                                                       "end scene": 0}

            if event == 'Next (Scenes)':
                window.hide()
                open_scenes()

            break

    window.close()


def open_scenes():
    scenes = []
    i = 0
    for scene in scenes_list:
        scenes.append(scene)
        i += 1

    if len(players_data["characters"]) < 2:
        sg.popup('Make sure to complete the Players field first')
        return

    chars = []
    for char in players_data["characters"]:
        chars.append(char)

    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)
    list = []
    num = 7
    for j in range(floor(len(scenes) / num) + 1):
        mini_list = []
        for i in range(num):
            place = j * num + i
            if place == len(scenes):
                break
            mini_list.append(sg.Button(scenes[place]))
        list.append(mini_list)
    list.append([sg.Text("")])

    layout = [[sg.Column(list, scrollable=True, vertical_scroll_only=True, size=(1100, 400))],
              [sg.Button('Create new features', size=button_size),
               sg.Button("New Scene", size=button_size),
               sg.Button("Ok", size=button_size),
               sg.Button("Next (Plot)", size=button_size)]]
    window = sg.Window("Scenes", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12), modal=True,
                       element_justification='c')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Ok"):
            break
        elif event == 'Next (Plot)':
            window.hide()
            open_plot()
            break
        elif event == 'Create new features':
            window.hide()
            open_features()
            window.un_hide()
        elif event == "New Scene":
            window.hide()
            scenes_list['New Scene'] = {"player count": 2, "player": [chars[0], chars[1]], "preconditions": {},
                                        "postconditions": {}, "menus": {}, "scene number": ['*'], "end scene": 0}
            open_scene('New Scene', chars)
            break
        elif event in scenes:
            window.hide()
            open_scene(event, chars)
            break

    window.close()


def open_scene(scene, chars):
    # when adding feature make sure to make it 'None' in initial state
    default0 = False
    if chars[0] in scenes_list[scene]["player"]:
        default0 = True
    default1 = False
    if chars[1] in scenes_list[scene]["player"]:
        default1 = True
    default2 = False
    if "end scene" in scenes_list[scene]:
        default2 = scenes_list[scene]["end scene"]

    menus = []
    for menu in scenes_list[scene]['menus']:
        menus.append(menu)
    scene_nums = []
    for num in scenes_list[scene]['scene number']:
        scene_nums.append(str(num))

    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)
    layout = [[sg.Text('Scene Name: '), sg.InputText(key='-n-', default_text=scene)],
              [sg.Checkbox(chars[0], default=default0, key='-p1-', text_color='white'),
               sg.Checkbox(chars[1], default=default1, key='-p2-', text_color='white')],
              [sg.Text('Scene Numbers:')], [sg.Text('(Separate different numbers by a comma or type "*" to not use '
                                                    'scene numbering)', text_color='white')],
              [sg.InputText(default_text=','.join(scene_nums), key='-nums-')],
              [sg.Text('Is an end scene?'), sg.Checkbox('Yes', default=default2, key='-e-', text_color='white')],
              [sg.Button('Preconditions', size=button_size), sg.Button('Postconditions', size=button_size),
               sg.Button('Create new features', size=button_size)],
              [sg.Text('Menus:')]]
    num = 6
    col = []
    for j in range(floor(len(menus) / num) + 1):
        mini_list = []
        for i in range(num):
            place = j * num + i
            if place == len(menus):
                break
            mini_list.append(sg.Button(menus[place]))
        col.append(mini_list)
    layout.append([sg.Column(col, scrollable=True, vertical_scroll_only=True, size=(550, 200))])
    layout.append([sg.Text("")])
    layout.append([sg.Button("New Menu", size=button_size), sg.Button("Save", size=button_size),
                   sg.Button("Cancel", size=button_size), sg.Button('Delete', size=button_size)])

    window = sg.Window(scene, layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12), modal=True)

    if scene != 'New Scene':
        window['-n-'].update(disabled=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            if 'New Scene' in scenes_list:
                del scenes_list['New Scene']
            break
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Delete':
            del scenes_list[scene]
            sg.popup('Scene deleted successfully')
            break
        elif event == 'Create new features':
            window.hide()
            open_features()
            window.un_hide()
        elif event == "Preconditions":
            window.hide()
            open_preconditions(scene)
            window.un_hide()
        elif event == "Postconditions":
            window.hide()
            open_postconditions(scene)
            window.un_hide()
        elif event in menus:
            window.hide()
            open_menu(scene, event, chars)
            break
        elif event == "New Menu":
            window.hide()
            scenes_list[scene]['menus']['New Menu'] = {}
            open_menu(scene, 'New Menu', chars)
            break
        elif event == "Save":
            if values['-n-'] == 'New Scene':
                sg.popup('The name "New Scene" is not allowed.')
                continue
            player = []
            if values['-nums-'] == '':
                sg.popup('Please insert one or more scene numbers separated by a comma.')
                continue
            try:
                scene_nums = []
                if values['-nums-'] == '*':
                    scene_nums.append(values['-nums-'])
                else:
                    nums = values['-nums-'].split(',')
                    for num in nums:
                        num = int(num.strip())
                        scene_nums.append(num)
            except:
                sg.popup('Your scene numbers input is incorrect.')
                continue
            if values['-p1-']:
                player.append(chars[0])
            if values['-p2-']:
                player.append(chars[1])
            end = 0
            if values['-e-']:
                end = 1
            scenes_list[values['-n-']] = scenes_list[scene]
            scenes_list[values['-n-']]['player count'] = len(player)
            scenes_list[values['-n-']]['scene number'] = scene_nums
            scenes_list[values['-n-']]['player'] = player
            scenes_list[values['-n-']]['end scene'] = end
            if 'New Scene' in scenes_list:
                del scenes_list['New Scene']
            break
    window.close()
    open_scenes()


def open_preconditions(scene):
    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)

    def new_line(i):
        return [[sg.Combo(features, key=f'-p{i}-'),
                 sg.Combo(['less than', 'is', 'more than'], key=f'-t{i}-'),
                 sg.InputText(key=f'-v{i}-', size=input_size)]]

    list = []
    i = 0
    for precondition in scenes_list[scene]['preconditions']:
        mini_list = [sg.Combo(features, default_value=precondition, key=f'-p{i}-'),
                     sg.Combo(['less than', 'is', 'more than'], key=f'-t{i}-',
                              default_value=scenes_list[scene]['preconditions'][precondition][0]),
                     sg.InputText(scenes_list[scene]['preconditions'][precondition][1], key=f'-v{i}-',
                                  size=input_size)]
        list.append(mini_list)
        i += 1

    layout = [[sg.Column(list, key='-Column-', scrollable=True, vertical_scroll_only=True, size=(600, 300))],
              [sg.Button("Add Precondition", size=button_size),
               sg.Button("Remove Row", size=button_size),
               sg.Button("Save", size=button_size),
               sg.Button("Cancel", size=button_size)]]
    window = sg.Window(scene + " Preconditions", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       modal=True)

    removed = []
    while True:
        cont = False
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Save':
            preconditions = []
            for j in range(i):
                if j in removed:
                    continue
                if values[f'-p{j}-'] in preconditions:
                    sg.popup('One or more preconditions is repeated.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    preconditions.append(values[f'-p{j}-'])
                if values[f'-t{j}-'] in ('less than', 'more than'):
                    try:
                        float(values[f'-v{j}-'])
                    except:
                        sg.popup(
                            'One or more preconditions with "less than" or "more than" requirement is not a float.',
                            font=("Georgia", 12))
                        cont = True
                        break
                if values[f'-p{j}-'] == '' or values[f'-t{j}-'] == '' or values[f'-v{j}-'] == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
            if cont:
                continue
            scenes_list[scene]['preconditions'] = {}
            for j in range(i):
                if j in removed:
                    continue
                scenes_list[scene]['preconditions'][values[f'-p{j}-']] = [values[f'-t{j}-'], values[f'-v{j}-']]
            break
        elif event == 'Add Precondition':
            window.extend_layout(window['-Column-'], new_line(i))
            i += 1
        elif event == 'Remove Row':
            j = i - 1
            while j in removed:
                j = j - 1
                if j == -1:
                    break
            if j > -1:
                removed.append(j)
                window[f'-p{j}-'].update(disabled=True)
                window[f'-v{j}-'].update(disabled=True)
                window[f'-t{j}-'].update(disabled=True)
    window.close()


def open_postconditions(scene, menu='', choice=''):
    scene_type = scenes_list[scene]['player count']
    s_plot_features = plot["single player beat features"]
    m_plot_features = plot["multi player beat features"]
    new_postconditions = features.copy()
    if menu:
        if scene_type == 1:
            for feature in s_plot_features:
                if feature in new_postconditions:
                    new_postconditions.remove(feature)
        else:
            for feature in m_plot_features:
                if feature in new_postconditions:
                    new_postconditions.remove(feature)

    window_name = scene
    location = scenes_list[scene]['postconditions']
    if menu != '':
        window_name = window_name + " : " + menu + " : " + choice
        location = scenes_list[scene]['menus'][menu][choice]

    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)

    def new_line(i):
        return [[sg.Combo(new_postconditions, key=f'-p{i}-'),
                 sg.Combo(['set', 'add'], key=f'-t{i}-'),
                 sg.InputText(key=f'-v{i}-', size=input_size)]]

    list = []
    i = 0
    for postcondition in location:
        mini_list = [sg.Combo(new_postconditions, default_value=postcondition, key=f'-p{i}-'),
                     sg.Combo(['set', 'add'], key=f'-t{i}-',
                              default_value=location[postcondition][0]),
                     sg.InputText(location[postcondition][1], key=f'-v{i}-',
                                  size=input_size)]
        list.append(mini_list)
        i += 1

    layout = [[sg.Column(list, key='-Column-', scrollable=True, vertical_scroll_only=True, size=(600, 300))],
              [sg.Button("Add Postcondition", size=button_size),
               sg.Button("Remove Row", size=button_size),
               sg.Button("Save", size=button_size),
               sg.Button("Cancel", size=button_size)]]
    window = sg.Window(window_name, layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       modal=True)

    removed = []
    while True:
        cont = False
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Save':
            postconditions = []
            for j in range(i):
                if j in removed:
                    continue
                if values[f'-p{j}-'] in postconditions:
                    sg.popup('One or more postconditions is repeated.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    postconditions.append(values[f'-p{j}-'])
                if values[f'-t{j}-'] == 'add':
                    try:
                        float(values[f'-v{j}-'])
                    except:
                        sg.popup('One or more postconditions with "add" effect is not a float.',
                                 font=("Georgia", 12))
                        cont = True
                        break
                if values[f'-p{j}-'] == '' or values[f'-t{j}-'] == '' or values[f'-v{j}-'] == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
            if cont:
                continue
            if menu != '':
                scenes_list[scene]['menus'][menu][choice] = {}
            else:
                scenes_list[scene]['postconditions'] = {}
            for j in range(i):
                if j in removed:
                    continue
                if menu != '':
                    scenes_list[scene]['menus'][menu][choice][values[f'-p{j}-']] = [values[f'-t{j}-'],
                                                                                    values[f'-v{j}-']]
                else:
                    scenes_list[scene]['postconditions'][values[f'-p{j}-']] = [values[f'-t{j}-'], values[f'-v{j}-']]
            break
        elif event == 'Add Postcondition':
            window.extend_layout(window['-Column-'], new_line(i))
            i += 1
        elif event == 'Remove Row':
            j = i - 1
            while j in removed:
                j = j - 1
                if j == -1:
                    break
            if j > -1:
                removed.append(j)
                window[f'-p{j}-'].update(disabled=True)
                window[f'-v{j}-'].update(disabled=True)
                window[f'-t{j}-'].update(disabled=True)
    window.close()


def open_menu(scene, menu, chars):
    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)

    def new_line(i):
        return [[sg.InputText(key=f'-c{i}-', size=input_size),
                 sg.Button('Postconditions', key=f'-p{i}-', size=button_size)]]

    list = []
    i = 0
    for choice in scenes_list[scene]['menus'][menu]:
        mini_list = [sg.InputText(choice, key=f'-c{i}-', size=input_size),
                     sg.Button('Postconditions', key=f'-p{i}-', size=button_size)]
        list.append(mini_list)
        i += 1

    layout = [[sg.Text('Menu Name: '), sg.InputText(key='-n-', default_text=menu)],
              [sg.Text('Choices:')],
              [sg.Column(list, key='-Column-', scrollable=True, vertical_scroll_only=True, size=(600, 300))],
              [sg.Button("Add Choice", size=button_size),
               sg.Button("Remove Row", size=button_size),
               sg.Button("Delete", size=button_size),
               sg.Button("Save", size=button_size),
               sg.Button("Cancel", size=button_size)]]
    window = sg.Window(scene + " : " + menu, layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       modal=True)

    removed = []

    if menu != 'New Menu':
        window['-n-'].update(disabled=True)

    while True:
        cont = False
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            if "New Menu" in scenes_list[scene]['menus']:
                del scenes_list[scene]['menus']['New Menu']
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Save':
            if values['-n-'] == 'New Menu':
                sg.popup('The name "New Menu" is not allowed.')
                continue
            choices = []
            for j in range(i):
                if j in removed:
                    continue
                if values[f'-c{j}-'] in choices:
                    sg.popup('One or more choices is repeated.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    choices.append(values[f'-c{j}-'])
                if values[f'-c{j}-'] == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
            if cont:
                continue
            new_dict = {}
            for j in range(i):
                if j in removed:
                    continue
                if values[f'-c{j}-'] in scenes_list[scene]['menus'][menu]:
                    new_dict[values[f'-c{j}-']] = scenes_list[scene]['menus'][menu][values[f'-c{j}-']]
                else:
                    new_dict[values[f'-c{j}-']] = {}
            scenes_list[scene]['menus'][values['-n-']] = new_dict
            if "New Menu" in scenes_list[scene]['menus']:
                del scenes_list[scene]['menus']['New Menu']
            break
        elif '-p' in event:
            if values[f'-c{event[2]}-'] not in scenes_list[scene]['menus'][menu]:
                scenes_list[scene]['menus'][menu][values[f'-c{event[2]}-']] = {}
            window.hide()
            open_postconditions(scene, menu, values[f'-c{event[2]}-'])
            window.un_hide()
        elif event == 'Add Choice':
            window.extend_layout(window['-Column-'], new_line(i))
            i += 1
        elif event == 'Remove Row':
            j = i - 1
            while j in removed:
                j = j - 1
                if j == -1:
                    break
            if j > -1:
                removed.append(j)
                window[f'-c{j}-'].update(disabled=True)
                window[f'-p{j}-'].update(disabled=True)
        elif event == 'Delete':
            del scenes_list[scene]['menus'][menu]
            sg.popup('Menu deleted successfully')
            break
    window.close()
    open_scene(scene, chars)


def open_features():
    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)
    i = 1
    col = [[sg.InputText(key=f'-f{i}-')]]

    def new_line(j):
        return [[sg.InputText(key=f'-f{j}-')]]

    layout = [[sg.Text("New Features:")], [sg.Column(col, key='-Column-')],
              [sg.Button('Add New Feature', size=button_size)],
              [sg.Button("Save", size=button_size), sg.Button("Cancel", size=button_size)]]
    window = sg.Window("Scenes", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12), modal=True)

    while True:
        cont = False
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Save':
            for j in range(i):
                if values[f'-f{j}-'] == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
            if cont:
                continue
            for j in range(i):
                initial_state[values[f'-f{j}-']] = 'None'
            read_features()
            break
        elif event == 'Add New Feature':
            i += 1
            window.extend_layout(window['-Column-'], new_line(i))
    window.close()


def open_initial_state():
    button_size = (11, 2)
    textbox_size = (14, 2)

    layout = [[sg.Text('Initial state:', text_color='white')]]
    layout_list2 = [sg.Button("Save", size=button_size), sg.Button("Cancel", size=button_size),
                    sg.Button("Next (Plot)", size=button_size)]
    layout_list = [[sg.Text(key=f"-feature{i}-", text=features[i], size=(15, None)),
                    sg.Text('Initial value: ', justification='right', text_color='white'),
                    sg.InputText(key=f"-featurevalue{i}-", justification='center', size=textbox_size,
                                 default_text=str(initial_state[features[i]]))] for i in range(len(features))]

    layout.append(layout_list)
    layout.append(layout_list2)

    window = sg.Window("Initial State", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       resizable=True, modal=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event in ('Save', 'Next (Plot)'):
            for i in range(len(features)):
                if values[f"-featurevalue{i}-"] == "" or values[f"-featurevalue{i}-"] == " ":
                    value = "None"
                else:
                    value = values[f"-featurevalue{i}-"]
                initial_state[features[i]] = value

            if event == 'Next (Plot)':
                window.hide()
                open_plot()

            break

    window.close()


def open_plot():
    if len(players_data["characters"]) < 2:
        sg.popup('Make sure to complete the Players field first')
        return

    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)
    layout = [[sg.Text("Gate every ", size=textbox_size), sg.InputText(key="-gate-", default_text="Type a number",
                                                                       size=input_size), sg.Text("EM scenes.")],
              [sg.Text("Gating holds a faster player till the slower player has seen the same number of scenes."
                       "\nSelect this value according to the length and dramatic weight of your typical scene.",
                       text_color='white')],
              [sg.Text("Plot points count: ", size=textbox_size), sg.InputText(key='-plot-', default_text='Type a '
                                                                                                          'number',
                                                                               size=input_size)],
              [sg.Text("Single player beat features count: ", size=textbox_size), sg.InputText(key='-s-',
                                                                                               default_text='Type a '
                                                                                                            'number',
                                                                                               size=input_size)],
              [sg.Text("Multi-player beat features count: ", size=textbox_size), sg.InputText(key='-m-',
                                                                                              default_text='Type a '
                                                                                                           'number',
                                                                                              size=input_size)],
              [sg.Button('Apply', size=button_size), sg.Button('Cancel', size=button_size)]]

    window = sg.Window("Plot", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       resizable=True, modal=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Apply':
            if values['-gate-'] == '' or values['-plot-'] == '' or values['-s-'] == '' or values['-m-'] == '':
                sg.popup('One or more fields is missing.', font=("Georgia", 12))
                continue
            else:
                try:
                    gate = int(values['-gate-'])
                    plot_points = int(values['-plot-'])
                    s = int(values['-s-'])
                    m = int(values['-m-'])
                except:
                    sg.popup('One or more fields is not a number.', font=("Georgia", 12))
                    continue

            window.hide()
            open_plot_features(gate, plot_points, s, m)
            break

    window.close()


def open_plot_features(gate, plot_points, s, m):
    button_size = (11, 2)
    textbox_size = (30, None)
    input_size = (18, 2)
    chars = []
    for char in players_data["characters"]:
        chars.append(char)
    layout = [[sg.Text('Input your features: ')],
              [sg.Text('Single player scene features: ', text_color='white')]]
    for i in range(s):
        layout.append([sg.Combo(features, key=f'-s{i}-'), sg.Text("Weight: "),
                       sg.InputText("Type a float", key=f'-sw{i}-', size=input_size)])
        layout.append([sg.Checkbox(chars[0], key=f'-c1{i}-', text_color='white'),
                       sg.Checkbox(chars[1], key=f'-c2{i}-', text_color='white')])
    layout.append([sg.Text('Multi-player scene features: ', text_color='white')])
    for i in range(m):
        layout.append([sg.Combo(features, key=f'-m{i}-'), sg.Text("Weight: "),
                       sg.InputText("Type a float", key=f'-mw{i}-', size=input_size)])
    layout.append([sg.Text('Select whether each plot point is single player or multiplayer: ')])
    for i in range(plot_points):
        layout.append([sg.Text(f'{i + 1}'), sg.Combo(["Single player", "Multiplayer"], key=f'-p{i}-')])

    l = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True, size=(500, 500))],
         [sg.Button('Apply', size=button_size), sg.Button('Cancel', size=button_size)]]

    window = sg.Window("Plot", l, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       resizable=True, modal=True)

    while True:
        event, values = window.read()
        cont = False
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event == 'Apply':
            s_features = []
            m_features = []
            s_weights = []
            m_weights = []
            p_types = []
            s_features_0 = []
            s_features_1 = []
            for i in range(s):
                if str(values[f'-s{i}-']) == '' or str(values[f'-sw{i}-']) == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
                if not values[f'-c1{i}-'] and not values[f'-c2{i}-']:
                    sg.popup('One or more single player features is objective for no character\'s single scenes.',
                             font=("Georgia", 12))
                    cont = True
                    break
                try:
                    temp = float(values[f'-sw{i}-'])
                except:
                    sg.popup('One or more weight fields is not a number.', font=("Georgia", 12))
                    cont = True
                    break
                if str(values[f'-s{i}-']) in s_features:
                    sg.popup('One or more single player scene features is picked more than once.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    s_weights.append(float(values[f'-sw{i}-']))
                    s_features.append(str(values[f'-s{i}-']))
                    if values[f'-c1{i}-']:
                        s_features_0.append(values[f'-s{i}-'])
                    if values[f'-c2{i}-']:
                        s_features_1.append(values[f'-s{i}-'])
            if cont:
                continue

            for i in range(m):
                if str(values[f'-m{i}-']) == '' or str(values[f'-mw{i}-']) == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
                try:
                    temp = float(values[f'-mw{i}-'])
                except:
                    sg.popup('One or more weight fields is not a number.', font=("Georgia", 12))
                    cont = True
                    break
                if str(values[f'-m{i}-']) in m_features:
                    sg.popup('One or more multi-player scene features is picked more than once.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    m_weights.append(float(values[f'-mw{i}-']))
                    m_features.append(str(values[f'-m{i}-']))
            if cont:
                continue

            for i in range(plot_points):
                if str(values[f'-p{i}-']) == '':
                    sg.popup('One or more fields is missing.', font=("Georgia", 12))
                    cont = True
                    break
                else:
                    if str(values[f'-p{i}-']) == "Multiplayer":
                        p_types.append("m")
                    else:
                        p_types.append("s")

            if cont:
                continue

            window.hide()
            open_plot_feature_values(gate, plot_points, s, m, s_features, m_features, s_weights, m_weights, p_types,
                                     chars, s_features_0, s_features_1)
            break

    window.close()


def open_plot_feature_values(gate, plot_points, s, m, s_features, m_features, s_weights, m_weights, p_types, chars,
                             s_features_0, s_features_1):
    plot_features = []
    for i in range(plot_points):
        if p_types[i] == "s":
            plot_features.append(s_features)
        else:
            plot_features.append(m_features)
    button_size = (11, 2)
    textbox_size = (18, None)
    input_size = (18, 2)
    layout = []
    for i in range(plot_points):
        list = [[sg.Text(f"Plot point {i + 1}:", text_color='white')]]
        for j in range(len(plot_features[i])):
            list = list + [
                [sg.Text(plot_features[i][j], size=textbox_size), sg.Text("Value ="), sg.InputText(key=f'-f{i}-{j}-',
                                                                                                   size=input_size)]]
        layout = layout + list

    l = [[sg.Column(layout, scrollable=True, vertical_scroll_only=True, size=(450, 300))],
         [sg.Button('Save', size=button_size),
          sg.Button('Cancel', size=button_size),
          sg.Button('Next (Validate EM)', size=(16, 2))]]

    window = sg.Window("Plot", l, finalize=True, element_padding=(6, 6), font=("Georgia", 12),
                       resizable=True, modal=True)

    while True:
        event, values = window.read()
        cont = False
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sg.popup("Your changes were not saved.", font=("Georgia", 12))
            break
        elif event in ('Save', 'Next (Validate EM)'):
            for i in range(plot_points):
                for j in range(len(plot_features[i])):
                    if values[f'-f{i}-{j}-'] == '':
                        sg.popup('One or more fields is missing.', font=("Georgia", 12))
                        cont = True
                        break
                if cont:
                    break
            if cont:
                continue
            plot["gate every"] = gate
            plot["single player beat features"] = s_features
            plot["single player beat weights"] = s_weights
            plot["multi player beat features"] = m_features
            plot["multi player beat weights"] = m_weights
            progression = []
            for i in range(plot_points):
                progression_i = [p_types[i]]
                values_i = []
                for j in range(len(plot_features[i])):
                    values_i.append(values[f'-f{i}-{j}-'])
                progression_i.append(values_i)
                progression.append(progression_i)
            plot["progression"] = progression

            players_data["characters"][chars[0]]["objective features"] = s_features_0
            players_data["characters"][chars[1]]["objective features"] = s_features_1

            if event == "Next (Validate EM)":
                window.hide()
                open_validate_em()

            break

    window.close()


def open_validate_em():
    button_size = (14, 2)
    layout = [
        [sg.Multiline(size=(80, 25), key='-OUT-', reroute_stdout=True)],
        [sg.Button('Ok', size=button_size), sg.Button("Next (Validate Renpy)", size=button_size)]]
    window = sg.Window("EM Validation", layout, finalize=True, element_padding=(6, 6), font=("Georgia", 12), modal=True,
                       element_justification='c')

    searcher = EM_Searcher()
    solutions = searcher.validate()
    window['-OUT-'].print('------------------Solutions----------------\n')
    for sol in solutions:
        window['-OUT-'].print(sol, '\n')
    searcher.visulaize_solutions()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Ok', "Next (Validate Renpy)"):
            if event == "Next (Validate Renpy)":
                window.hide()
                open_validate_renpy()
            break

    window.close()


def open_validate_renpy():
    em_scenes = []
    for scene in scenes_list:
        em_scenes.append(scene)
    renpy_scenes = []
    with open("script.rpy") as s:
        renpy_scene_data = s.readlines()
    for line in renpy_scene_data:
        line = line.replace(" ", "")
        if line.startswith("label"):
            renpy_scenes.append(line[5:-2])
    renpy_scenes_copy = renpy_scenes.copy()
    for scene in renpy_scenes:
        if scene in em_scenes:
            em_scenes.remove(scene)
            renpy_scenes_copy.remove(scene)

    sg.popup('The following Experience Manager scenes were found with no corresponding RenPy scene. \nMake sure to '
             'add corresponding RenPy scenes to ensure the game functions correctly. \n\n' + '\n'.join(em_scenes) +
             '\n\nThe following RenPy scenes were fount with no corresponding Experience Manager scenes. \nMake sure '
             'this is intended. \n\n' + '\n'.join(renpy_scenes_copy), font=("Georgia", 12), title='RenPy Validation',
             text_color='white')


def generate_player_choices_sheet():
    indices = []

    for label in scenes_list:
        scene = scenes_list[label]
        for menu_label in scene['menus']:
            menu = scene['menus'][menu_label]
            for choice in menu:
                indices.append(parse_entry(label, menu_label, choice))

    sheet = pd.DataFrame(index=indices)
    sheet.to_csv('./player_choices_sheet.csv')
    sg.popup('Player Choices Sheet generated successfully.')
