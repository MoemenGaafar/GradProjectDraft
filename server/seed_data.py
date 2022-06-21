from probability_calculator import ProbabilityCalculator
from generate_player_choices_sheet import generate_new_sheet
import random

generate_new_sheet()

calc = ProbabilityCalculator('player_choices_sheet.csv')

for i in range(100):

    wolfFight = random.randint(0, 1)

    if wolfFight:
        redFight = 1
    else:
        redFight = 0

    choices = {'Red_Meets_Wolf_Fight_Fight-Wolf_Yes': wolfFight, 'Red_Meets_Wolf_Fight_Fight-Wolf_No': 1-wolfFight,
            'Red_Meets_Wolf_Fight_Fight-Red_Yes': redFight, 'Red_Meets_Wolf_Fight_Fight-Red_No': 1-redFight,
            'Wolf1_Bunny_Eat': 1, 'Wolf1_Bunny_Ignore': None, 'Wolf1_Bunny_Help': None, 'Red1_Bird_Give': 0, 'Red1_Bird_Ignore': 1}

    calc.add_entry(choices)