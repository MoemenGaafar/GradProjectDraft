# type: ignore

define red = Character('Red Riding Hood')
define wolf = Character('Wolf')

label Red1:
    "Red1"
    jump next

label Wolf1:
    "Wolf1"
    jump next

label Common_Scene:
    "Common Scene"
    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Restaurant",
            prompt = "Do I open the restaurant?",
            choices = [("Open", "Open"), ("Close", "Close")], 
            reactions = ["Alright! Got it!", "I better leave it alone"])
    jump next

label Red_Decides_Restaurant:
    "Red_Decides_Restaurant"
    jump next

label Red_Ending:
    "Red_Ending"
    jump next

label Wolf_Goes_Restaurant:
    "Wolf_Goes_Restaurant"
    jump next

label Wolf_Goes_Supermarket:
    "Wolf_Goes_Supermarket"
    jump next

label Wolf_Restaurant_Closed:
    "Wolf_Restaurant_Closed"
    jump next

label Wolf_Restaurant_Open:
    "Wolf_Restaurant_Open"
    jump next

label Wolf_Buys_Food:
    "Wolf_Buys_Food"
    jump next

label Wolf_Happy_Ending:
    "Wolf_Happy_Ending"
    jump next

label Wolf_Neutral_Ending:
    "Wolf_Neutral_Ending"
    jump next

label Wolf_Sad_Ending:
    "Wolf_Sad_Ending"
    jump next