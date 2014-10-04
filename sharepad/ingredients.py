# name, display_name
ingr_types = [
    ["pizza_base", "Pizza Base"],
    ["extra_cheese", "Extra Cheese"],
    ["meat_fish_and_poultry", "Meat, Fish and Poultry"],
    ["veggies", "Veggies"],
    ["herbs", "Herbs"],
    ["sweets", "Sweets"],
]

# name, display_name, ingr_type
ingredients = [
    # Pizza Base
    ["margherita", "Margherita", "pizza_base"],
    ["mini_margherita", "Mini Margherita", "pizza_base"],
    ["gluten_free", "Gluten Free", "pizza_base"],
    ["wholewheat", "Wholewheat", "pizza_base"],
    ["chakalaka", "Chakalaka", "pizza_base"],
    ["garlic_focaccia", "Garlic Focaccia", "pizza_base"],
    ["cheese_focaccia", "Cheese Focaccia", "pizza_base"],
    ["herb_focaccia", "Herb Focaccia", "pizza_base"],
    ["pizza_wrap", "Pizza Wrap", "pizza_base"],
    ["rosso", "Rosso", "pizza_base"],
    ["nutella", "Nutella", "pizza_base"],

    # Extra Cheese
    ["cheddar", "Cheddar", "extra_cheese"],
    ["feta", "Feta", "extra_cheese"],
    ["gorgonzola", "Gorgonzola", "extra_cheese"],
    ["haloumi", "Haloumi", "extra_cheese"],
    ["mozzarella", "Mozzarella", "extra_cheese"],
    ["mini_mozzarella", "Mini Mozzarella", "extra_cheese"],
    ["parmigiano", "Parmigiano", "extra_cheese"],

    # Fish, Meat and Poultry
    ["anchovies", "Anchovies", "meat_fish_and_poultry"],
    ["bacon", "Bacon", "meat_fish_and_poultry"],
    ["biltong", "Biltong", "meat_fish_and_poultry"],
    ["chourico", "Chourico", "meat_fish_and_poultry"],
    ["egg_x2", "Egg [x2]", "meat_fish_and_poultry"],
    ["ham", "Ham", "meat_fish_and_poultry"],
    ["lamb", "Lamb", "meat_fish_and_poultry"],
    ["mince", "Mince", "meat_fish_and_poultry"],
    ["parma_ham", "Parma Ham", "meat_fish_and_poultry"],
    ["salami", "Salami", "meat_fish_and_poultry"],
    ["spare_ribs", "Spare Ribs", "meat_fish_and_poultry"],
    ["spicy_chicken", "Spicy Chicken", "meat_fish_and_poultry"],
    ["tuna", "Tuna", "meat_fish_and_poultry"],

    # Veggies
    ["almonds_roasted", "Almonds [Roasted]", "veggies"],
    ["artichokes", "Artichokes", "veggies"],
    ["avocado", "Avocado", "veggies"],
    ["baby_marrow", "Baby Marrow", "veggies"],
    ["banana", "Banana", "veggies"],
    ["brinjals", "Brinjals", "veggies"],
    ["capers", "Capers", "veggies"],
    ["caramelised_onions", "Caramelised Onions", "veggies"],
    ["cherry_tomatoes", "Cherry Tomatoes", "veggies"],
    ["green_peppers", "Green Peppers", "veggies"],
    ["jalapenos", "Jalapenos", "veggies"],
    ["mushrooms", "Mushrooms", "veggies"],
    ["olives", "Olives", "veggies"],
    ["onions", "Onions", "veggies"],
    ["peppadews", "Peppadews", "veggies"],
    ["pineapple", "Pineapple", "veggies"],
    ["sesame_seeds", "Sesame Seeds", "veggies",
     ["veggie", "african", "fresh", "fishy", "sweet"]],
    ["spinach", "Spinach", "veggies",
     ["veggie", "fresh", "healthy", "african", "english"]],
    ["sundried_tomatoes", "Sundried Tomatoes", "veggies",
     ["mediterranean", "italian", "fresh", "veggie", "cheezy", "meaty"]],

    # Herbs
    ["basil", "Basil", "herbs", ["italian", "fresh"]],
    ["chillies", "Chillies", "herbs",
     ["spicy", "african", "cheezy", "american", "portuguese", "meaty",
      "veggie", "tropical", "fresh"]],
    ["chives", "Chives", "herbs", ["french", "meaty", "cheezy", "english"]],
    ["coriander", "Coriander", "herbs",
     ["fresh", "healthy", "meaty", "african", "american", "veggie", "spicy"]],
    ["garlic", "Garlic", "herbs",
     ["italian", "french", "american", "fishy", "portuguese", "spicy"]],
    ["roasted_garlic", "Roasted Garlic", "herbs",
     ["cheezy", "italian",  "french", "meaty", "mediterranean", "veggie"]],
    ["rocket", "Rocket", "herbs",
     ["fresh", "american", "healthy", "meaty", "veggie", "spicy"]],
    ["rosemary", "Rosemary", "herbs", ["sweet", "english", "meaty"]],
    ["spring_onions", "Spring Onions", "herbs", ["french", "cheezy", "fishy"]],

    # Sweets
    ["flake", "Flake", "sweets", ["sweet"]],
    ["jelly_tots", "Jelly Tots", "sweets",  ["sweet"]],
    ["marshmallows", "Marshmallows", "sweets", ["sweet"]],
    ["oreo_biscuits", "Oreo Biscuits", "sweets", ["sweet"]],
    ["peppermint_aero", "Peppermint Aero", "sweets", ["sweet"]],
    ["smarties", "Smarties", "sweets", ["sweet"]],
    ["whispers", "Whispers", "sweets", ["sweet"]],
    ["100s_and_1000s", "100's & 1000's", "sweets", ["sweet"]]
]

