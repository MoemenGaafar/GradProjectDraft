# type: ignore

define red = Character('Red Riding Hood')
define wolf = Character('Wolf')

label Red1:
    "Red1"
    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Bird",
            prompt = "Do I give it some?",
            choices = [("Give bird some seeds", "Give"), ("Ignore bird", "Ignore")], 
            reactions = ["It's cute tho I'll give it some", "I will not give it any to learn a lesson"])
    jump next

label Wolf1:
    "Wolf1"
    python:
        make_choice(character = wolf,
            current_scene = current_scene, 
            menu_label = "Bunny",
            prompt = "What should I do?",
            choices = [("Help Bunny", "Help"), ("Ignore Bunny", "Ignore"), ("Attack Bunny and Eat it", "Eat")], 
            reactions = ["Help", "Ignore", "Eat"])
    jump next

label Red_Meets_Bunny:
    "Red_Meets_Bunny"
    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Bunny",
            prompt = "What should I do?",
            choices = [("Help Bunny", "Help"), ("Ignore Bunny", "Ignore")], 
            reactions = ["Help", "Ignore"])
    jump next

label Red_Finds_Bunny_Corpse:
    "Red_Finds_Bunny_Corpse"
    jump next

label Wolf_Spots_Red_Bunny:
    "Wolf_Spots_Red_Bunny"
    jump next

label Wolf_Spots_Red_NoBunny:
    "Wolf_Spots_Red_NoBunny"
    jump next

label Red_Wolf_Meet:
    "Red_Wolf_Meet"
    jump next

label Bunny_Calls_Hunter:
    "Bunny_Calls_Hunter"
    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Hunter",
            prompt = "What should I do?",
            choices = [("Call Hunter", "Call"), ("Forgive Wolf", "Ignore")], 
            reactions = ["Call", "Ignore"])
    jump next

label Bunny_Makes_Peace:
    "Bunny_Makes_Peace"
    jump next

label Red_Meets_Wolf_Fight:
    "Red_Meets_Wolf_Fight"
    python:
        make_choice(character = wolf,
            current_scene = current_scene, 
            menu_label = "Fight-Wolf",
            prompt = "What should I do?",
            choices = [("Threaten", "Yes"), ("Act Kindly", "No")], 
            reactions = ["Threaten", "Kind"])

        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Fight-Red",
            prompt = "What should I do?",
            choices = [("Threaten", "Yes"), ("Act Kindly", "No")], 
            reactions = ["Threaten", "Kind"])
        
    jump next

label Hunter_Kills_Wolf:
    "Hunter_Kills_Wolf"
    jump next

label All_Become_Friends:
    "All_Become_Friends"
    jump next

label Wolf_Eats_Red:
    "Wolf_Eats_Red"
    jump next