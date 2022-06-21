# type: ignore

define red = Character('Red Riding Hood')
define wolf = Character('Wolf')
define bird = Character('Bird')
define hunter = Character('Hunter')
define bunny = Character('Bunny')

image red_reversed = im.Flip("red.png", horizontal="True")
image bunny_reversed = im.Flip("bunny.png", horizontal="True")

label Red1:
    play music "illurock.opus"

    scene street1
    with fade

    "Once upon an afternoon..."

    "In a city crowded as any, hotter than most"

    "Little Red lost her way on her way to the GRAMMYs..."

    show red_reversed at left
    with dissolve

    red "Oh no! It appears that I am lost!"

    red "I must find my way to the bus station and find it fast!"

    "So Red was set to find her way. She looked around for any signs of a bus. Except..."

    show bird at right
    with dissolve

    red "Oh look at that! It's a cute bird!"

    bird "Ew. An ugly human!"

    python:
        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Bird",
            prompt = "Do I call the bird ugly back?",
            choices = [("Let the poor bird go", "Give"), ("Make the rude bird sorry", "Ignore")],
            reactions = ["That's unkind of you, little bird. Please excuse me.", "YOU ARE UGLY! FLY AWAY UGLY CREATURE!"])
    jump next

label Wolf1:

    play music "illurock.opus"

    scene street2
    with fade

    "Once upon an afternoon..."

    "In a city crowded as any, hotter than most"

    " A hungry Wolf roamed the aisles looking for little girls to prey on"

    show wolf at left
    with dissolve

    wolf "What won't I give now for some rosemary and lemon roast human..."

    show bunny_reversed at right
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
            reactions = ["Here is a carrot for you, Bugs!", "Go away, skinny Rabbit!", "Well... I have a better idea! RAWR!!!"])
    jump next

label Red_Meets_Bunny:
    scene street1
    with fade

    show red_reversed at left
    with dissolve

    "Little Red walks and walks, looking for the bus."

    show bunny_reversed at right
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

    show red_reversed at left
    with dissolve

    "Little Red walks and walks, looking for the bus."

    show bunnydead
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

    red "What can I do for you Mr. Wolf"

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

    show bunny0 at center
    with dissolve

    bunny "I thought I heard a scream"

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

    show bunny0 at center
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

    wolf "Stop screaming, little girl! I have a headache!"

    python:
        make_choice(character = wolf,
            current_scene = current_scene, 
            menu_label = "Fight-Wolf",
            prompt = "Do I attack the little girl?",
            choices = [("Attack the girl", "Yes"), ("Spare the girl, the Cheesecake Factory is probably yummier anyway.", "No")],
            reactions = ["Get ready to enter my tummy, little girl. RAAWR!", "Well, little girl, I will spare you but do remember you owe me one."])

        make_choice(character = red,
            current_scene = current_scene, 
            menu_label = "Fight-Red",
            prompt = "Do I threaten the Wolf?",
            choices = [("Yes. Scare him away!", "Yes"), ("Everybody deserves a second chance. Even a wolf.", "No")],
            reactions = ["Take another step, Wolf, and my hunter friend will make you sorry!", "Let me buy you food at the Cheesecake Factory instead, Mr. Wolf"])


    jump next

label Hunter_Kills_Wolf:

    scene street2
    with fade

    show wolf at left
    with dissolve

    show red at right
    with dissolve

    show hunter
    with dissolve

    hunter "I come heeding your call, little girl! Who do you want me to rid this City of!"

    red "Rid us of this evil Wolf, good hunter."

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

    red "Maybe we could also go to the GRAMMY's later?"

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