styles = [
    ["italian", "Italian"],
    ["greek", "Greek"],
    ["portuguese", "Portuguese"],
    ["american", "American"],
    ["french", "French"],
    ["english", "English"],
    ["meaty", "Meaty"],
    ["spicy", "Spicy"],
    ["fresh", "Fresh"],
    ["veggie", "Veggie"],
    ["mediterranean", "Mediterranean"],
    ["african", "African"],
    ["cheesy", "Cheesy"],
    ["tropical", "Tropical"],
    ["healthy", "Healthy"],
    ["wacky", "Wacky"],
    ["fishy", "Fishy"],
    ["sweet", "Sweet"]
]

styles_ingredients = {

    "italian": [
        "margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia",
        "herb_focaccia", "rosso", "gorgonzola", "mozzarella",
        "mini_mozzarella", "parmigiano", "anchovies", "egg_x2", "lamb",
        "mince", "parma_ham", "salami", "tuna", "almonds_roasted",
        "artichokes", "baby_marrow", "capers", "cherry_tomatoes", "mushrooms",
        "olives", "sundried_tomatoes", "basil", "chillies", "chives",
        "coriander", "garlic", "roasted_garlic", "rocket", "rosemary",
        "spring_onions"],

    "greek": [
        "margherita", "mini_margherita", "garlic_focaccia", "herb_focaccia",
        "pizza_wrap", "feta", "haloumi", "mozzarella", "mini_mozzarella",
        "anchovies", "lamb", "mince", "tuna", "almonds_roasted", "artichokes",
        "baby_marrow", "brinjals",  "caramelised_onions", "cherry_tomatoes",
        "olives", "onions", "sesame_seeds", "spinach", "chillies", "chives",
        "coriander", "garlic", "rosemary", "spring_onions"],

    "portuguese": [
        "margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia",
        "herb_focaccia", "mozzarella", "mini_mozzarella", "anchovies",
        "chourico", "egg_x2", "lamb", "parma_ham", "salami", "spicy_chicken",
        "capers", "cherry_tomatoes", "green_peppers", "mushrooms", "olives",
        "onions", "spinach", "sundried_tomatoes", "chillies", "chives",
        "coriander", "garlic", "roasted_garlic", "rocket", "rosemary",
        "spring_onions"],

    "american": [
        "margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia",
        "herb_focaccia", "rosso", "nutella", "cheddar", "mozzarella",
        "mini_mozzarella", "anchovies", "bacon", "ham", "salami", "spare_ribs",
        "avocado", "caramelised_onions", "green_peppers", "jalapenos",
        "mushrooms", "olives", "onions", "basil", "chillies", "chives",
        "coriander", "garlic", "roasted_garlic", "rocket", "spring_onions",
        "marshmallows", "oreo_biscuits"],

    "french": [
        "margherita", "mini_margherita", "gluten_free", "garlic_focaccia",
        "cheese_focaccia", "herb_focaccia", "rosso", "gorgonzola",
        "mozzarella", "mini_mozzarella", "parmigiano", "anchovies",
        "parma_ham", "salami", "tuna", "almonds_roasted", "artichokes",
        "avocado", "baby_marrow", "brinjals", "capers", "cherry_tomatoes",
        "green_peppers", "mushrooms", "onions", "spinach", "chives", "garlic",
        "roasted_garlic", "spring_onions"],

    "english": [
        "margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia",
        "herb_focaccia", "cheddar", "feta", "haloumi", "ham", "bacon",
        "chourico", "almonds_roasted", "artichokes", "avocado", "baby_marrow",
        "brinjals", "capers", "caramelised_onions", "cherry_tomatoes",
        "green_peppers", "mushrooms", "olives", "spinach", "sundried_tomatoes",
        "basil", "chives", "coriander", "rocket", "rosemary"],

    "meaty": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "mozzarella", "mini_mozzarella", "parmigiano", "bacon", "biltong",
        "chourico", "ham", "lamb", "mince", "parma_ham", "salami",
        "spare_ribs", "spicy_chicken", "almonds_roasted", "capers",
        "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos",
        "mushrooms", "olives", "onions", "peppadews", "pineapple",
        "sesame_seeds", "spinach", "chives", "coriander", "garlic",
        "roasted_garlic", "rocket", "rosemary", "spring_onions"],

    "spicy": [
        "margherita", "mini_margherita", "chakalaka", "garlic_focaccia",
        "herb_focaccia", "pizza_wrap", "nutella", "haloumi", "mozzarella",
        "mini_mozzarella", "chourico", "egg_x2", "mince", "salami",
        "spare_ribs", "spicy_chicken", "avocado", "banana", "brinjals",
        "green_peppers", "jalapenos", "mushrooms", "olives", "onions",
        "peppadews", "pineapple", "chillies", "chives", "coriander", "garlic",
        "roasted_garlic", "rocket", "rosemary", "spring_onions"],

    "fresh": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia",
        "pizza_wrap", "rosso", "feta", "haloumi", "mozzarella",
        "mini_mozzarella", "egg_x2", "ham", "parma_ham", "spare_ribs",
        "spicy_chicken", "artichokes", "avocado", "baby_marrow", "banana",
        "brinjals", "capers", "cherry_tomatoes", "green_peppers", "jalapenos",
        "mushrooms", "olives", "onions", "peppadews", "pineapple",
        "sesame_seeds", "spinach", "basil", "chillies", "chives", "coriander",
        "garlic", "rocket", "rosemary", "spring_onions"],

    "veggie": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia",
        "pizza_wrap", "rosso", "feta", "haloumi", "mozzarella",
        "mini_mozzarella", "parmigiano", "anchovies", "bacon", "biltong",
        "chourico", "almonds_roasted", "artichokes", "avocado", "baby_marrow",
        "banana", "brinjals", "capers", "caramelised_onions",
        "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives",
        "onions", "peppadews", "pineapple", "sesame_seeds", "spinach",
        "sundried_tomatoes", "basil", "chillies", "chives", "coriander",
        "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],

    "mediterranean": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "garlic_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta",
        "gorgonzola", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano",
        "anchovies", "lamb", "mince", "parma_ham", "salami", "tuna",
        "almonds_roasted", "artichokes", "baby_marrow", "brinjals", "capers",
        "green_peppers", "olives", "sesame_seeds", "sundried_tomatoes",
        "basil", "garlic", "roasted_garlic", "rosemary"],

    "african": [
        "margherita", "mini_margherita", "chakalaka", "cheddar", "feta",
        "haloumi", "mozzarella", "mini_mozzarella", "biltong", "lamb", "mince",
        "spare_ribs", "spicy_chicken", "avocado", "banana", "onions",
        "peppadews", "sesame_seeds", "spinach", "sundried_tomatoes", "basil",
        "chillies", "chives", "coriander", "garlic", "roasted_garlic",
        "rocket"],

    "cheesy": [
        "margherita", "mini_margherita", "chakalaka", "garlic_focaccia",
        "cheese_focaccia", "herb_focaccia", "cheddar", "feta", "gorgonzola",
        "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "bacon",
        "biltong", "chourico", "ham", "lamb", "mince", "parma_ham", "salami",
        "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers",
        "jalapenos", "peppadews", "spinach", "sundried_tomatoes", "basil",
        "chives", "garlic", "roasted_garlic", "rocket", "spring_onions"],

    "tropical": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia",
        "pizza_wrap", "mozzarella", "mini_mozzarella", "bacon", "chourico",
        "ham", "lamb", "spicy_chicken", "avocado", "banana", "cherry_tomatoes",
        "green_peppers", "jalapenos", "onions", "peppadews", "pineapple",
        "spinach", "chillies", "chives", "coriander"],

    "healthy": [
        "mini_margherita", "gluten_free", "wholewheat", "chakalaka",
        "garlic_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta",
        "gorgonzola", "haloumi", "mini_mozzarella", "egg_x2", "ham", "lamb",
        "parma_ham", "spare_ribs", "spicy_chicken", "tuna", "almonds_roasted",
        "artichokes", "avocado", "baby_marrow", "banana", "brinjals", "capers",
        "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos",
        "mushrooms", "olives", "onions", "peppadews", "pineapple",
        "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chillies",
        "chives", "coriander", "garlic", "roasted_garlic", "rocket",
        "rosemary", "spring_onions"],

    "fishy": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia",
        "pizza_wrap", "rosso", "feta", "gorgonzola", "haloumi", "mozzarella",
        "mini_mozzarella", "parmigiano", "anchovies", "tuna",
        "almonds_roasted", "artichokes", "avocado", "baby_marrow", "brinjals",
        "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers",
        "olives", "onions", "peppadews", "pineapple", "sesame_seeds",
        "spinach", "sundried_tomatoes", "basil", "chives", "coriander",
        "garlic", "rocket", "spring_onions"],

    "sweet": [
        "margherita", "mini_margherita", "gluten_free", "wholewheat",
        "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia",
        "pizza_wrap", "rosso", "nutella", "cheddar", "feta", "gorgonzola",
        "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies",
        "bacon", "biltong", "chourico", "egg_x2", "ham", "lamb", "mince",
        "parma_ham", "salami", "spare_ribs", "spicy_chicken", "tuna",
        "almonds_roasted", "artichokes", "avocado", "baby_marrow", "banana",
        "brinjals", "capers", "caramelised_onions", "cherry_tomatoes",
        "green_peppers", "jalapenos", "mushrooms", "olives", "onions",
        "peppadews", "pineapple", "sesame_seeds", "spinach",
        "sundried_tomatoes", "basil", "chillies", "chives", "coriander",
        "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions",
        "flake", "jelly_tots", "marshmallows", "oreo_biscuits",
        "peppermint_aero", "smarties", "whispers", "100s_and_1000s"],
}
