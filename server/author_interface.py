from author_interface_functionalities import *


def write_file(data, file):
    json_data = json.dumps(data, indent=4)
    with open(file, "w") as f:
        f.write(json_data)


# Create initial layout
sg.theme('DarkPurple4')
button_size = (14, 2)
main_layout = [[sg.Button("Start", size=button_size)],
               [sg.Button("Players", size=button_size), sg.Button("Scenes", size=button_size)],
               [sg.Button("Initial State", size=button_size), sg.Button("Plot", size=button_size)],
               [sg.Button("Validate EM", size=button_size), sg.Button("Validate RenPy", size=button_size)],
               [sg.Button("Generate Player Choices Sheet", size=(30, 2))],
               [sg.Button("Exit", size=button_size)]]

# Create the window
window = sg.Window('The Multiplayer Interactive Maker', main_layout, element_padding=(6, 6), font=("Georgia", 12),
                   element_justification='c')
# Create an event loop
while True:
    event, values = window.read()
    # Handle button clicks
    if event == "Start":
        window.hide()
        open_players()
        window.un_hide()
    elif event == "Players":
        window.hide()
        open_players()
        window.un_hide()
    elif event == "Scenes":
        window.hide()
        open_scenes()
        window.un_hide()
    elif event == "Initial State":
        window.hide()
        open_initial_state()
        window.un_hide()
    elif event == "Plot":
        window.hide()
        open_plot()
        window.un_hide()
    elif event == "Validate EM":
        window.hide()
        open_validate_em()
        window.un_hide()
    elif event == "Validate RenPy":
        window.hide()
        open_validate_renpy()
        window.un_hide()
    elif event == "Generate Player Choices Sheet":
        generate_player_choices_sheet()

    # End program if user closes window or presses the Exit button
    elif event == "Exit" or event == sg.WIN_CLOSED:
        write_file(scenes_list, scene_file)
        write_file(players_data, players_file)
        write_file(plot, plot_file)
        write_file(initial_state, state_file)
        break
window.close()