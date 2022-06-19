# type: ignore

define red = Character('Red Riding Hood')
define wolf = Character('Wolf')
define bird = Character('Bird')
define hunter = Character('Hunter')
define bunny = Character('Bunny')


label Red1:

    scene street1
    with fade

    "Once upon an afternoon..."

    "In a city crowded as any, hotter than most"

    "Little Red lost her way on her way to the GRAMMYs..."

    show red at left
    with dissolve

    red "Oh no! It appears that I am lost!"

    red "I must find my way to the bus station and find it fast!"

    "So Red was set to find her way. She looked around for any signs of a bus. Except..."

    show bird at right
    with dissolve

    red "Oh look at that! It's a lovely bird!"

    bird "Why Hello! You are a lovely girl."

    bird "But would you be lovelier and give me some of those seeds you keep in you purse?"

    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Bird",
            prompt = "Do I give it some?",
            choices = [("Give bird some seeds", "Give"), ("Ignore bird", "Ignore")], 
            reactions = ["It's cute, I'll give it seeds", "I will not give it any, let it learn to feed itself"])
    jump next

label Wolf1:

    scene street2
    with fade

    "Once upon an afternoon..."

    "In a city crowded as any, hotter than most"

    " A hungry Wolf roamed the aisles looking for little girls to prey on"

    show wolf at left
    with dissolve

    wolf "What won't I give now for some rosemary and lemon roast human..."

    show bunny at right
    with dissolve

    bunny "Bonsoir, Mr. Wolf!"

    wolf "Who are you and what do you want?"

    bunny "I am Bugs Bunny and I like warm hugs."

    bunny "Can you help me and give me a carrot from your orange fur?"
    python:
        make_choice(character = wolf,
            current_scene = current_scene, 
            menu_label = "Bunny",
            prompt = "What should I do?",
            choices = [("Help Bunny", "Help"), ("Ignore Bunny", "Ignore"), ("Eat Bunny", "Eat")],
            reactions = ["Here is a carrot for you, Bugs!", "Go away, skinny Rabbit!", "Well... I have a better idea!"])
    jump next

label Red_Meets_Bunny:
    scene street1
    with fade

    show red at left
    with dissolve

    "Little Red walks and walks, looking for the bus."

    show bunny at right
    with dissolve

    bunny "Bonsoir, little girl!"

    red "Oh look! What a cute bunny! How can I help you bunny?"

    bunny "I am Bugs Bunny and I like warm hugs."

    bunny "Can you help me and give me a carrot from your purse?"

    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Bunny",
            prompt = "What should I do?",
            choices = [("Help Bunny", "Help"), ("Ignore Bunny", "Ignore")], 
            reactions = ["Why of course! Here's a carrot for you, Bugs!", "Silly Bunny, I have more important things to worry about"])
    jump next


label Red_Finds_Bunny_Corpse:
    scene street1
    with fade

    show red at left
    with dissolve

    "Little Red walks and walks, looking for the bus."

    show bunnydead at right
    with dissolve

    red "Oh no! What could possibly be this."

    "Red stares in horror at a bunny's bloodied corpse"

    jump next

label Wolf_Spots_Red_Bunny:
    scene street2red
    with fade

    show wolf at left
    with dissolve

    wolf "Is that?"

    wolf "A HUMAN?!"

    wolf "How good would she taste with a side of coleslaw and a dessert of cinnamon roll?"

    jump next

label Wolf_Spots_Red_NoBunny:
    scene street2red
    with fade

    show wolf at left
    with dissolve

    wolf "Is that?"

    wolf "A HUMAN?!"

    wolf "How good would she taste with a side of coleslaw and a dessert of cinnamon roll?"

    jump next

label Red_Wolf_Meet:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    wolf "Hello, hello, little girl!"

    red "AAAAAAAAA WHAT ARE YOU?"

    wolf "Why, of course, I am Mr. Wolf"

    red "What can I do for you Ms. Wolf"

    wolf "I'd like to cook you!"

    red "AAAAAAAAA"

    jump next

label Bunny_Calls_Hunter:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    show bunny at center
    with dissolve

    bunny "I though I heard a scream"

    red " HE WANTS TO EAT ME!!"

    bunny "Tell me quickly do you want me to call the hunter and rid the world of him for good?"

    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Hunter",
            prompt = "What should I do?",
            choices = [("Call the Hunter", "Call"), ("Give Wolf a second chance", "Ignore")],
            reactions = ["Yes please! Do call the hunter who frees the city from the likes of him!", "NO! Everybody deserves a second chance. Even a wolf."])
    jump next

label Bunny_Makes_Peace:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    show bunny at center
    with dissolve

    bunny "I though I heard a scream"

    red " HE WANTS TO EAT ME!!"

    bunny "Mr. Wolf, I thought you are a good wolf. Be the good wolf I believe you are and spare this girl. I wouldn't imagine she tastes good anyway."

    red "HEY!"

    wolf "Hmmm... You are right. By all means, I'd rather eat at the Cheesecake Factory a few streets down anyway."
    jump next

label Red_Meets_Wolf_Fight:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    python:
        make_choice(character = wolf,
            current_scene = current_scene, 
            menu_label = "Fight-Wolf",
            prompt = "Do I threaten the Wolf?",
            choices = [("Threaten the Wolf", "Yes"), ("Give him a second chance", "No")],
            reactions = ["Take another step, Wolf, and my aunt in the police will make you sorry!", "Everybody deserves a second chance. Even a wolf. Let's  walk to the Cheesecake Factory instead, Mr. Wolf"])

        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Fight-Red",
            prompt = "Do I take another step?",
            choices = [("Yes!", "Yes"), ("Spare the girl, the Cheesecake Factory is probably yummier anyway.", "No")],
            reactions = ["Sorry little girl... fries before guys.", "Well, little girl, I will spare you but do remember you owe me one."])
        
    jump next

label Hunter_Kills_Wolf:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    show bunny
    with dissolve

    show hunter
    with dissolve

    hunter "I come heeding your call, courageous Bunny! Who do you want me to rid this City of!"

    bunny "Rid us of these evil Wolf, good hunter."

    wolf "AAAAAAAAAAA"

    hunter "MWAHAHAHA"

    hide wolf

    show wolfdead at left
    with dissolve

    jump next

label All_Become_Friends:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    wolf "Care to join me at the Cheesecake Factory, little girl?"

    red "It's Red. And of course, why not!"

    wolf "Then let's go, Red"

    red "Maybe we could get to the GRAMMY's after too?"

    jump next

label Wolf_Eats_Red:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    wolf "MWAHAHAHAHAHA"

    red "AAAAAAAAAAAA"

    hide red

    show reddead at right
    with dissolve

    jump next