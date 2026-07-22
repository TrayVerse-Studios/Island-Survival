from tkinter import *
from random import *
from time import sleep, time

debug = False

def update_health(current_health):
    global health, alive
    current_health = max(0, min(current_health, 100))
    health = current_health
    bar_width = (current_health / 100) * 200
    healthbar.coords(health_bar, 0, 0, bar_width, 25)
    hp.config(text = f"Health: {current_health}%")
    if current_health == 0:
        alive = False

def update_stamina(current_stamina):
    global stamina
    current_stamina = max(0, min(current_stamina, 100))
    stamina = current_stamina
    bar_width = (current_stamina / 100) * 200
    staminabar.coords(stamina_bar, 0, 0, bar_width, 25)
    sp.config(text = f"Stamina: {current_stamina}%")

def take_damage(num=10):
    global health
    health -= num
    update_health(health)

def heal(num=10):
    global health
    health += num
    update_health(health)
    
def tire(num=10):
    global stamina
    stamina -= num
    update_stamina(stamina)

def recharge(num=10):
    global stamina
    stamina += num
    update_stamina(stamina)

def get_best_tools():
    global best_pickaxe, best_axe, best_sword
    if inventory.get("galaxium_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "galaxium_pickaxe"
    elif inventory.get("ruby_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "ruby_pickaxe"
    elif inventory.get("diamond_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "diamond_pickaxe"
    elif inventory.get("iron_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "iron_pickaxe"
    elif inventory.get("stone_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "stone_pickaxe"
    elif inventory.get("wooden_pickaxe", {}).get("quantity", 0) > 0:
        best_pickaxe = "wooden_pickaxe"
    else:
        best_pickaxe = None
    if inventory.get("galaxium_axe", {}).get("quantity", 0) > 0:
        best_axe = "galaxium_axe"
    elif inventory.get("ruby_axe", {}).get("quantity", 0) > 0:
        best_axe = "ruby_axe"
    elif inventory.get("diamond_axe", {}).get("quantity", 0) > 0:
        best_axe = "diamond_axe"
    elif inventory.get("iron_axe", {}).get("quantity", 0) > 0:
        best_axe = "iron_axe"
    elif inventory.get("stone_axe", {}).get("quantity", 0) > 0:
        best_axe = "stone_axe"
    elif inventory.get("wooden_axe", {}).get("quantity", 0) > 0:
        best_axe = "wooden_axe"
    else:
        best_axe = None
    if inventory.get("galaxium_sword", {}).get("quantity", 0) > 0:
        best_sword = "galaxium_sword"
    elif inventory.get("ruby_sword", {}).get("quantity", 0) > 0:
        best_sword = "ruby_sword"
    elif inventory.get("diamond_sword", {}).get("quantity", 0) > 0:
        best_sword = "diamond_sword"
    elif inventory.get("iron_sword", {}).get("quantity", 0) > 0:
        best_sword = "iron_sword"
    elif inventory.get("stone_sword", {}).get("quantity", 0) > 0:
        best_sword = "stone_sword"
    elif inventory.get("wooden_sword", {}).get("quantity", 0) > 0:
        best_sword = "wooden_sword"
    else:
        best_sword = None
    if debug:
        print(f"Best Pickaxe: {best_pickaxe}")
        print(f"Best axe: {best_axe}")
        print(f"Best sword: {best_sword}")

def durability_check():
    for item in inventory:
        if item in durability_template:
            if inventory[item]["durability"] <= 0:
                inventory[item]["quantity"] -= 1
                if inventory[item]["quantity"] <= 0:
                    del inventory[item]
                else:
                    inventory[item]["durability"] = durability_template[item]
                event_msg(f"Your {item.replace('_', ' ').capitalize()} broke!")
    get_best_tools()

def get_scavenge_chances():
    """Return the chance table that applies right now (base + any owned tools)."""
    chances = scavenge_chance["base"].copy()

    if best_pickaxe:
        for item, ch in scavenge_chance[best_pickaxe].items():
            chances[item] = max(chances.get(item, 0), ch)
    if best_axe:
        for item, ch in scavenge_chance[best_axe].items():
            chances[item] = max(chances.get(item, 0), ch)
    if debug:
        print(f"Chances: {chances}")
    return chances

def event_msg(msg, font=("Arial", 16), duration=2000):
    event = Label(game, text=msg, font=font, wraplength=300)
    event.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    if duration > 0:
        game.after(duration, event.destroy)
    else:
        game.wait_variable(wait_var)
        event.destroy()

def invsee():
    if not inventory:
        event_msg("Your inventory is empty.")
        return

    inv_win = Toplevel(game)
    inv_win.title("Inventory")
    inv_win.geometry("650x500")
    inv_win.transient(game)
    inv_win.grab_set()

    # ── Left side: scrollable list of item buttons ──────────────────
    left = Frame(inv_win)
    left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    canvas = Canvas(left, width=220, highlightthickness=0)
    scrollbar = Scrollbar(left, orient=VERTICAL, command=canvas.yview)
    button_frame = Frame(canvas)

    button_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # ── Right side: item details ────────────────────────────────────
    right = Frame(inv_win, padx=25, pady=20)
    right.pack(side=RIGHT, fill=BOTH, expand=True)

    title_lbl = Label(right, text="Select an item", font=("Arial", 18, "bold"))
    title_lbl.pack(anchor="w", pady=(0, 15))

    qty_lbl = Label(right, text="", font=("Arial", 14))
    qty_lbl.pack(anchor="w")

    dur_lbl = Label(right, text="", font=("Arial", 14))
    dur_lbl.pack(anchor="w", pady=(8, 0))

    nutrition_lbl = Label(right, text="", font=("Arial", 14))
    nutrition_lbl.pack(anchor="w", pady=(8, 0))

    damage_lbl = Label(right, text="", font=("Arial", 14))   # ← new
    damage_lbl.pack(anchor="w", pady=(8, 0))

    extra_lbl = Label(right, text="", font=("Arial", 12), fg="gray", justify=LEFT)
    extra_lbl.pack(anchor="w", pady=(15, 0))

    # Create the Eat button ONCE (it will be shown/hidden as needed)
    eat_btn = Button(right, text="Eat", font=("Arial", 12), width=10)

    def eat_item(item_key):
        if item_key not in inventory:
            return

        data = inventory[item_key]
        nutrition = data["nutrition"]
        name = data["name"]

        recharge(nutrition)

        # 30% chance of getting sick from raw food
        if item_key.startswith("raw_") and randint(1, 100) <= 30:
            event_msg(f"You ate {name}. It restored {nutrition} stamina, but you feel a bit sick.")
            take_damage(5)
        else:
            event_msg(f"You ate {name} and restored {nutrition} stamina.")

        # Consume one
        data["quantity"] -= 1
        if data["quantity"] <= 0:
            del inventory[item_key]
            # Clear the details panel
            title_lbl.config(text="Select an item")
            qty_lbl.config(text="")
            dur_lbl.config(text="")
            nutrition_lbl.config(text="")
            damage_lbl.config(text="")
            extra_lbl.config(text="")
            eat_btn.pack_forget()
        else:
            show_details(item_key)   # refresh the numbers

    def show_details(item_key):
        if item_key not in inventory:
            return

        data = inventory[item_key]
        title_lbl.config(text=data["name"])
        qty_lbl.config(text=f"Quantity: {data['quantity']}")

        # Durability
        if "durability" in data:
            max_dur = durability_template.get(item_key, "?")
            dur_lbl.config(text=f"Durability: {data['durability']} / {max_dur}")
        else:
            dur_lbl.config(text="")

        # Nutrition
        if "nutrition" in data:
            nutrition_lbl.config(text=f"Nutrition: {data['nutrition']}")
        else:
            nutrition_lbl.config(text="")

        # Attack damage (swords)
        if item_key in damage_template:
            damage_lbl.config(text=f"Attack Damage: {damage_template[item_key]}")
        else:
            damage_lbl.config(text="")

        # Show or hide the Eat button
        eat_btn.pack_forget()
        if data.get("edible", False):
            eat_btn.config(command=lambda k=item_key: eat_item(k))
            eat_btn.pack(anchor="w", pady=(10, 0))

        # Flavour text
        if item_key.endswith(("_pickaxe", "_axe")):
            extra_lbl.config(text="This is a tool.\nIt loses durability when used.")
        elif item_key.endswith("_sword"):
            extra_lbl.config(text="This is a weapon.\nIt can be used in combat.")
        else:
            extra_lbl.config(text="")

    # Create one button for every item currently in the inventory
    for item_key in sorted(inventory.keys()):
        name = inventory[item_key]["name"]
        btn = Button(
            button_frame,
            text=name,
            width=22,
            anchor="w",
            font=("Arial", 11),
            command=lambda k=item_key: show_details(k)
        )
        btn.pack(fill=X, pady=2)

    Button(inv_win, text="Close", font=("Arial", 12), width=12,
           command=inv_win.destroy).pack(side=BOTTOM, pady=12)

    if debug:
        print(f"Inventory: {inventory}")

def scavenge():
    global inventory
    if stamina < 10:
        event_msg("You are too tired to scavenge. You need to rest.")
    else:
        chances = get_scavenge_chances()
        found = {}
        count = 0
        while count < 10:
            for item, chance in chances.items():
                if randint(1, 2) == 1:
                    pass
                else:
                    if randint(1, 1000) <= chance * 1000:
                        inventory.update({item: {"name": item.replace('_', ' ').capitalize(), "quantity": inventory.get(item, {}).get("quantity", 0) + 1}})
                        if item in durability_template:
                            inventory[item]["durability"] = randint(1, durability_template[item])
                        if item in food_template:
                            inventory[item]["edible"] = True
                            inventory[item]["nutrition"] = food_template[item]
                        else:
                            inventory[item]["edible"] = False
                        found[item] = found.get(item, 0) + 1
                    count += 1
                    if randint(1, 2) == 1:
                        if best_pickaxe and item in scavenge_chance[best_pickaxe]:
                            inventory[best_pickaxe]["durability"] -= 1
                        if best_axe and item in scavenge_chance[best_axe]:
                            inventory[best_axe]["durability"] -= 1
                    durability_check()
        if found:
            lines = [f"{qty} × {item.replace('_', ' ').capitalize()}" for item, qty in found.items()]
            msg = "You found:\n" + "\n".join(lines)
            event_msg(msg)
        else:
            event_msg("You found nothing while scavenging.")
        tire(10)
        get_best_tools()
        if debug:
            print(f"Found: {found}")

def crafting():
    craft_win = Toplevel(game)
    craft_win.title("Crafting")
    craft_win.geometry("750x550")
    craft_win.transient(game)
    craft_win.grab_set()

    # ── Left side: scrollable recipe list ───────────────────────────
    left = Frame(craft_win)
    left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    canvas = Canvas(left, width=230, highlightthickness=0)
    scrollbar = Scrollbar(left, orient=VERTICAL, command=canvas.yview)
    button_frame = Frame(canvas)

    button_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=button_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # ── Right side: details ─────────────────────────────────────────
    right = Frame(craft_win, padx=25, pady=15)
    right.pack(side=RIGHT, fill=BOTH, expand=True)

    title_lbl = Label(right, text="Select a recipe", font=("Arial", 18, "bold"))
    title_lbl.pack(anchor="w", pady=(0, 8))

    produces_lbl = Label(right, text="", font=("Arial", 13))
    produces_lbl.pack(anchor="w")

    ingredients_lbl = Label(right, text="", font=("Arial", 12), justify=LEFT)
    ingredients_lbl.pack(anchor="w", pady=(12, 0))

    req_lbl = Label(right, text="", font=("Arial", 12))
    req_lbl.pack(anchor="w", pady=(10, 0))

    status_lbl = Label(right, text="", font=("Arial", 12, "bold"))
    status_lbl.pack(anchor="w", pady=(12, 0))

    # Craft button – created once, shown/hidden as needed
    craft_btn = Button(right, text="Craft", font=("Arial", 13), width=12)

    def can_craft(recipe_key):
        recipe = crafting_recipes[recipe_key]

        # Check requirement (workbench / furnace etc.)
        req = recipe["requirements"]
        if req is not None:
            if inventory.get(req, {}).get("quantity", 0) <= 0:
                return False, f"Missing requirement: {req.replace('_', ' ').capitalize()}"

        # Check ingredients
        missing = []
        for item, needed in recipe["ingredients"].items():
            owned = inventory.get(item, {}).get("quantity", 0)
            if owned < needed:
                missing.append(f"{item.replace('_', ' ')} ({owned}/{needed})")

        if missing:
            return False, "Missing: " + ", ".join(missing)

        return True, "Ready to craft!"

    def do_craft(recipe_key):
        recipe = crafting_recipes[recipe_key]

        # 1. Remove ingredients
        for item, needed in recipe["ingredients"].items():
            inventory[item]["quantity"] -= needed
            if inventory[item]["quantity"] <= 0:
                del inventory[item]

        # 2. Add the crafted item(s)
        result = recipe_key
        amount = recipe["quantity"]

        if result not in inventory:
            inventory[result] = {
                "name": result.replace('_', ' ').capitalize(),
                "quantity": 0,
                "edible": False
            }
            # Tools
            if result in durability_template:
                inventory[result]["durability"] = durability_template[result]
            # Food
            if result in food_template:
                inventory[result]["edible"] = True
                inventory[result]["nutrition"] = food_template[result]

        inventory[result]["quantity"] += amount

        get_best_tools()          # in case a better tool was just crafted
        event_msg(f"Crafted {amount} × {inventory[result]['name']}")
        show_details(recipe_key)  # refresh the panel

    def show_details(recipe_key):
        recipe = crafting_recipes[recipe_key]
        nice_name = recipe_key.replace('_', ' ').capitalize()

        title_lbl.config(text=nice_name)
        produces_lbl.config(text=f"Produces: {recipe['quantity']} × {nice_name}")

        # Build ingredients text with owned / needed
        lines = ["Ingredients:"]
        for item, needed in recipe["ingredients"].items():
            owned = inventory.get(item, {}).get("quantity", 0)
            status = "✓" if owned >= needed else "✗"
            lines.append(f"  {status}  {item.replace('_', ' ').capitalize()}: {owned} / {needed}")
        ingredients_lbl.config(text="\n".join(lines))

        # Requirement
        req = recipe["requirements"]
        if req is None:
            req_lbl.config(text="Requirement: None")
        else:
            owned_req = inventory.get(req, {}).get("quantity", 0)
            mark = "✓" if owned_req > 0 else "✗"
            req_lbl.config(text=f"Requirement: {mark}  {req.replace('_', ' ').capitalize()}")

        # Can we craft?
        possible, message = can_craft(recipe_key)
        status_lbl.config(text=message, fg="green" if possible else "red")

        # Show / hide the Craft button
        craft_btn.pack_forget()
        if possible:
            craft_btn.config(command=lambda: do_craft(recipe_key))
            craft_btn.pack(anchor="w", pady=(15, 0))

    # Create a button for every recipe
    for recipe_key in sorted(crafting_recipes.keys()):
        name = recipe_key.replace('_', ' ').capitalize()
        btn = Button(
            button_frame,
            text=name,
            width=24,
            anchor="w",
            font=("Arial", 11),
            command=lambda k=recipe_key: show_details(k)
        )
        btn.pack(fill=X, pady=2)

    # Close button
    Button(craft_win, text="Close", font=("Arial", 12), width=12,
           command=craft_win.destroy).pack(side=BOTTOM, pady=12)
    get_best_tools()

def proceed():
    wait_var.set(True)

def roll_event():
    global inventory
    roll = randint(1, 10)
    if roll == 1:
        event_msg("A storm hits the island! You lose 10 health.", font=("Arial", 16, "bold"))
        take_damage(10)
    elif roll == 2:
        event_msg("You found a hidden stash of food! You gain 20 stamina.", font=("Arial", 16, "bold"))
        recharge(20)
    elif roll == 3:
        event_win = Toplevel(game)
        event_win.title("Event")
        event_win.geometry("750x550")
        event_win.transient(game)
        event_win.grab_set()

        def opt1():
            rand = randint(1, 3)
            if rand == 1:
                chances = get_scavenge_chances()
                found = {}
                count = 0
                while count < 10:
                    for item, chance in chances.items():
                        if randint(1, 2) == 1:
                            pass
                        else:
                            if randint(1, 1000) <= chance * 1000:
                                inventory.update({item: {"name": item.replace('_', ' ').capitalize(), "quantity": inventory.get(item, {}).get("quantity", 0) + 1}})
                                if item in durability_template:
                                    inventory[item]["durability"] = randint(1, durability_template[item])
                                if item in food_template:
                                    inventory[item]["edible"] = True
                                    inventory[item]["nutrition"] = food_template[item]
                                else:
                                    inventory[item]["edible"] = False
                                found[item] = found.get(item, 0) + 1
                            count += 1
                if found:
                    lines = [f"{qty} × {item.replace('_', ' ').capitalize()}" for item, qty in found.items()]
                    event_msg("You successfully raided the village and found some valuable resources! You found:\n" + "\n".join(lines), font=("Arial", 16, "bold"))
                else:
                    event_msg("You roamed the village undetected, but found nothing.", font=("Arial", 16, "bold"))
            elif rand == 2:
                if (not best_sword == "wooden_sword") and (not best_sword == "stone_sword"):
                    chances = get_scavenge_chances()
                    found = {}
                    count = 0
                    while count < 10:
                        for item, chance in chances.items():
                            if randint(1, 2) == 1:
                                pass
                            else:
                                if randint(1, 1000) <= chance * 1000:
                                    inventory.update({item: {"name": item.replace('_', ' ').capitalize(), "quantity": inventory.get(item, {}).get("quantity", 0) + 1}})
                                    if item in durability_template:
                                       inventory[item]["durability"] = randint(1, durability_template[item])
                                    if item in food_template:
                                        inventory[item]["edible"] = True
                                        inventory[item]["nutrition"] = food_template[item]
                                    else:
                                       inventory[item]["edible"] = False
                                    found[item] = found.get(item, 0) + 1
                                count += 1
                    if found:
                        lines = [f"{qty} × {item.replace('_', ' ').capitalize()}" for item, qty in found.items()]
                        event_msg("The villagers caught you raiding their village and retaliated, but you fought back. You lose 5 health, but keep some resources. You found:\n" + "\n".join(lines), font=("Arial", 16, "bold"))
                    else:
                        event_msg("The villagers caught you raiding their village and retaliated, but you fought back. You lose 5 health.", font=("Arial", 16, "bold"))
                    take_damage(5)
                else:
                    event_msg("The villagers caught you raiding their village and retaliated! You lose 20 health.", font=("Arial", 16, "bold"))
                    take_damage(20)
            else:
                event_msg("You were unsuccessful in your raid and had to flee the village.", font=("Arial", 16, "bold"))
            event_win.destroy()
        def opt2():
            event_msg("You decide to leave the village alone and continue your journey.", font=("Arial", 16, "bold"))
            event_win.destroy()

        event = Label(event_win, text="While exploring the island, you stumble upon a small village. It seems to be well-established.", font=("Arial", 20, "bold"), wraplength=300)
        event.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        option1 = Button(event_win, text="Raid the village", font=("Arial", 16), width=20, command=opt1)
        option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
        option2 = Button(event_win, text="Leave the village alone", font=("Arial", 16), width=20, command=opt2)
        option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)


crafting_recipes = {
    "wooden_log": {
        "ingredients": {"stick": 4},
        "requirements": None,
        "quantity": 1
    },
    "wooden_plank": {
        "ingredients": {"wooden_log": 1},
        "requirements": None,
        "quantity": 4
    },
    "crafting_bench": {
        "ingredients": {"wooden_plank": 4},
        "requirements": None,
        "quantity": 1
    },
    "furnace": {
        "ingredients": {"rock": 8},
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "stick": {
        "ingredients": {"wooden_log": 1},
        "requirements": None,
        "quantity": 4
    },
    "wooden_pickaxe": {
        "ingredients": {
            "wooden_log": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "wooden_axe": {
        "ingredients": {
            "wooden_log": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "wooden_sword": {
        "ingredients": {
            "wooden_log": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "stone_pickaxe": {
        "ingredients": {
            "rock": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "stone_axe": {
        "ingredients": {
            "rock": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "stone_sword": {
        "ingredients": {
            "rock": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "iron_pickaxe": {
        "ingredients": {
            "iron_ingot": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "iron_axe": {
        "ingredients": {
            "iron_ingot": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "iron_sword": {
        "ingredients": {
            "iron_ingot": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "diamond_pickaxe": {
        "ingredients": {
            "diamond": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "diamond_axe": {
        "ingredients": {
            "diamond": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "diamond_sword": {
        "ingredients": {
            "diamond": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "ruby_pickaxe": {
        "ingredients": {
            "ruby": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "ruby_axe": {
        "ingredients": {
            "ruby": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "ruby_sword": {
        "ingredients": {
            "ruby": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "galaxium_pickaxe": {
        "ingredients": {
            "galaxium": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "galaxium_axe": {
        "ingredients": {
            "galaxium": 1,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "galaxium_sword": {
        "ingredients": {
            "galaxium": 2,
            "stick": 1,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "cooked_meat": {
        "ingredients": {
            "raw_meat": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 2
    },
    "iron_ingot": {
        "ingredients": {
            "iron_ore": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 2
    },
    "copper_ingot": {
        "ingredients": {
            "copper_ore": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 2
    },
    "wire": {
        "ingredients": {
            "copper_ingot": 1,
            "rubber": 1
        },
        "requirements": "crafting_bench",
        "quantity": 5
    },
    "circuit": {
        "ingredients": {
            "wire": 2,
            "copper_ingot": 1,
            "iron_ingot": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "receiver": {
        "ingredients": {
            "circuit": 1,
            "wire": 2,
            "iron_ingot": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "transmitter": {
        "ingredients": {
            "circuit": 1,
            "wire": 2,
            "iron_ingot": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "radio": {
        "ingredients": {
            "receiver": 1,
            "transmitter": 1,
            "circuit": 1,
            "wire": 2,
            "battery": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "battery": {
        "ingredients": {
            "iron_ingot": 1,
            "copper_ingot": 1,
            "lemon": 1,
            "iron_ingot": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "diamond": {
        "ingredients": {
            "diamond_ore": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 1
    },
    "ruby": {
        "ingredients": {
            "ruby_ore": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 1
    },
    "galaxium": {
        "ingredients": {
            "galaxium_ore": 2,
            "wooden_log": 1
        },
        "requirements": "furnace",
        "quantity": 1
    }
}
food_template = {
    "apple": 5,
    "raw_meat": 15,
    "cooked_meat": 25,
    "lemon": 5
}
damage_template ={
    "wooden_sword": 2,
    "stone_sword": 5,
    "iron_sword": 15,
    "diamond_sword": 25,
    "ruby_sword": 50,
    "galaxium_sword": 200
}
durability_template = {
    "wooden_axe": 20,
    "wooden_pickaxe": 20,
    "wooden_sword": 20,
    "stone_pickaxe": 50,
    "stone_axe": 50,
    "stone_sword": 50,
    "iron_pickaxe": 75,
    "iron_axe": 75,
    "iron_sword": 75,
    "diamond_pickaxe": 150,
    "diamond_axe": 150,
    "diamond_sword": 150,
    "ruby_pickaxe": 250,
    "ruby_axe": 250,
    "ruby_sword": 250,
    "galaxium_pickaxe": 500,
    "galaxium_axe": 500,
    "galaxium_sword": 500
}
day = 0
scavenge_chance = {
    "base": {
        "rock": 0.2,
        "stick": 0.3,
        "vine": 0.3,
        "apple": 0.15,
        "lemon": 0.15,
        "raw_meat": 0.1,
        "wooden_pickaxe": 0.02,
        "wooden_axe": 0.02,
        "stone_pickaxe": 0.01,
        "stone_axe": 0.01
    },
    "wooden_axe": {
        "stick": 0.5,
        "vine": 0.5,
        "apple": 0.3,
        "lemon": 0.3,
        "wooden_log": 0.5
    },
    "wooden_pickaxe": {
        "rock": 0.5
    },
    "stone_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.02
    },
    "stone_axe": {
        "stick": 0.55,
        "vine": 0.5,
        "apple": 0.3,
        "lemon": 0.3,
        "wooden_log": 0.6,
        "rubber": 0.02
    },
    "iron_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.1,
        "diamond": 0.02,
        "copper_ore": 0.05
    },
    "iron_axe": {
        "stick": 0.6,
        "vine": 0.51,
        "apple": 0.32,
        "lemon": 0.32,
        "wooden_log": 0.6,
        "rubber": 0.05
    },
    "diamond_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.2,
        "diamond_ore": 0.1,
        "ruby_ore": 0.02,
        "copper_ore": 0.1
    },
    "diamond_axe": {
        "stick": 0.7,
        "vine": 0.6,
        "apple": 0.5,
        "lemon": 0.5,
        "wooden_log": 0.7,
        "rubber": 0.1
    },
    "ruby_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.5,
        "diamond_ore": 0.2,
        "ruby_ore": 0.1,
        "copper_ore": 0.2
    },
    "ruby_axe": {
        "stick": 0.85,
        "vine": 0.7,
        "apple": 0.5,
        "lemon": 0.5,
        "wooden_log": 0.85,
        "rubber": 0.2
    },
    "galaxium_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.8,
        "diamond_ore": 0.5,
        "ruby_ore": 0.2,
        "copper_ore": 0.5
    },
    "galaxium_axe": {
        "stick": 1,
        "vine": 0.8,
        "apple": 0.6,
        "lemon": 0.6,
        "wooden_log": 1,
        "rubber": 0.5
    }
}
health = 100
stamina = 100
inventory = {}
game = Tk()
game.title("Island Survival")
game.geometry('1920x1080')
game.state('zoomed')
wait_var = BooleanVar(value=False)

menubar = Menu(game)
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label ='Save', command = None)
file.add_command(label ='Load Save', command = None)
menubar.add_command(label ='Quit', command = game.destroy)

advance = Button(game, text="Advance", command=proceed, font=("Arial", 20, "bold"))
advance.place(relx = 0.5, rely = 0.95, anchor = CENTER)

event = Label(game, text="Welcome!", font=("Arial", 20, "bold"), wraplength=300)
event.place(relx = 0.5, rely = 0.5, anchor = CENTER)
game.wait_variable(wait_var)
event.destroy()
event_msg(msg="You find yourself on a desert island with no supplies or memory of how you got there.", font=("Arial", 16), duration=0)
event_msg(msg="Now, you have only one goal…", font=("Arial", 16), duration=0)
event_msg(msg="SURVIVE", font=("Arial", 20, "bold"), duration=0)

game.config(menu = menubar)

healthbar = Canvas(game, width=200, height=25, bg="red", highlightthickness=0)
healthbar.place(relx = 0.18, rely = 0.05, anchor = "w")
health_bar = healthbar.create_rectangle(0, 0, 200, 25, fill="green", width=0)
hp = Label(game, text = f"Health: {health}%", font=("Arial", 20, "bold"))
hp.place(relx = 0, rely = 0.05, anchor = "w")

staminabar = Canvas(game, width=200, height=25, bg="blue", highlightthickness=0)
staminabar.place(relx = 0.18, rely = 0.1, anchor = "w")
stamina_bar = staminabar.create_rectangle(0, 0, 200, 25, fill="yellow", width=0)
sp = Label(game, text = f"Stamina: {stamina}%", font=("Arial", 20, "bold"))
sp.place(relx = 0, rely = 0.1, anchor = "w")

scav = Button(game, text="Scavenge", command=scavenge, font=("Arial", 20, "bold"))
scav.place(relx = 1, rely = 0.05, anchor = "e")

inv = Button(game, text="Inventory", command=invsee, font=("Arial", 20, "bold"))
inv.place(relx = 1, rely = 0.15, anchor = "e")

craft = Button(game, text="Crafting", command=crafting, font=("Arial", 20, "bold"))
craft.place(relx = 1, rely = 0.25, anchor = "e")

day += 1
day_counter = Label(game, text = f"Day {day}", font=("Arial", 20, "bold"))
day_counter.place(relx = 0.5, rely = 0.05, anchor = CENTER)
escaped = False
alive = True

get_best_tools()

'''
try:
    z = int(input("Enable debug mode? (1 = yes, 0 = no): "))
    debug = (z == 1)
except:
    pass
'''

while alive and not escaped:
    get_best_tools()
    game.wait_variable(wait_var)
    day += 1
    day_counter.config(text = f"Day {day}")
    recharge(5)
    roll_event()

game.config(menu = None)
staminabar.destroy()
sp.destroy()
scav.destroy()
inv.destroy()
craft.destroy()

if not alive:
    event_msg("You have died. Game over.", font=("Arial", 20, "bold"), duration=0)
    advance.config(text="End")
elif escaped:
    event_msg("Congratulations! You have escaped the island!", font=("Arial", 20, "bold"), duration=0)
    advance.config(text="Leave")

game.wait_variable(wait_var)

game.destroy()