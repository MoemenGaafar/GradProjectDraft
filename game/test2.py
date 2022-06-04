from probability_calculator import ProbabilityCalculator

calc = ProbabilityCalculator('player_choices_sheet.csv')

#choices = {'Red1_Bird_Give': 1, 'Red1_Bird_Ignore': 0, 
#            'Bunny_Calls_Hunter_Hunter_Call': 0, 'Bunny_Calls_Hunter_Hunter_Ignore': 1}

choices2 = {'Red_Meets_Wolf_Fight_Fight-Wolf_Yes': 0, 'Red_Meets_Wolf_Fight_Fight-Wolf_No': 1,
            'Red_Meets_Wolf_Fight_Fight-Red_Yes': 0, 'Red_Meets_Wolf_Fight_Fight-Red_No': 1,
            'Wolf1_Bunny_Eat': 1, 'Wolf1_Bunny_Ignore': 0, 'Wolf1_Bunny_Help': 0, 'Red1_Bird_Give': 1, 'Red1_Bird_Ignore': 0}

#calc.add_entry(choices)
calc.add_entry(choices2)