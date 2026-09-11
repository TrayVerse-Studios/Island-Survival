from tkinter import *
from random import *
import sys
import os
import json
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk
import webbrowser

game_log = ""
save = ""
difficulties = {
    "very_easy": 0.5,
    "easy": 0.75,
    "normal": 1,
    "hard": 1.25,
    "very_hard": 1.5
}

difficulty = 1

# Create a safe folder for saves in the user's Documents directory
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "IslandSurvivalSaves")
os.makedirs(SAVE_DIR, exist_ok=True)

class OptionDialog(Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """
    def __init__(self,parent,title,question,options):
        Toplevel.__init__(self,parent)
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", blank)
        self.iconphoto(True, logo)
        self.options = options
        self.result = '_'
        self.createWidgets()
        self.grab_set()
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()
    def createWidgets(self):
        frmQuestion = Frame(self)
        Label(frmQuestion,text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = Button(frmButtons,text=option.replace("_", " ").title(),command=lambda x=option:self.setOption(x))
            btn.grid(column=column,row=0)
            column += 1 
    def setOption(self,optionSelected):
        self.result = optionSelected
        self.destroy()

def link(url: str):
    webbrowser.open_new_tab(url)

def get_game_state():
    """Gathers all important variables into a dictionary."""
    return {
        "health": health, "stamina": stamina, "hydration": hydration, "hunger": hunger,
        "sick": sick, "day": day, "inventory": inventory,
        "main_mission": main_mission, "difficulty": difficulty,
        "mission1": mission1, "mission2": mission2, "mission3": mission3, "mission4": mission4,
        "mission5": mission5, "mission6": mission6, "mission7": mission7, "mission8": mission8,
        "rejected": rejected, "escaped": escaped, "save": save,
        "abandoned_ship": abandoned_ship, "abandoned_ufo": abandoned_ufo,
        "active_beacon": active_beacon, "active_advanced_beacon": active_advanced_beacon,
        "selected_pickaxe": selected_pickaxe, "selected_axe": selected_axe, "selected_sword": selected_sword,
        "selected_container": selected_container, "selected_rest": selected_rest, "game_log": game_log
    }

def apply_game_state(state):
    """Applies the loaded dictionary back to the game variables and updates the UI."""
    global health, stamina, hydration, hunger, sick, day, inventory, game_log, save, difficulty
    global main_mission, mission1, mission2, mission3, mission4, mission5, mission6, mission7, mission8
    global rejected, escaped, abandoned_ship, abandoned_ufo, active_beacon, active_advanced_beacon
    global selected_pickaxe, selected_axe, selected_sword, selected_container, selected_rest

    health = state.get("health", 100)
    stamina = state.get("stamina", 100)
    hydration = state.get("hydration", 100)
    hunger = state.get("hunger", 100)
    sick = state.get("sick", 0)
    day = state.get("day", 0)
    inventory = state.get("inventory", {})
    
    main_mission = state.get("main_mission", 0)
    mission1 = state.get("mission1", False)
    mission2 = state.get("mission2", False)
    mission3 = state.get("mission3", False)
    mission4 = state.get("mission4", False)
    mission5 = state.get("mission5", False)
    mission6 = state.get("mission6", False)
    mission7 = state.get("mission7", False)
    mission8 = state.get("mission8", False)
    
    rejected = state.get("rejected", False)
    escaped = state.get("escaped", False)
    abandoned_ship = state.get("abandoned_ship", False)
    abandoned_ufo = state.get("abandoned_ufo", False)
    active_beacon = state.get("active_beacon", False)
    active_advanced_beacon = state.get("active_advanced_beacon", False)

    selected_pickaxe = state.get("selected_pickaxe", None)
    selected_axe = state.get("selected_axe", None)
    selected_sword = state.get("selected_sword", None)
    selected_container = state.get("selected_container", None)
    selected_rest = state.get("selected_rest", None)
    game_log = state.get("game_log", "")
    save = state.get("save", "")
    difficulty = state.get("difficulty", 1)

    # Update the UI to reflect the loaded state
    update_health(health)
    update_stamina(stamina)
    update_hydration(hydration)
    update_hunger(hunger)
    day_counter.config(text=f"Day {day}")
    update_inventory_capacity()
    ensure_selected_tools(auto_equip=False)
    get_best_tools()

def save_game(new=False):
    global save
    filepath = save if not new and os.path.isfile(save) else filedialog.asksaveasfilename(
        initialdir=SAVE_DIR,
        title="Save Game",
        defaultextension=".json",
        filetypes=[("JSON Save Files", "*.json")]
    )
    if filepath:
        try:
            save = filepath
            with open(filepath, 'w') as f:
                json.dump(get_game_state(), f, indent=4)
            with open(filepath.replace(".json", ".md"), 'w') as f:
                f.write(game_log)

            event_msg(["Game Saved Successfully!"])
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save game:\n{e}")

def load_game():
    filepath = filedialog.askopenfilename(
        initialdir=SAVE_DIR,
        title="Load Game",
        filetypes=[("JSON Save Files", "*.json")]
    )
    if filepath:
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
            apply_game_state(state)
            event_msg(["Game Loaded Successfully!"])
            return True
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load game:\n{e}")
            return False

def play_game(new=True):
    global wait_var, advance, day, alive, escaped, sicklbl, game_log, washed_up
    game.deiconify()
    game.state("zoomed")
    
    advance = Button(game, text="Advance", command=proceed, font=("Arial", 20, "bold"))
    advance.place(relx=0.5, rely=0.95, anchor=CENTER)

    if new:
        diff = OptionDialog(game, "Select Difficulty", "Choose your difficulty level:", list(difficulties.keys()))
        difficulty = difficulties.get(diff.result, 1)
        event_msg(msg=["Welcome!", "You find yourself on a desert island with no supplies or memory of how you got there.", "Now, you have only one goal…", "SURVIVE"], font=("Arial", 20, "bold"))
        if len(os.listdir(SAVE_DIR)) == 0:
            if messagebox.askyesno("Welcome!", "It looks like this is your first time playing. Would you like to read the Wiki for tips and guidance?"):
                link("https://github.com/TrayVerse-Studios/Island-Survival/wiki")

    setup_game_ui()

    if randint(1,5) == 1:
        found = roll_loot(washed_up, rolls=5)
        if found:
            lines = [f"{qty} × {item.replace('_', ' ').title()}" for item, qty in found.items()]
            event_msg(msg=[f"An array of materials washed up on the shore:\n{'\n'.join(lines)}"])

    while alive and not escaped:
        ensure_selected_tools(auto_equip=True)
        get_best_tools()
        game.wait_variable(wait_var)
        day += 1
        day_counter.config(text=f"Day {day}")
        game_log = game_log + f"\n# --- Day {day} ---\n\n"

        sickness()

        # Bedroll bonus (does not cost hunger)
        if randint(1, 2) == 1 and best_rest:
            if best_rest == "advanced_camp":
                l = randint(41, 50)
            elif best_rest == "fortified_camp":
                l = randint(31, 40)
            elif best_rest == "improved_shelter":
                l = randint(21, 30)
            elif best_rest == "shelter":
                l = randint(11, 20)
            elif best_rest == "bedroll":
                l = randint(1, 10)
            event_msg([f"You were well rested and gained {l} stamina."])
            recharge(l, change_hunger=False)

        # Daily thirst
        thirst(5)
        if hydration == 0:
            take_damage(40)

        needed = min(5, 100 - stamina)      # only convert what you can actually use
        available = min(needed, hunger)

        if available > 0:
            recharge(available)             # gains stamina + loses hunger
        elif hunger == 0:
            take_damage(8)
        if not alive:
            break
        roll_event()

    scav.destroy()
    inv.destroy()
    craft.destroy()

    if not alive:
        end = "You have died. Game over."
        event_msg(msg=[end], font=("Arial", 20, "bold"))
        advance.config(text="End")
    elif escaped:
        end = "Congratulations! You have escaped the island!"
        event_msg(msg=[end], font=("Arial", 20, "bold"))
        advance.config(text="Leave")

    game.wait_variable(wait_var)

    destroy_game_ui()
    start_menu()

def quit_game():
    global save
    if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
        if os.path.isfile(save):
            save_game()
        elif messagebox.askyesno("Save", "Do you want to save before quitting?"):
            save_game(new=True)
        game.destroy()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def inventory_total():
    """Return the number of individual items currently held."""
    return sum(data.get("quantity", 0) for data in inventory.values())


def inventory_space():
    """Return the number of free inventory spaces."""
    return inv_max - inventory_total()


def can_add_item(item_key, amount=1):
    """Check whether the requested number of items can be added."""
    return inventory_space() >= amount


def add_item(item_key, amount=1, looting=False, cont=False, loot_table: dict=None):
    global item_descriptions
    """
    Add an item to the inventory if there is enough capacity.

    Returns True if the item was added, otherwise False.
    """
    if amount <= 0:
        return True, 0

    if not can_add_item(item_key, amount):
        if cont:
            amount = inventory_space()
            if amount <= 0:
                return False, 0
        else:
            return False, amount

    if item_key not in inventory:
        inventory[item_key] = {
            "name": item_key.replace("_", " ").title(),
            "quantity": 0,
            "durability": None,
            "nutrition": 0,
            "hydration": 0,
            "description": item_descriptions.get(item_key, "")
        }

    if item_key in durability_template:
        if not inventory[item_key]["durability"]:
            inventory[item_key]["durability"] = []
        for _ in range(amount):
            if looting:
                inventory[item_key]["durability"].append(randint(
                    1, durability_template[item_key]
                ))
                if loot_table: 
                    if randint(1, 2) == 1:
                        if selected_pickaxe and item_key in loot_table.get(selected_pickaxe, {}):
                            wear_tool(selected_pickaxe)
                        if selected_axe and item_key in loot_table.get(selected_axe, {}):
                            wear_tool(selected_axe)
            else:
                inventory[item_key]["durability"].append(durability_template[item_key])

    if item_key in food_template:
        inventory[item_key]["nutrition"] = food_template[item_key]
    if item_key in drink_template:
        inventory[item_key]["hydration"] = drink_template[item_key]
        

    inventory[item_key]["quantity"] += amount
    return True, amount

def roll_loot(loot_table: dict, rolls: int = 8, looting: bool = False, cont=False):
    """
    Rolls a loot table and attempts to add the items to the inventory.
    Returns a dictionary of the items successfully found.
    """
    found = {}
    count = 0
    while count < rolls:
        for item, chance in loot_table.items():
            count += 1
            if randint(1, 1000) <= chance * 1000:
                success, _ = add_item(item, looting=looting, loot_table=loot_table, cont=cont)
                if success:
                    if item in container_for_water:
                        container = container_for_water[item]
                        if inventory.get(container, {}).get("quantity", 0) <= 0:
                            continue
                        remove_item(container)
                    found[item] = found.get(item, 0) + 1
    return found

def remove_item(item_key, amount=1):
    """
    Removes a specified amount of an item from the inventory.
    Returns True if successful, False if the player doesn't have enough.
    """
    if item_key not in inventory:
        return False
    
    data = inventory[item_key]
    if data["quantity"] < amount:
        return False
    
    # Handle durability list if applicable
    if "durability" in data and isinstance(data["durability"], list):
        for _ in range(min(amount, len(data["durability"]))):
            data["durability"].pop(0)
            
    data["quantity"] -= amount
    if data["quantity"] <= 0:
        del inventory[item_key]
        
    # Refresh tools and UI in case a tool was removed
    ensure_selected_tools(auto_equip=False)
    get_best_tools()
    
    return True

def blank():
    pass

def start_battle(enemy_key, on_win=None, on_lose=None):
    global animal_data, enemy_data
    """
    Opens a turn-based battle window.
    enemy_key  – key from enemy_data
    on_win     – optional callback when player wins
    on_lose    – optional callback when player loses
    """

    if enemy_key in animal_data:
        enemy = animal_data[enemy_key]
    elif enemy_key in enemy_data:
        enemy = enemy_data[enemy_key]
    else:
        event_msg([f"Unknown enemy: {enemy_key}"])
        return
    enemy_name = enemy["name"]
    enemy_max_hp = round(enemy["max_hp"] * uniform(0.9, 1.1)) * difficulty
    enemy_hp = enemy_max_hp
    reaction = round(enemy["reaction_time"] * uniform(0.9, 1.1), 1) * difficulty          # higher → lower dodge chance
    atk_speed = round(enemy.get("attack_speed", 1.0) * uniform(0.9, 1.1), 1) * difficulty
    for attack in list(enemy["attacks"]):
        enemy[attack]['damage'] = round(enemy[attack]['damage'] * uniform(0.9, 1.1))

    # ---------- WINDOW ----------
    battle = Toplevel(game)
    battle.iconphoto(True, logo)
    battle.title(f"Battle – {enemy_name}")
    battle.geometry("900x600")
    battle.transient(game)
    battle.grab_set()
    battle.protocol("WM_DELETE_WINDOW", blank)

    # Left = Player
    left = Frame(battle, padx=20, pady=15)
    left.pack(side=LEFT, fill=Y)

    Label(left, text="YOU", font=("Arial", 18, "bold")).pack(anchor="w")
    player_hp_lbl = Label(left, text=f"Health: {health}%", font=("Arial", 14))
    player_hp_lbl.pack(anchor="w", pady=(5, 0))

    player_bar = Canvas(left, width=200, height=22, bg="red", highlightthickness=0)
    player_bar.pack(anchor="w", pady=4)
    player_bar_rect = player_bar.create_rectangle(0, 0, health * 2, 22, fill="green", width=0)

    Label(left, text="Choose action:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))

    melee_btn = Button(left, text="Melee Weapons", width=18, font=("Arial", 11))
    melee_btn.pack(anchor="w", pady=3)

    ranged_btn = Button(left, text="Ranged Weapons", width=18, font=("Arial", 11))
    ranged_btn.pack(anchor="w", pady=3)

    # Right = Enemy
    right = Frame(battle, padx=20, pady=15)
    right.pack(side=RIGHT, fill=Y)

    Label(right, text=enemy_name, font=("Arial", 18, "bold")).pack(anchor="e")
    enemy_hp_lbl = Label(right, text=f"Health: {enemy_hp}/{enemy_max_hp}", font=("Arial", 14))
    enemy_hp_lbl.pack(anchor="e", pady=(5, 0))

    enemy_bar = Canvas(right, width=200, height=22, bg="darkred", highlightthickness=0)
    enemy_bar.pack(anchor="e", pady=4)
    enemy_bar_rect = enemy_bar.create_rectangle(0, 0, 200, 22, fill="orange", width=0)

    # Center log + controls
    center = Frame(battle, padx=10)
    center.pack(fill=BOTH, expand=True)

    log = Text(center, height=12, width=50, font=("Arial", 11), state="disabled", wrap="word")
    log.pack(pady=10, fill=BOTH, expand=True)

    def battle_log(msg):
        log.config(state="normal")
        log.insert("end", msg + "\n")
        log.see("end")
        log.config(state="disabled")

    # Weapon selection frame (appears when Melee/Ranged is clicked)
    weapon_frame = Frame(center)

    next_turn_btn = Button(center, text="Next Turn →", font=("Arial", 14, "bold"), width=16)
    next_turn_btn.pack(pady=8)

    status_lbl = Label(center, text="Your turn – choose a weapon", font=("Arial", 12), fg="blue")
    status_lbl.pack() 

    # ---------- STATE ----------
    player_turn = True
    battle_over = False
    current_weapon = None
    qte_active = False
    qte_button = None
    qte_timer = None

    def update_bars():
        # Player
        player_hp_lbl.config(text=f"Health: {health}%")
        player_bar.coords(player_bar_rect, 0, 0, max(0, health * 2), 22)
        # Enemy
        enemy_hp_lbl.config(text=f"Health: {enemy_hp}/{enemy_max_hp}")
        bar_w = int((enemy_hp / enemy_max_hp) * 200)
        enemy_bar.coords(enemy_bar_rect, 0, 0, max(0, bar_w), 22)

    def end_battle(player_won):
        nonlocal battle_over
        battle_over = True
        next_turn_btn.config(state="disabled")
        melee_btn.config(state="disabled")
        ranged_btn.config(state="disabled")

        if player_won:
            battle_log(f"\n*** You defeated the {enemy_name}! ***")
            status_lbl.config(text="Victory!", fg="green")
            if on_win:
                battle.after(1500, lambda: (battle.destroy(), on_win(enemy)))
            else:
                battle.after(2000, battle.destroy)
        else:
            battle_log(f"\n*** You were defeated by the {enemy_name}... ***")
            status_lbl.config(text="Defeat...", fg="red")
            if on_lose:
                battle.after(1500, lambda: (battle.destroy(), on_lose(enemy)))
            else:
                battle.after(2000, battle.destroy)

    def get_melee_weapons():
        result = ["punch"]
        result.extend(w for w in melee_template if inventory.get(w, {}).get("quantity", 0) > 0)
        return result

    def get_ranged_weapons():
        result = []
        for w, (dmg, ammo) in ranged_template.items():
            if inventory.get(w, {}).get("quantity", 0) > 0:
                if ammo is None or inventory.get(ammo, {}).get("quantity", 0) > 0:
                    result.append(w)
        return result

    def show_weapon_menu(kind):
        for child in weapon_frame.winfo_children():
            child.destroy()
        weapon_frame.pack(pady=5)

        weapons = get_melee_weapons() if kind == "melee" else get_ranged_weapons()
        if not weapons:
            Label(weapon_frame, text=f"No usable {kind} weapons!", fg="red").pack()
            return

        Label(weapon_frame, text=f"Select {kind} weapon:", font=("Arial", 11, "bold")).pack()

        for w in weapons:
            if w == "punch":
                dmg = 5
            else:
                dmg = melee_template[w] if kind == "melee" else ranged_template[w][0]
            ammo_txt = ""
            if kind == "ranged" and ranged_template[w][1]:
                ammo = ranged_template[w][1]
                ammo_txt = f"  (Ammo: {inventory.get(ammo, {}).get('quantity', 0)})"

            btn = Button(
                weapon_frame,
                text=f"{w.replace('_', ' ').title()}  –  {dmg} dmg{ammo_txt}",
                width=36,
                anchor="w",
                command=lambda weapon=w, k=kind: select_weapon(weapon, k)
            )
            btn.pack(pady=2)

    def select_weapon(weapon, kind):
        nonlocal current_weapon
        current_weapon = (weapon, kind)
        for child in weapon_frame.winfo_children():
            child.destroy()

        if weapon == "punch":
            dmg = 5
        else:
            dmg = melee_template[weapon] if kind == "melee" else ranged_template[weapon][0]
        Label(weapon_frame, text=f"Selected: {weapon.replace('_', ' ').title()} ({dmg} dmg)",
              font=("Arial", 11)).pack()
        Button(weapon_frame, text="ATTACK!", font=("Arial", 12, "bold"),
               bg="#c44", fg="white", width=12,
               command=player_attack).pack(pady=6)

    def lose_durability(weapon):
        """Reduce durability of a weapon. Returns True if it broke."""
        if weapon == "punch" or weapon not in inventory:
            return False
        data = inventory[weapon]
        if "durability" not in data:
            return False

        dur = data["durability"]
        if isinstance(dur, list):
            if dur:
                dur[0] -= 1
                if dur[0] <= 0:
                    dur.pop(0)
                    data["quantity"] -= 1
                    if data["quantity"] <= 0:
                        del inventory[weapon]
                        battle_log(f"Your {weapon.replace('_', ' ')} broke!")
                        return True
            return False
        else:
            data["durability"] -= 1
            if data["durability"] <= 0:
                data["quantity"] -= 1
                if data["quantity"] <= 0:
                    del inventory[weapon]
                battle_log(f"Your {weapon.replace('_', ' ')} broke!")
                return True
        return False

    def player_attack():
        nonlocal enemy_hp, player_turn, current_weapon
        if not player_turn or battle_over or current_weapon is None:
            return

        weapon, kind = current_weapon
        if weapon == "punch":
            damage = 5
        elif kind == "melee":
            damage = melee_template[weapon]
        else:
            damage = ranged_template[weapon][0]
            ammo = ranged_template[weapon][1]
            if ammo:
                if inventory.get(ammo, {}).get("quantity", 0) <= 0:
                    battle_log("No ammunition left!")
                    return
                inventory[ammo]["quantity"] -= 1
                if inventory[ammo]["quantity"] <= 0:
                    del inventory[ammo]

        # Dodge chance (higher reaction_time → lower dodge chance)
        dodge_chance = max(5, 70 - reaction)        # reaction 55 → ~15% dodge
        if randint(1, 100) <= dodge_chance:
            battle_log(f"The {enemy_name} dodged your attack!")
        else:
            # Critical hit?
            if randint(1, 100) <= 12:
                damage = int(damage * 1.6)
                battle_log(f"CRITICAL HIT! You dealt {damage} damage with {weapon.replace('_', ' ')}!")
            else:
                battle_log(f"You hit the {enemy_name} for {damage} damage with {weapon.replace('_', ' ')}!")

            enemy_hp = max(0, enemy_hp - damage)
            update_bars()

        lose_durability(weapon)
        current_weapon = None
        for child in weapon_frame.winfo_children():
            child.destroy()

        if enemy_hp <= 0:
            end_battle(True)
            return

        player_turn = False
        status_lbl.config(text="Enemy's turn – get ready!", fg="red")
        next_turn_btn.config(state="normal")

    def start_qte(attack):
        nonlocal qte_active, qte_button, qte_timer
        qte_active = True
        next_turn_btn.config(state="disabled")

        # Time window based on attack type + enemy speed
        base_time = 1000 if attack["type"] == "melee" else 1800
        time_ms = int(base_time / atk_speed)

        def success():
            nonlocal qte_active
            if not qte_active:
                return
            qte_active = False
            if qte_timer:
                battle.after_cancel(qte_timer)
            if qte_button:
                qte_button.destroy()
            battle_log(f"You blocked the {attack['name']}!")
            finish_enemy_turn(0)          # no damage

        def fail():
            nonlocal qte_active
            if not qte_active:
                return
            qte_active = False
            if qte_button:
                qte_button.destroy()
            battle_log(f"You failed to block! Took {attack['damage']} damage.")
            finish_enemy_turn(attack["damage"])

        qte_button = Button(center, text="CLICK!", font=("Arial", 20, "bold"),
                            bg="yellow", width=12, height=2, command=success)
        qte_button.pack(pady=10)
        qte_timer = battle.after(time_ms, fail)
        status_lbl.config(text=f"QTE! Click the button! ({time_ms}ms)", fg="orange")

    def finish_enemy_turn(damage):
        nonlocal player_turn
        if damage > 0:
            take_damage(damage)
            update_bars()
            if health <= 0:
                end_battle(False)
                return

        player_turn = True
        status_lbl.config(text="Your turn – choose a weapon", fg="blue")
        next_turn_btn.config(state="normal")
        melee_btn.config(state="normal")
        ranged_btn.config(state="normal")

    def enemy_turn():
        if battle_over:
            return
        attack = choice(enemy["attacks"])
        battle_log(f"The {enemy_name} uses {attack['name']}!")
        start_qte(attack)

    def next_turn():
        if battle_over:
            return
        if player_turn:
            battle_log("You hesitate...")
            # still allow enemy to act
        next_turn_btn.config(state="disabled")
        melee_btn.config(state="disabled")
        ranged_btn.config(state="disabled")
        for child in weapon_frame.winfo_children():
            child.destroy()
        enemy_turn()

    # Wire up buttons
    melee_btn.config(command=lambda: show_weapon_menu("melee"))
    ranged_btn.config(command=lambda: show_weapon_menu("ranged"))
    next_turn_btn.config(command=next_turn)

    battle_log(f"A wild {enemy_name} appears!")
    battle_log("Choose a weapon and attack, then press Next Turn.")
    update_bars()

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

def update_hydration(current_hydration):
    global hydration, alive
    current_hydration = max(0, min(current_hydration, 100))
    hydration = current_hydration
    bar_width = (current_hydration / 100) * 200
    hydrationbar.coords(hydration_bar, 0, 0, bar_width, 25)
    hyp.config(text = f"Hydration: {current_hydration}%")

def update_hunger(current_hunger):
    global hunger, alive
    current_hunger = max(0, min(current_hunger, 100))
    hunger = current_hunger
    bar_width = (current_hunger / 100) * 200
    hungerbar.coords(hunger_bar, 0, 0, bar_width, 25)
    hup.config(text = f"Hunger: {current_hunger}%")

def wear_tool(tool_key):
    """Reduce durability of the first tool in the list. Returns True if it broke."""
    if tool_key not in inventory:
        return True
    data = inventory[tool_key]
    dur = data.get("durability")
    if not isinstance(dur, list) or not dur:
        return False

    dur[0] -= 1
    if dur[0] <= 0:
        dur.pop(0)
        remove_item(tool_key)
        event_msg([f"Your {tool_key.replace('_', ' ').title()} broke!"])
        ensure_selected_tools(auto_equip=False)
        durability_check()
        return True
    return False

def take_damage(num=10):
    global health
    health -= round(num * difficulty)
    update_health(health)

def heal(num=10):
    global health
    health += num
    update_health(health)
    
def tire(num=10):
    global stamina
    stamina -= round(num * difficulty)
    update_stamina(stamina)

def recharge(num=10, change_hunger=True):
    global stamina

    stamina += num
    if change_hunger:
        starve(num, diff=False)
    update_stamina(stamina)

def hydrate(num=10):
    global hydration
    hydration += num
    update_hydration(hydration)

def thirst(num=10):
    global hydration
    hydration -= round(num * difficulty)
    update_hydration(hydration)

def feed(num=10):
    global hunger
    hunger += num
    update_hunger(hunger)

def starve(num=10, diff=True):
    global hunger
    hunger -= round(num * difficulty) if diff else num
    update_hunger(hunger)

def sickness(num: int=None):
    global sick, sicklbl, difficulty
    if num:
        sick = round(max(0, sick + (num * difficulty))) if num > 0 else max(0, sick + num)
        return

    if sick > 0:
        if not sicklbl:
            sicklbl = True
            sick_lbl.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        sick -= 1
        take_damage(10)
        if sick <= 0:
            sicklbl = False
            sick_lbl.forget()
        
TOOL_CATEGORIES = {
    "pickaxe": [
        "galaxium_pickaxe", "ruby_pickaxe", "diamond_pickaxe",
        "iron_pickaxe", "stone_pickaxe", "wooden_pickaxe"
    ],
    "axe": [
        "galaxium_axe", "ruby_axe", "diamond_axe",
        "iron_axe", "stone_axe", "wooden_axe"
    ],
    "sword": [
        "galaxium_sword", "ruby_sword", "diamond_sword",
        "iron_sword", "stone_sword", "wooden_sword"
    ],
    "container": ["bucket", "bowl", "coconut_shell"],
    "rest": [
        "advanced_camp", "fortified_camp", "improved_shelter",
        "shelter", "bedroll"
    ],
}

def tool_owned(item_key):
    return inventory.get(item_key, {}).get("quantity", 0) > 0

def get_best_for(category):
    for item in TOOL_CATEGORIES[category]:
        if tool_owned(item):
            return item
    return None

def get_item_category(item_key):
    for category, items in TOOL_CATEGORIES.items():
        if item_key in items:
            return category
    return None

def ensure_selected_tools(auto_equip=False):
    """Clear broken/missing selections. If auto_equip=True, fill empty slots with the best tool."""
    global selected_pickaxe, selected_axe, selected_sword, selected_container, selected_rest

    pairs = [
        ("pickaxe", "selected_pickaxe"),
        ("axe", "selected_axe"),
        ("sword", "selected_sword"),
        ("container", "selected_container"),
        ("rest", "selected_rest"),
    ]

    current = {
        "selected_pickaxe": selected_pickaxe,
        "selected_axe": selected_axe,
        "selected_sword": selected_sword,
        "selected_container": selected_container,
        "selected_rest": selected_rest,
    }

    for category, varname in pairs:
        value = current[varname]
        if value and not tool_owned(value):
            value = None
        if auto_equip and value is None:
            value = get_best_for(category)
        current[varname] = value

    selected_pickaxe = current["selected_pickaxe"]
    selected_axe = current["selected_axe"]
    selected_sword = current["selected_sword"]
    selected_container = current["selected_container"]
    selected_rest = current["selected_rest"]

def select_tool(item_key):
    global selected_pickaxe, selected_axe, selected_sword, selected_container, selected_rest

    if not tool_owned(item_key):
        event_msg(["You don't have that tool."])
        return

    category = get_item_category(item_key)
    if category == "pickaxe":
        selected_pickaxe = item_key
    elif category == "axe":
        selected_axe = item_key
    elif category == "sword":
        selected_sword = item_key
    elif category == "container":
        selected_container = item_key
    elif category == "rest":
        selected_rest = item_key
    else:
        event_msg(["That item cannot be selected as a tool."])
        return

    event_msg([f"Selected {item_key.replace('_', ' ').title()}."])

def get_best_tools():
    global best_pickaxe, best_axe, best_sword, best_container, best_rest
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
    if inventory.get("bucket", {}).get("quantity", 0) > 0:
        best_container = "bucket"
    elif inventory.get("bowl", {}).get("quantity", 0) > 0:
        best_container = "bowl"
    elif inventory.get("coconut_shell", {}).get("quantity", 0) > 0:
        best_container = "coconut_shell"
    else:
        best_container = None
    if inventory.get("advanced_camp", {}).get("quantity", 0) > 0:
        best_rest = "advanced_camp"
    elif inventory.get("fortified_camp", {}).get("quantity", 0) > 0:
        best_rest = "fortified_camp"
    elif inventory.get("improved_shelter", {}).get("quantity", 0) > 0:
        best_rest = "improved_shelter"
    elif inventory.get("shelter", {}).get("quantity", 0) > 0:
        best_rest = "shelter"
    elif inventory.get("bedroll", {}).get("quantity", 0) > 0:
            best_rest = "bedroll"
    else:
        best_rest = None

def durability_check():
    for item in list(inventory):
        if item in durability_template:
            data = inventory[item]
            dur = data.get("durability")
            if isinstance(dur, list):
                # Remove any already-broken entries (safety)
                while dur and dur[0] <= 0:
                    dur.pop(0)
                    data["quantity"] -= 1
                if data["quantity"] <= 0 or not dur:
                    del inventory[item]
                    event_msg([f"Your {item.replace('_', ' ').title()} broke!"])
    ensure_selected_tools(auto_equip=False)
    get_best_tools()

def get_scavenge_chances():
    """Return the chance table that applies right now (base + any owned tools)."""
    chances = scavenge_chance["base"].copy()

    if selected_pickaxe:
        for item, ch in scavenge_chance[selected_pickaxe].items():
            chances[item] = max(chances.get(item, 0), ch)
    if selected_axe:
        for item, ch in scavenge_chance[selected_axe].items():
            chances[item] = max(chances.get(item, 0), ch)
    if selected_container:
        for item, ch in scavenge_chance[selected_container].items():
            chances[item] = max(chances.get(item, 0), ch)
    return chances

current_event = None
event_after_id = None

def event_msg(msg=[], font=("Arial", 16)):
    global current_event, event_after_id, game_log

    if msg == "":
        return

    event_msg_win = Toplevel(game)
    event_msg_win.title("Event")
    event_msg_win.geometry("750x550")
    event_msg_win.transient(game)
    event_msg_win.grab_set()
    event_msg_win.protocol("WM_DELETE_WINDOW", blank)
    event_msg_win.iconphoto(True, logo)

    wait_var_msg = BooleanVar(value=False)

    def proceed_msg():
        wait_var_msg.set(True)

    eventmsg = Label(event_msg_win, text="", font=font, wraplength=700, justify=CENTER)
    eventmsg.place(relx=0.5, rely=0.5, anchor=CENTER)
    advancemsg = Button(event_msg_win, text="Advance", command=proceed_msg, font=("Arial", 20, "bold"))

    for message in msg:
        if message == msg[-1]:
            advancemsg.destroy()
        else:
            advancemsg.place(relx=0.5, rely=0.95, anchor=CENTER)
        eventmsg.config(text=message)
        game_log = game_log + f"{message}\n"
        if len(msg) > 1 and message != msg[-1]:
            event_msg_win.wait_variable(wait_var_msg)
            advancemsg.place_forget()

    game_log = game_log + "\n"

    Button(event_msg_win, text="Continue", command=event_msg_win.destroy).pack(pady=15)

def filter_keys(keys, query):
    """Return keys whose name or key matches the search text."""
    q = query.strip().lower()
    if not q:
        return list(keys)
    result = []
    for key in keys:
        name = key.replace("_", " ").lower()
        if q in name or q in key.lower():
            result.append(key)
    return result

def invsee():
    if health <= 0:
        return
    if not inventory:
        event_msg(msg=["Your inventory is empty."])
        return

    inv_win = Toplevel(game)
    inv_win.title("Inventory")
    inv_win.geometry("700x520")
    inv_win.transient(game)
    inv_win.grab_set()
    inv_win.iconphoto(True, logo)

    # ── Left side: scrollable list of item buttons ──────────────────
    left = Frame(inv_win)
    left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    search_var = StringVar()
    search_entry = Entry(left, textvariable=search_var, font=("Arial", 11))
    search_entry.pack(fill=X, pady=(0, 6))
    search_entry.focus_set()

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

    capacity_lbl = Label(right, text=f"Inventory: {inventory_total()} / {inv_max}", font=("Arial", 14))
    capacity_lbl.pack(anchor="w", pady=(0, 8))

    qty_lbl = Label(right, text="", font=("Arial", 14))
    qty_lbl.pack(anchor="w")

    dur_lbl = Label(right, text="", font=("Arial", 14))
    dur_lbl.pack(anchor="w", pady=(4, 0))

    nutrition_lbl = Label(right, text="", font=("Arial", 14))
    nutrition_lbl.pack(anchor="w", pady=(4, 0))

    hydration_lbl = Label(right, text="", font=("Arial", 14))
    hydration_lbl.pack(anchor="w", pady=(4, 0))

    damage_lbl = Label(right, text="", font=("Arial", 14))
    damage_lbl.pack(anchor="w", pady=(4, 0))

    desc = Label(right, text="", font=("Arial", 12), fg="gray", justify=CENTER, wraplength=350)
    desc.pack(anchor="w", pady=(8, 0))

    extra_lbl = Label(right, text="", font=("Arial", 12), fg="gray", justify=LEFT)
    extra_lbl.pack(anchor="w", pady=(4, 0))

    select_btn = Button(right, text="Select", font=("Arial", 12), width=10)
    # Action buttons (created once)
    consume_btn = Button(right, text="Consume", font=("Arial", 12), width=10)

    # Drop UI (created once)
    drop_frame = Frame(right)
    qty_entry = Entry(drop_frame, width=6, font=("Arial", 12), justify="center")
    qty_entry.insert(0, "1")
    drop_btn = Button(drop_frame, text="Drop", font=("Arial", 12), width=8)
    drop_warning = Label(right, text="", font=("Arial", 11), fg="red", justify=LEFT)

    def clear_details():
        title_lbl.config(text="Select an item")
        qty_lbl.config(text="")
        dur_lbl.config(text="")
        nutrition_lbl.config(text="")
        hydration_lbl.config(text="")
        damage_lbl.config(text="")
        extra_lbl.config(text="")
        consume_btn.pack_forget()
        drop_frame.pack_forget()
        drop_warning.pack_forget()
        select_btn.pack_forget()
        desc.config(text="")

    def consume_item(item_key):
        if item_key not in inventory:
            return
        try:
            amount = int(qty_entry.get().strip())
        except ValueError:
            event_msg(msg=["Please enter a valid whole number."])
            return
        
        if amount <= 0:
            event_msg(msg=["Please enter a positive number."])
            return

        data = inventory[item_key]
        nutrition = data.get("nutrition", 0) * amount
        hydr = data.get("hydration", 0) * amount
        name = data["name"]

        # Always fill hunger when the item has nutrition
        if nutrition > 0:
            feed(nutrition)

        # Handle hydration / salt
        if item_key in drink_template:
            if hydr > 0:
                hydrate(hydr)
                event_msg([f"You consumed {amount} × {name}. +{nutrition} hunger, +{hydr} hydration."])
            elif hydr < 0:
                thirst(abs(hydr))
                event_msg([f"You consumed {amount} × {name}. +{nutrition} hunger, but it was salty (−{abs(hydr)} hydration)."])
            else:
                event_msg([f"You consumed {amount} × {name}. +{nutrition} hunger."])
        elif item_key.startswith("raw_") and randint(1, 100) <= 30:
            event_msg([f"You consumed {amount} × {name}. +{nutrition} hunger, but you feel sick."])
            sickness(num=2*amount)
        elif item_key == "herbal_medicine":
            heal(15)
            sickness(num=-4*amount)
            event_msg([f"You consumed {amount} × {name} and treated your sickness."])
        elif item_key == "bandage":
            heal(5)
            event_msg([f"You used {amount} × {name} and treated your injuries."])
        else:
            event_msg([f"You consumed {amount} × {name}. +{nutrition} hunger."])
        

        # Consume one
        data["quantity"] -= amount
        capacity_lbl.config(text=f"Inventory: {inventory_total()} / {inv_max}")

        if data["quantity"] <= 0:
            del inventory[item_key]
            clear_details()
        else:
            show_details(item_key)
        rebuild_item_buttons()

    def can_safely_drop_backpack(item_key, amount):
        if item_key not in ("small_backpack", "large_backpack", "tactical_backpack"):
            return True

        original_qty = inventory[item_key]["quantity"]
        inventory[item_key]["quantity"] -= amount
        if inventory[item_key]["quantity"] <= 0:
            del inventory[item_key]

        update_inventory_capacity()
        new_max = inv_max
        current_items = inventory_total()

        # Restore
        if item_key not in inventory:
            inventory[item_key] = {
                "name": item_key.replace("_", " ").title(),
                "quantity": 0
            }
        inventory[item_key]["quantity"] = original_qty
        update_inventory_capacity()

        return new_max >= current_items

    def drop_item(item_key):
        if item_key not in inventory:
            return
        try:
            amount = int(qty_entry.get().strip())
        except ValueError:
            event_msg(["Please enter a valid whole number."])
            return
        if amount <= 0:
            event_msg(["Please enter a positive number."])
            return
        
        data = inventory[item_key]
        amount = min(amount, data["quantity"])
        
        if not can_safely_drop_backpack(item_key, amount):
            event_msg(["You cannot drop that backpack — you are carrying too many items for the lower capacity."])
            return
            
        name = data["name"]
        
        if remove_item(item_key, amount):
            update_inventory_capacity()
            capacity_lbl.config(text=f"Inventory: {inventory_total()} / {inv_max}")
            event_msg([f"Dropped {amount} × {name}."])
            clear_details()
            rebuild_item_buttons()
        else:
            event_msg(["Failed to drop item."])

    def show_details(item_key):
        if item_key not in inventory:
            return

        data = inventory[item_key]
        capacity_lbl.config(text=f"Inventory: {inventory_total()} / {inv_max}")
        title_lbl.config(text=data["name"])
        qty_lbl.config(text=f"Quantity: {data['quantity']}")
        desc.config(text=data.get("description", ""))

        # Durability
        if "durability" in data:
            max_dur = durability_template.get(item_key, "?")
            dur_val = data["durability"]
            if isinstance(dur_val, list):
                if dur_val:
                    dur_lbl.config(text=f"Durability: {dur_val[0]} / {max_dur}  ({len(dur_val)} tools)")
                else:
                    dur_lbl.config(text="")
            else:
                dur_lbl.config(text=f"Durability: {dur_val} / {max_dur}")
        else:
            dur_lbl.config(text="")

        # Nutrition
        if "nutrition" in data:
            nutrition_lbl.config(text=f"Nutrition: {data['nutrition']}")
        else:
            nutrition_lbl.config(text="")

        if "hydration" in data:
            hydration_lbl.config(text=f"Hydration: {data['hydration']}")
        else:
            hydration_lbl.config(text="")

        # Attack damage
        if item_key in melee_template:
            damage_lbl.config(text=f"Attack Damage: {melee_template[item_key]}")
        else:
            damage_lbl.config(text="")

        # inside show_details:
        select_btn.pack_forget()
        category = get_item_category(item_key)
        if category:
            selected = {
                "pickaxe": selected_pickaxe,
                "axe": selected_axe,
                "sword": selected_sword,
                "container": selected_container,
                "rest": selected_rest,
            }[category]

            if selected == item_key:
                extra_lbl.config(text=extra_lbl.cget("text") + "\nCurrently selected")
            else:
                select_btn.config(command=lambda k=item_key: (select_tool(k), show_details(k)))
                select_btn.pack(anchor="w", pady=(8, 0))

        # Reset buttons
        consume_btn.pack_forget()
        drop_frame.pack_forget()
        drop_warning.pack_forget()
        # Consume button (food or drink)
        if item_key in food_template or item_key in drink_template:
            consume_btn.config(command=lambda k=item_key: consume_item(k))
            consume_btn.pack(anchor="w", pady=(10, 0))
        elif item_key == "bandage":
            consume_btn.config(text="Use", command=lambda k=item_key: consume_item(k))
            consume_btn.pack(anchor="w", pady=(10, 0))

        # Drop controls
        qty_entry.delete(0, END)
        qty_entry.insert(0, "1")

        if can_safely_drop_backpack(item_key, 1):
            drop_btn.config(command=lambda k=item_key: drop_item(k))
            drop_frame.pack(anchor="w", pady=(12, 0))
            qty_entry.pack(side=LEFT, padx=(0, 8))
            drop_btn.pack(side=LEFT)
        else:
            drop_warning.config(text="Cannot drop this backpack\nwhile carrying so many items.")
            drop_warning.pack(anchor="w", pady=(10, 0))

        # Flavour text
        if item_key.endswith(("_pickaxe", "_axe")):
            extra_lbl.config(text="This is a tool.\nIt loses durability when used.")
        elif item_key.endswith("_sword"):
            extra_lbl.config(text="This is a weapon.\nIt can be used in combat.")
        else:
            extra_lbl.config(text="")

    # Create one button for every item
    def rebuild_item_buttons(*_):
        for child in button_frame.winfo_children():
            child.destroy()

        matches = filter_keys(inventory.keys(), search_var.get())
        if not matches:
            Label(button_frame, text="No items found", fg="gray").pack(anchor="w")
            return

        for item_key in matches:
            name = inventory[item_key]["name"]
            qty = inventory[item_key].get("quantity", 0)
            btn = Button(
                button_frame,
                text=f"{name}  ({qty})",
                width=22,
                anchor="w",
                font=("Arial", 11),
                command=lambda k=item_key: show_details(k)
            )
            btn.pack(fill=X, pady=2)

    search_var.trace_add("write", rebuild_item_buttons)
    rebuild_item_buttons()

    Button(inv_win, text="Close", font=("Arial", 12), width=12,
           command=inv_win.destroy).pack(side=BOTTOM, pady=12)

def update_inventory_capacity():
    global inv_max

    if inventory.get("tactical_backpack", {}).get("quantity", 0) > 0:
        inv_max = 60
    elif inventory.get("large_backpack", {}).get("quantity", 0) > 0:
        inv_max = 45
    elif inventory.get("small_backpack", {}).get("quantity", 0) > 0:
        inv_max = 30
    else:
        inv_max = 15

def scavenge():
    global inventory
    ensure_selected_tools(auto_equip=True)
    if health <= 0:
        return
    if inventory_total() >= inv_max:
        event_msg(msg=["Your inventory is full. You cannot scavenge until you free up some space."])
    elif stamina < 5:
        event_msg(msg=["You are too tired to scavenge. You need to rest."])
    else:
        found = roll_loot(get_scavenge_chances(), rolls=10, looting=True)
        msg = f"You went scavenging with your {selected_pickaxe.replace('_', ' ')} and {selected_axe.replace('_', ' ')}" if selected_pickaxe and selected_axe else f"You went scavenging with your {selected_pickaxe.replace('_', ' ')}" if selected_pickaxe else f"You went scavenging with your {selected_axe.replace('_', ' ')}" if selected_axe else "You went scavenging"
        if found:
            lines = [f"{qty} × {item.replace('_', ' ').title()}" for item, qty in found.items()]
            if inventory_total() >= inv_max:
                msg = msg + "\nYour inventory is full. You couldn't carry everything you found.\nYou found:\n" + "\n".join(lines)
            else:
                msg = msg + "\nYou found:\n" + "\n".join(lines)
        else:
            msg = msg + "\nYou found nothing."
        event_msg([msg])
        tire(5)
        get_best_tools()

def crafting():
    if health <= 0:
        return
    craft_win = Toplevel(game)
    craft_win.title("Crafting")
    craft_win.geometry("750x550")
    craft_win.transient(game)
    craft_win.grab_set()
    craft_win.iconphoto(True, logo)

    # ── Left side: scrollable recipe list ───────────────────────────
    left = Frame(craft_win)
    left.pack(side=LEFT, fill=Y, padx=10, pady=10)

    search_var = StringVar()
    search_entry = Entry(left, textvariable=search_var, font=("Arial", 11))
    search_entry.pack(fill=X, pady=(0, 6))
    search_entry.focus_set()

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
        result = recipe_key
        amount = recipe["quantity"]

        # How many spaces will be freed by removing the ingredients?
        spaces_freed = sum(recipe["ingredients"].values())
        # How many spaces will the result take?
        spaces_needed = amount
        net = spaces_needed - spaces_freed

        if net > 0 and inventory_space() < net:
            return False, f"Your inventory is full. You need {net} more free space to craft this."

        # Check requirement (workbench / furnace etc.)
        req = recipe["requirements"]
        if req is not None:
            if inventory.get(req, {}).get("quantity", 0) <= 0:
                return False, f"Missing requirement: {req.replace('_', ' ').title()}"

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
        global inv_max
        recipe = crafting_recipes[recipe_key]
        result = recipe_key
        amount = recipe["quantity"]

        # Remove ingredients
        for item, needed in recipe["ingredients"].items():
            remove_item(item, needed)

        # Add the crafted item
        add_item(result, amount)

        # Backpack capacity
        if result == "small_backpack":
            global inv_max
            inv_max = max(inv_max, 20)

        elif result == "large_backpack":
            inv_max = max(inv_max, 35)

        elif result == "tactical_backpack":
            inv_max = max(inv_max, 50)

        ensure_selected_tools(auto_equip=False)
        get_best_tools()

        event_msg([f"Crafted {amount} × {inventory[result]['name']}"])
        show_details(recipe_key)

    def show_details(recipe_key):
        recipe = crafting_recipes[recipe_key]
        nice_name = recipe_key.replace('_', ' ').title()

        title_lbl.config(text=nice_name)
        produces_lbl.config(text=f"Produces: {recipe['quantity']} × {nice_name}")

        # Build ingredients text with owned / needed
        lines = ["Ingredients:"]
        for item, needed in recipe["ingredients"].items():
            owned = inventory.get(item, {}).get("quantity", 0)
            status = "✓" if owned >= needed else "✗"
            lines.append(f"  {status}  {item.replace('_', ' ').title()}: {owned} / {needed}")
        ingredients_lbl.config(text="\n".join(lines))

        # Requirement
        req = recipe["requirements"]
        if req is None:
            req_lbl.config(text="Requirement: None")
        else:
            owned_req = inventory.get(req, {}).get("quantity", 0)
            mark = "✓" if owned_req > 0 else "✗"
            req_lbl.config(text=f"Requirement: {mark}  {req.replace('_', ' ').title()}")

        # Can we craft?
        possible, message = can_craft(recipe_key)
        status_lbl.config(text=message, fg="green" if possible else "red")

        # Show / hide the Craft button
        craft_btn.pack_forget()
        if possible:
            craft_btn.config(command=lambda: do_craft(recipe_key))
            craft_btn.pack(anchor="w", pady=(15, 0))

    # Create a button for every recipe
    def rebuild_recipe_buttons(*_):
        for child in button_frame.winfo_children():
            child.destroy()

        matches = filter_keys(sorted(crafting_recipes.keys()), search_var.get())
        if not matches:
            Label(button_frame, text="No recipes found", fg="gray").pack(anchor="w")
            return

        for recipe_key in matches:
            name = recipe_key.replace("_", " ").title()
            btn = Button(
                button_frame,
                text=name,
                width=24,
                anchor="w",
                font=("Arial", 11),
                command=lambda k=recipe_key: show_details(k)
            )
            btn.pack(fill=X, pady=2)

    search_var.trace_add("write", rebuild_recipe_buttons)
    rebuild_recipe_buttons()

    # Close button
    Button(craft_win, text="Close", font=("Arial", 12), width=12,
           command=craft_win.destroy).pack(side=BOTTOM, pady=12)
    get_best_tools()

def proceed():
    wait_var.set(True)

def roll_event():
    global inventory, main_mission, active_beacon, mission1, mission2, mission3, mission4, mission5, mission6, mission7, mission8, rejected, escaped, abandoned_ship, abandoned_ufo, active_advanced_beacon, active_beacon
    if active_advanced_beacon:
        main_mission = 8
    elif (inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0) and inventory.get("advanced_signal_booster", {}).get("quantity", 0) > 0 and inventory.get("advanced_emergency_beacon", {}).get("quantity", 0) > 0 and not abandoned_ufo:
        main_mission = 7
    elif (inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0) and inventory.get("advanced_signal_booster", {}).get("quantity", 0) > 0:
        main_mission = 6
    elif (inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0):
        main_mission =5
    elif active_beacon:
        main_mission = 4
    elif (inventory.get("receiver", {}).get("quantity", 0) > 0 or inventory.get("radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0) and (inventory.get("signal_booster", {}).get("quantity", 0) > 0 or inventory.get("advanced_signal_booster", {}).get("quantity", 0) > 0) and (inventory.get("emergency_beacon", {}).get("quantity", 0) > 0 or inventory.get("advanced_emergency_beacon", {}).get("quantity", 0) > 0) and not rejected and not abandoned_ship:
        main_mission = 3
    elif (inventory.get("receiver", {}).get("quantity", 0) > 0 or inventory.get("radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0) and (inventory.get("signal_booster", {}).get("quantity", 0) > 0 or inventory.get("advanced_signal_booster", {}).get("quantity", 0) > 0):
        main_mission = 2
    elif (inventory.get("receiver", {}).get("quantity", 0) > 0 or inventory.get("radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0):
        main_mission = 1
    else:
        main_mission = 0
    roll = randint(1, 101)
    if 1 <= roll <= 10:
        if (randint(1,2) == 1 and selected_rest == "fortified_camp") or selected_rest == "advanced_camp":
            event_msg(msg=["A storm hits the island! You are safe in your shelter."], font=("Arial", 16, "bold"))
        elif selected_rest:
            event_msg(msg=["A storm hits the island! You lose 5 health and your shelter was destroyed."], font=("Arial", 16, "bold"))
            inventory[selected_rest]["quantity"] -= 1
            if inventory[selected_rest]["quantity"] <= 0:
                del inventory[selected_rest]
            take_damage(5)
        else:
            event_msg(msg=["A storm hits the island! You lose 10 health."], font=("Arial", 16, "bold"))
            take_damage(10)
    elif 11 <= roll <= 20:
        event_msg(msg=["You found a hidden stash of food! You gain 20 hunger."], font=("Arial", 16, "bold"))
        feed(20)
    elif 21 <= roll <= 30:
        event_village_win = Toplevel(game)
        event_village_win.title("Event")
        event_village_win.geometry("750x550")
        event_village_win.transient(game)
        event_village_win.grab_set()
        event_village_win.protocol("WM_DELETE_WINDOW", blank)
        event_village_win.iconphoto(True, logo)

        # Realistic loot you might find in a small island village

        def has_decent_weapon():
            """True if the player has something stronger than a wooden/stone sword."""
            return selected_sword in ("iron_sword", "diamond_sword", "ruby_sword", "galaxium_sword")

        def opt1():  # Raid the village
            event_village_win.destroy()
            outcome = randint(1, 3)

            if outcome == 1:
                # Clean getaway
                found = roll_loot(village_loot, rolls=8, looting=True)
                if found:
                    lines = [f"{qty} × {item.replace('_', ' ').title()}" for item, qty in found.items()]
                    event_msg(
                        msg=["You slipped through the village unnoticed and grabbed what you could:\n" + "\n".join(lines)]
                    )
                else:
                    event_msg(msg=["You explored the village carefully but found nothing useful."])

            elif outcome == 2:
                # Caught, but fight back
                if has_decent_weapon():
                    found = roll_loot(village_loot, rolls=5, looting=True)
                    take_damage(5)
                    if found:
                        lines = [f"{qty} × {item.replace('_', ' ').title()}" for item, qty in found.items()]
                        event_msg(
                            msg=["The villagers spotted you! You fought them off (lost 5 health) and still escaped with:\n" + "\n".join(lines)]
                        )
                    else:
                        event_msg(
                            msg=["The villagers spotted you! You fought them off but lost 5 health and found nothing."]
                        )
                else:
                    take_damage(20)
                    event_msg(
                        msg=["The villagers caught you raiding their homes. Without a proper weapon you were badly beaten and lost 20 health."]
                    )

            else:
                # Failed completely
                event_msg(msg=["You were spotted early and had to flee empty-handed."])

        def opt2():  # Leave them alone
            event_village_win.destroy()
            event_msg(msg=["You decide to leave the village in peace and continue exploring."])

        event_village = Label(
            event_village_win,
            text="While exploring the island, you stumble upon a small village.\nIt looks well-established and lived-in.",
            font=("Arial", 18, "bold"),
            wraplength=500,
            justify="center"
        )
        event_village.place(relx=0.5, rely=0.4, anchor=CENTER)

        option1 = Button(event_village_win, text="Raid the village", font=("Arial", 16), width=20, command=opt1)
        option1.place(relx=0.33, rely=0.8, anchor=CENTER)
        option2 = Button(event_village_win, text="Leave them alone", font=("Arial", 16), width=20, command=opt2)
        option2.place(relx=0.67, rely=0.8, anchor=CENTER)
    elif 31 <= roll <= 40:
        if main_mission == 1:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)
            event_mission_win.iconphoto(True, logo)
            
            if not (inventory.get("radio", {}).get("quantity", 0) > 0 or inventory.get("transmitter", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_transmitter", {}).get("quantity", 0) > 0) and (inventory.get("receiver", {}).get("quantity", 0) > 0 and inventory.get("advanced_receiver", {}).get("quantity", 0) > 0):
                def opt1():
                    event_mission_win.destroy()
                    event_msg(msg=["You listen to the signal. It's the captain of a cruise ship nearby the island."])
                
                def opt2():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])
                
                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin. However, you have no way to respond.", font=("Arial", 20, "bold"), wraplength=300)
                eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
                option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
                option1.place(relx = 0.5, rely = 0.8, anchor = CENTER)
                option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
                option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
            elif inventory.get("radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_radio", {}).get("quantity", 0) > 0 or ((inventory.get("transmitter", {}).get("quantity", 0) > 0 or inventory.get("advanced_transmitter", {}).get("quantity", 0) > 0) and (inventory.get("receiver", {}).get("quantity", 0) > 0 or inventory.get("advanced_receiver", {}).get("quantity", 0) > 0)):
                def opt1():
                    def opt1a():
                        global mission1
                        event_mission_win.destroy()
                        event_msg(msg=["You begin to speak. Before you can explain the situation, the signal cuts off. The captain doesn't know you are, but he knows you're there."])
                        mission1 = True
                    def opt1b():
                        event_mission_win.destroy()
                        event_msg(msg=["You ignore the signal."])
                    
                    if mission1:
                        event_msg(msg=["You listen to the signal. It's the captain from earlier."])
                    else:
                        event_msg(msg=["You listen to the signal. It's the captain of a cruise ship nearby the island."])
                    option1.config(text="Respond to the signal", command=opt1a)
                    option2.config(text="Ignore the signal", command=opt1b)
                def opt2():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])

                if inventory.get("radio", {}).get("quantity", 0) > 0:
                    eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
                else:
                    eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
                eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
                option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
                option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
                option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
                option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 2:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.iconphoto(True, logo)
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)

            def opt1():
                def opt1a():
                    global mission2
                    event_mission_win.destroy()
                    if abandoned_ship:
                        event_msg(msg=["You begin to speak. You tell the captain about your situation. He doesn't believe you."])
                    elif rejected:
                        event_msg(msg=["You begin to speak. You tell the captain about your situation. He says that he can't help you."])
                    elif mission2:
                        event_msg(msg=["You begin to speak. You tell the captain about your situation. He says he already told you that he can't help you without knowing your current location."])
                        mission2 = True
                    else:
                        event_msg(msg=["You begin to speak. You tell the captain about your situation. He says that he can't help you without knowing your current location."])
                        mission2 = True
                def opt1b():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])

                if mission1 or mission2:
                    eventmission.config(text="You listen to the signal. It's the captain from earlier.")
                else:
                    eventmission.config(text="You listen to the signal. It's the captain of a cruise ship nearby the island.")
                option1.config(text="Respond to the signal", command=opt1a)
                option2.config(text="Ignore the signal", command=opt1b)
            def opt2():
                event_mission_win.destroy()
                event_msg(msg=["You ignore the signal."])
            
            if inventory.get("radio", {}).get("quantity", 0) > 0:
                eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            else:
                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 3:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.iconphoto(True, logo)
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)

            def opt1():
                def opt1a():
                    def opt1aI():
                        global active_beacon, mission3
                        event_mission_win.destroy()
                        event_msg(msg=["You activate the emergency beacon. They know where you are."])
                        inventory["emergency_beacon"]["quantity"] -= 1
                        if inventory["emergency_beacon"]["quantity"] <= 0:
                            del inventory["emergency_beacon"]
                        active_beacon = True
                        mission3 = True
                    def opt1aII():
                        event_mission_win.destroy()
                        event_msg(msg=["You end the transmission."])
                    if mission2:
                        eventmission.config(text="You begin to speak. You tell the captain about your situation. He says he already told you that he can't help you without knowing your current location.")
                    else:
                        eventmission.config(text="You begin to speak. You tell the captain about your situation. He says that he can't help you without knowing your current location.")
                    option1.config(text="Activate the emergency beacon", command=opt1aI)
                    option2.config(text="End the transmission", command=opt1aII)
                def opt1b():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])
            
                if mission1 or mission2:
                    eventmission.config(text="You listen to the signal. It's the captain from earlier.")
                else:
                    eventmission.config(text="You listen to the signal. It's the captain of a cruise ship nearby the island.")
                option1.config(text="Respond to the signal", command=opt1a)
                option2.config(text="Ignore the signal", command=opt1b)
            def opt2():
                event_mission_win.destroy()
                event_msg(msg=["You ignore the signal."])
            
            if inventory.get("radio", {}).get("quantity", 0) > 0:
                eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            else:
                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 4:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            active_beacon = False
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)
            event_mission_win.iconphoto(True, logo)
            
            def opt1():
                global mission4, rejected, escaped
                galaxium_present = False
                for item in list(inventory):
                    if "galaxium" in item or "advanced" in item:
                        galaxium_present = True 
                if galaxium_present:
                    event_mission_win.destroy()
                    event_msg(msg=["You reach the ship. As you board the ship, the captain senses an aura from you. Something alien. Upon this, he prevented you from boarding the ship."])
                    rejected = True
                else:
                    event_mission_win.destroy()
                    event_msg(msg=["You reach the ship and board it. The captain sets sail."])
                    escaped = True
                mission4 = True
            def opt2():
                global abandoned_ship
                event_mission_win.destroy()
                event_msg(msg=["You hide from the ship, making sure they don't see you. After a while, it leaves"])
                abandoned_ship = True

            eventmission = Label(event_mission_win, text="The cruise ship you've been in contact with has arrived at the shore.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Board the ship", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Abandon the ship", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 5:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)
            event_mission_win.iconphoto(True, logo)
            
            if not (inventory.get("advanced_radio", {}).get("quantity", 0) > 0 or inventory.get("advanced_transmitter", {}).get("quantity", 0) > 0) and inventory.get("advanced_receiver", {}).get("quantity", 0) > 0:
                def opt1():
                    event_mission_win.destroy()
                    event_msg(msg=["You listen to the signal. It's the pilot of a UFO above the atmosphere."])
                def opt2():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])

                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin. However, you have no way to respond.", font=("Arial", 20, "bold"), wraplength=300)
                eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
                option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
                option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
                option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
                option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
            elif inventory.get("advanced_radio", {}).get("quantity", 0) > 0 or (inventory.get("advanced_transmitter", {}).get("quantity", 0) > 0 and inventory.get("advanced_receiver", {}).get("quantity", 0) > 0):
                def opt1():
                    def opt1a():
                        global mission5
                        event_mission_win.destroy()
                        event_msg(msg=["You begin to speak. Before you can explain the situation, the signal cuts off. The pilot doesn't know you are, but he knows you're there."])
                        mission5 = True
                    def opt1b():
                        event_mission_win.destroy()
                        event_msg(msg=["You ignore the signal."])
                    
                    if mission5:
                        eventmission.config(text="You listen to the signal. It's the pilot from earlier.")
                    else:
                        eventmission.config(text="You listen to the signal. It's the pilot of a UFO above the atmosphere. He seems to be speaking an alien language, but your device automatically translates.")
                    option1.config(text="Respond to the signal", command=opt1a)
                    option2.config(text="Ignore the signal", command=opt1b)
                def opt2():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])

                if inventory.get("advanced_radio", {}).get("quantity", 0) > 0:
                    eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
                else:
                    eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
                eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
                option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
                option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
                option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
                option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 6:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.iconphoto(True, logo)
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)

            def opt1():
                def opt1a():
                    global mission6
                    event_mission_win.destroy()
                    if abandoned_ufo:
                        event_msg(msg=["You begin to speak. You tell the pilot about your situation. He ignored you."])
                    elif mission6:
                        event_msg(msg=["You begin to speak. You tell the pilot about your situation. He says he already told you that he can't help you without knowing your current location."])
                        mission6 = True
                    else:
                        event_msg(msg=["You begin to speak. You tell the pilot about your situation. He says that he can't help you without knowing your current location."])
                        mission6 = True
                def opt1b():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])

                if mission1 or mission2:
                    eventmission.config(text="You listen to the signal. It's the pilot from earlier.")
                else:
                    eventmission.config(text="You listen to the signal. It's the pilot of a UFO above the atmosphere. He seems to be speaking an alien language, but your device automatically translates.")
                option1.config(text="Respond to the signal", command=opt1a)
                option2.config(text="Ignore the signal", command=opt1b)
            def opt2():
                event_mission_win.destroy()
                event_msg(msg=["You ignore the signal."])
            
            if inventory.get("advanced_radio", {}).get("quantity", 0) > 0:
                eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            else:
                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 7:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            event_mission_win.iconphoto(True, logo)
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)

            def opt1():
                def opt1a():
                    def opt1aI():
                        global active_advanced_beacon, mission7
                        event_mission_win.destroy()
                        event_msg(msg=["You activate the emergency beacon. They know where you are."])
                        inventory["advanced_emergency_beacon"]["quantity"] -= 1
                        if inventory["advanced_emergency_beacon"]["quantity"] <= 0:
                            del inventory["advanced_emergency_beacon"]
                        active_advanced_beacon = True
                        mission7 = True
                    def opt1aII():
                        event_mission_win.destroy()
                        event_msg(msg=["You end the transmission."])
                    if mission6:
                        event_msg(msg=["You begin to speak. You tell the pilot about your situation. He says he already told you that he can't help you without knowing your current location."])
                    else:
                        event_msg(msg=["You begin to speak. You tell the pilot about your situation. He says that he can't help you without knowing your current location."])
                    option1.config(text="Activate the emergency beacon", command=opt1aI)
                    option2.config(text="End the transmission", command=opt1aII)
                def opt1b():
                    event_mission_win.destroy()
                    event_msg(msg=["You ignore the signal."])
            
                if mission5 or mission6:
                    eventmission.config(text="You listen to the signal. It's the pilot from earlier.")
                else:
                    eventmission.config(text="You listen to the signal. It's the pilot of a UFO above the atmosphere.")
                option1.config(text="Respond to the signal", command=opt1a)
                option2.config(text="Ignore the signal", command=opt1b)
            def opt2():
                event_mission_win.destroy()
                event_msg(msg=["You ignore the signal."])
            
            if inventory.get("advanced_radio", {}).get("quantity", 0) > 0:
                eventmission = Label(event_mission_win, text="Your radio is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            else:
                eventmission = Label(event_mission_win, text="Your receiver is picking up a signal with a mysterious origin.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Listen to the signal", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Ignore the signal", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
        elif main_mission == 8:
            event_mission_win = Toplevel(game)
            event_mission_win.title("Event")
            event_mission_win.geometry("750x550")
            event_mission_win.transient(game)
            event_mission_win.grab_set()
            active_advanced_beacon = False
            event_mission_win.protocol("WM_DELETE_WINDOW", blank)
            event_mission_win.iconphoto(True, logo)
            
            def opt1():
                global mission8
                option1.destroy()
                option2.destroy()
                def on_alien_win():
                    global escaped
                    event_mission_win.destroy()
                    event_msg(msg=["The goliath falls. You steal his UFO and fly away."])
                    escaped = True
                def on_alien_lose():
                    event_mission_win.destroy()
                    event_msg(msg=["You fall to the goliath."])

                start = Button(event_mission_win, text="Continue", command=lambda: start_battle("alien_goliath", on_win=on_alien_win, on_lose=on_alien_lose))
                start.pack(pady=15)
                eventmission.config(text="You reach the UFO. Before you can board it, a giant alien exits it. It seems hostile.")
                mission8 = True
            def opt2():
                global abandoned_ufo, mission8
                event_mission_win.destroy()
                event_msg(msg=["You hide from the UFO, making sure he doesn't see you. After a while, it leaves"])
                abandoned_ufo = True
                mission8 = True

            eventmission = Label(event_mission_win, text="The UFO you've been in contact with has arrived at the shore.", font=("Arial", 20, "bold"), wraplength=300)
            eventmission.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            option1 = Button(event_mission_win, text="Board the ship", font=("Arial", 16), width=20, command=opt1)
            option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
            option2 = Button(event_mission_win, text="Abandon the ship", font=("Arial", 16), width=20, command=opt2)
            option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
    elif 41 <= roll <= 50:
        event_animal_win = Toplevel(game)
        event_animal_win.title("Event")
        event_animal_win.geometry("750x550")
        event_animal_win.transient(game)
        event_animal_win.grab_set()
        event_animal_win.protocol("WM_DELETE_WINDOW", blank)
        event_animal_win.iconphoto(True, logo)

        def opt1():
            event_animal_win.destroy()
            start_battle(animal, on_win=on_win, on_lose=on_lose)
        def opt2():
            event_animal_win.destroy()
            event_msg(msg=[f"You ignore the {animal_data[animal]['name']}."])

        animal = choice(list(animal_data.keys()))
        eventanimal = Label(event_animal_win, text=f"While exploring the island, you encounter a {animal_data[animal]['name']}.", font=("Arial", 20, "bold"), wraplength=300)
        eventanimal.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        option1 = Button(event_animal_win, text=f"Fight the {animal_data[animal]['name']}", font=("Arial", 16), width=20, command=opt1)
        option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
        option2 = Button(event_animal_win, text=f"Ignore the {animal_data[animal]['name']}", font=("Arial", 16), width=20, command=opt2)
        option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
    elif 51 <= roll <= 60 and mission8 and not abandoned_ufo:
        event_enemy_win = Toplevel(game)
        event_enemy_win.title("Event")
        event_enemy_win.geometry("750x550")
        event_enemy_win.transient(game)
        event_enemy_win.grab_set()
        event_enemy_win.protocol("WM_DELETE_WINDOW", blank)
        event_enemy_win.iconphoto(True, logo)

        def opt1():
            event_enemy_win.destroy()
            start_battle(enemy, on_win=on_win, on_lose=on_lose)
        def opt2():
            event_enemy_win.destroy()
            event_msg(msg=[f"You ignore the {enemy_data[enemy]['name']}."])

        enemy = choice(list(enemy_data.keys()))
        eventenemy = Label(event_enemy_win, text=f"While exploring the island, you encounter a {enemy_data[enemy]['name']}.", font=("Arial", 20, "bold"), wraplength=300)
        eventenemy.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        option1 = Button(event_enemy_win, text=f"Fight the {enemy_data[enemy]['name']}", font=("Arial", 16), width=20, command=opt1)
        option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
        option2 = Button(event_enemy_win, text=f"Ignore the {enemy_data[enemy]['name']}", font=("Arial", 16), width=20, command=opt2)
        option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)
    elif 61 <= roll <= 70:
        pass
    elif 71 <= roll <= 80:
        pass
    elif 81 <= roll <= 90:
        pass
    elif 91 <= roll <= 100:
        pass
    elif roll == 101 and selected_pickaxe in ["ruby_pickaxe", "galaxium_pickaxe"]:
        event_galaxium_win = Toplevel(game)
        event_galaxium_win.title("Event")
        event_galaxium_win.geometry("750x550")
        event_galaxium_win.transient(game)
        event_galaxium_win.grab_set()
        event_galaxium_win.protocol("WM_DELETE_WINDOW", blank)
        event_galaxium_win.iconphoto(True, logo)

        def opt1():
            event_galaxium_win.destroy()
            event_msg(msg=["The cave was full of a mysterious ore."])
            # Mine as many ores as the current pickaxe still has durability
            pick = selected_pickaxe
            if pick and isinstance(inventory[pick].get("durability"), list) and inventory[pick]["durability"]:
                ores = inventory[pick]["durability"][0]          # only the active pickaxe
                added, actual = add_item("galaxium_ore", amount=ores, cont=True)
                # Wear the pickaxe by the number of ores actually mined
                for _ in range(actual):
                    wear_tool(pick)
            durability_check()

        def opt2():
            event_galaxium_win.destroy()
            event_msg(msg=["You ignored the cave."])

        eventgalaxium = Label(event_galaxium_win, text="While exploring the island, you discovered a mysterious cave.", font=("Arial", 20, "bold"), wraplength=300)
        eventgalaxium.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        option1 = Button(event_galaxium_win, text="Enter the cave", font=("Arial", 16), width=20, command=opt1)
        option1.place(relx = 0.33, rely = 0.8, anchor = CENTER)
        option2 = Button(event_galaxium_win, text="Ignore the cave", font=("Arial", 16), width=20, command=opt2)
        option2.place(relx = 0.67, rely = 0.8, anchor = CENTER)

# ====================== BATTLE DATA ======================

melee_template ={
    "wooden_sword": 2,
    "stone_sword": 5,
    "iron_sword": 15,
    "diamond_sword": 25,
    "ruby_sword": 50,
    "galaxium_sword": 200,
    "wooden_axe": 5,
    "stone_axe": 10,
    "iron_axe": 20,
    "diamond_axe": 30,
    "ruby_axe": 65,
    "galaxium_axe": 250,
    "wooden_spear": 5,
    "stone_spear": 10,
    "iron_spear": 18,
    "diamond_spear": 30,
    "ruby_spear": 75,
    "galaxium_spear": 300
}

ranged_template = {
    # weapon_key: (damage, ammo_item_needed or None)
    "wooden_bow": (5, "arrow"),
    "stone_bow": (10, "arrow"),
    "iron_bow": (18, "arrow"),
    "diamond_bow": (30, "arrow"),
    "ruby_bow": (75, "arrow"),
    "galaxium_bow": (300, "arrow"),
    "wooden_spear": (5, None),
    "stone_spear": (10, None),
    "iron_spear": (18, None),
    "diamond_spear": (30, None),
    "ruby_spear": (75, None),
    "galaxium_spear": (300, None),
    "blaster": (350, None),
    "omega_blaster": (500, None)
}

# How many arrows / ammo the player starts with when they craft/find them
# (you can expand this later)
ammo_items = {"arrow"}

animal_data = {
    "wild_boar": {
        "name": "Wild Boar",
        "max_hp": 70,
        "reaction_time": 55,          # higher = harder for it to dodge
        "attack_speed": 1.0,          # multiplier for QTE time
        "attacks": [
            {"name": "Claw Swipe", "damage": 11, "type": "melee"},
            {"name": "Charge", "damage": 14, "type": "melee"},
            {"name": "Tusk Gore", "damage": 18, "type": "melee"},
        ],
        "drops": {
            "raw_meat": 0.6,
            "hide": 0.2,
            "tusk": 0.2
        }
    },
    "island_wolf": {
        "name": "Island Wolf",
        "max_hp": 55,
        "reaction_time": 35,
        "attack_speed": 1.4,
        "attacks": [
            {"name": "Bite", "damage": 12, "type": "melee"},
            {"name": "Claw Swipe", "damage": 14, "type": "melee"},
            {"name": "Pounce", "damage": 16, "type": "melee"},
        ],
        "drops": {
            "raw_meat": 0.5,
            "fur": 0.5
        }
    },
    "giant_crab": {
        "name": "Giant Crab",
        "max_hp": 110,
        "reaction_time": 70,
        "attack_speed": 0.8,
        "attacks": [
            {"name": "Claw Snap", "damage": 20, "type": "melee"},
            {"name": "Shell Bash", "damage": 25, "type": "melee"},
        ],
        "drops": {
            "raw_meat": 0.7,
            "shell": 0.3
        }
    },
    "island_snake": {
        "name": "Island Snake",
        "max_hp": 40,
        "reaction_time": 30,
        "attack_speed": 1.5,
        "attacks": [
            {"name": "Bite", "damage": 10, "type": "melee"},
            {"name": "Venom Spit", "damage": 15, "type": "ranged"},
        ],
        "drops": {}
    },
    "komodo_dragon": {
        "name": "Komodo Dragon",
        "max_hp": 120,
        "reaction_time": 50,
        "attack_speed": 1.2,
        "attacks": [
            {"name": "Claw Swipe", "damage": 13, "type": "melee"},
            {"name": "Bite", "damage": 18, "type": "melee"},
            {"name": "Venom Spit", "damage": 20, "type": "ranged"},
            {"name": "Tail Whip", "damage": 22, "type": "melee"},
        ],
        "drops": {}
    }
}

enemy_data = {
    "alien_goliath": {
        "name": "Alien Goliath",
        "max_hp": 500,
        "reaction_time": 15,
        "attack_speed": 4.2,
        "attacks": [
            {"name": "Gamma Punch", "damage": 35, "type": "melee"},
            {"name": "Stomp", "damage": 40, "type": "melee"},
            {"name": "Omega Blaster", "damage": 50, "type": "ranged"},
        ],
        "drops": {
            "raw_meat": 0.5,
            "omega_blaster": 0.005
        }
    },
    "alien_troop": {
        "name": "Alien Troop",
        "max_hp": 300,
        "reaction_time": 20,
        "attack_speed": 3.0,
        "attacks": [
            {"name": "Kick", "damage": 13, "type": "melee"},
            {"name": "Super Punch", "damage": 20, "type": "melee"},
            {"name": "Headbutt", "damage": 25, "type": "melee"},
            {"name": "Blaster", "damage": 31, "type": "ranged"},
        ],
        "drops": {
            "raw_meat": 0.3,
            "blaster": 0.01
        }
    },
}

def on_win(enemy):
    found = roll_loot(enemy["drops"], rolls=5, looting=True, cont=True)
    if found:
        lines = [f"{qty} × {item.replace('_', ' ').title()}" for item, qty in found.items()]
        event_msg(msg=[f"You defeated the {enemy['name']} and got:\n{'\n'.join(lines)}"])

def on_lose(enemy):
    event_msg(msg=[f"The {enemy['name']} left you badly wounded..."])

durability_template = {
    "wooden_axe": 20,
    "wooden_pickaxe": 20,
    "wooden_sword": 20,
    "wooden_spear": 20,
    "wooden_bow": 20,
    "stone_pickaxe": 50,
    "stone_axe": 50,
    "stone_sword": 50,
    "stone_spear": 50,
    "stone_bow": 50,
    "iron_pickaxe": 75,
    "iron_axe": 75,
    "iron_sword": 75,
    "iron_spear": 75,
    "iron_bow": 75,
    "diamond_pickaxe": 150,
    "diamond_axe": 150,
    "diamond_sword": 150,
    "diamond_spear": 150,
    "diamond_bow": 150,
    "ruby_pickaxe": 250,
    "ruby_axe": 250,
    "ruby_sword": 250,
    "ruby_spear": 250,
    "ruby_bow": 250,
    "galaxium_pickaxe": 500,
    "galaxium_axe": 500,
    "galaxium_sword": 500,
    "galaxium_spear": 500,
    "galaxium_bow": 500,
    "blaster": 500,
    "omega_blaster": 500
}

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
            "raw_meat": 1,
            "wooden_log": 1
        },
        "requirements": "campfire",
        "quantity": 1
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
            "iron_ingot": 1,
            "antenna": 1
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
            "lemon": 1
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
    },
    "campfire": {
        "ingredients": {
            "wooden_log": 4,
            "stick": 2,
            "flint": 2
        },
        "requirements": None,
        "quantity": 1
    },
    "bedroll": {
        "ingredients": {
            "fibre": 4,
            "vine": 2,
            "large_leaf": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "rope": {
        "ingredients": {
            "fibre": 3
        },
        "requirements": None,
        "quantity": 1
    },
    "shelter": {
        "ingredients": {
            "wooden_log": 8,
            "large_leaf": 4,
            "vine": 4,
            "bedroll": 1
        },
        "requirements": None,
        "quantity": 1
    },
    "improved_shelter": {
        "ingredients": {
            "shelter": 1,
            "large_leaf": 2,
            "wooden_plank": 4
        },
        "requirements": None,
        "quantity": 1
    },
    "fortified_camp": {
        "ingredients": {
            "improved_shelter": 1,
            "iron_ingot": 4,
            "wooden_plank": 2
        },
        "requirements": None,
        "quantity": 1
    },
    "advanced_camp": {
        "ingredients": {
            "fortified_camp": 1,
            "galaxium": 4,
            "ruby": 2,
            "diamond": 1
        },
        "requirements": None,
        "quantity": 1
    },
    "bucket_with_fresh_water": {
        "ingredients": {
            "bucket_with_salt_water": 1,
            "wooden_log": 1
        },
        "requirements": "campfire",
        "quantity": 1
    },
    "bowl_with_fresh_water": {
        "ingredients": {
            "bowl_with_salt_water": 1,
            "wooden_log": 1
        },
        "requirements": "campfire",
        "quantity": 1
    },
    "coconut_shell_with_fresh_water": {
        "ingredients": {
            "coconut_shell_with_salt_water": 1,
            "wooden_log": 1
        },
        "requirements": "campfire",
        "quantity": 1
    },
    "coconut_shell": {
        "ingredients": {
            "coconut": 1
        },
        "requirements": None,
        "quantity": 2
    },
    "bowl": {
        "ingredients": {
            "clay": 3
        },
        "requirements": "furnace",
        "quantity": 1
    },
    "bucket": {
        "ingredients": {
            "iron_ingot": 3
        },
        "requirements": None,
        "quantity": 1
    },
    "coconut_shell_with_orange_juice": {
        "ingredients": {
            "coconut_shell": 1,
            "orange": 5
        },
        "requirements": None,
        "quantity": 1
    },
    "bowl_with_orange_juice": {
        "ingredients": {
            "bowl": 1,
            "orange": 10
        },
        "requirements": None,
        "quantity": 1
    },
    "bucket_with_orange_juice":{
        "ingredients": {
            "bucket": 1,
            "orange": 20
        },
        "requirements": None,
        "quantity": 1
    },
    "coconut_shell_with_apple_juice": {
        "ingredients": {
            "coconut_shell": 1,
            "apple": 5
        },
        "requirements": None,
        "quantity": 1
    },
    "bowl_with_apple_juice": {
        "ingredients": {
            "bowl": 1,
            "apple": 10
        },
        "requirements": None,
        "quantity": 1
    },
    "bucket_with_apple_juice":{
        "ingredients": {
            "bucket": 1,
            "apple": 15
        },
        "requirements": None,
        "quantity": 1
    },
    "coconut_shell_with_lemon_juice": {
        "ingredients": {
            "coconut_shell": 1,
            "lemon": 5
        },
        "requirements": None,
        "quantity": 1
    },
    "bowl_with_lemon_juice": {
        "ingredients": {
            "bowl": 1,
            "lemon": 10
        },
        "requirements": None,
        "quantity": 1
    },
    "bucket_with_lemon_juice":{
        "ingredients": {
            "bucket": 1,
            "lemon": 15
        },
        "requirements": None,
        "quantity": 1
    },
    "bandage": {
        "ingredients": {
            "fibre": 3,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "herbal_medicine": {
        "ingredients": {
            "leaf": 2,
            "coconut": 1
        },
        "requirements": "crafting_bench",
        "quantity": 2
    },
    "leather": {
        "ingredients": {
            "hide": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "small_backpack": {
        "ingredients": {
            "fibre": 4,
            "leather": 2,
            "vine": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "large_backpack": {
        "ingredients": {
            "leather": 6,
            "fibre": 4,
            "rubber": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "tactical_backpack": {
        "ingredients": {
            "leather": 8,
            "rubber": 4,
            "cloth": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "antenna": {
        "ingredients": {
            "iron_ingot": 2,
            "wire": 3,
            "rubber": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "signal_booster": {
        "ingredients": {
            "circuit": 2,
            "wire": 4,
            "iron_ingot": 2,
            "rubber": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "emergency_beacon": {
        "ingredients": {
            "transmitter": 1,
            "circuit": 2,
            "wire": 4,
            "iron_ingot": 2,
            "battery": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "wooden_bow": {
        "ingredients": {
            "wooden_log": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "wooden_spear": {
        "ingredients": {
            "wooden_log": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
	"stone_bow": {
        "ingredients": {
            "rock": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "stone_spear": {
        "ingredients": {
            "rock": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
	"iron_bow": {
        "ingredients": {
            "iron_ingot": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "iron_spear": {
        "ingredients": {
            "iron_ingot": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
	"diamond_bow": {
        "ingredients": {
            "diamond": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "diamond_spear": {
        "ingredients": {
            "diamond": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
	"ruby_bow": {
        "ingredients": {
            "ruby": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "ruby_spear": {
        "ingredients": {
            "ruby": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
	"galaxium_bow": {
        "ingredients": {
            "galaxium": 2,
            "stick": 1,
            "vine": 1,
			"rope": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "galaxium_spear": {
        "ingredients": {
            "galaxium": 1,
            "stick": 2,
            "vine": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "arrow": {
        "ingredients": {
            "stick": 1,
            "flint": 1,
            "feather": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "advanced_radio": {
        "ingredients": {
            "advanced_receiver": 1,
            "advanced_transmitter": 1,
            "galaxium": 2,
            "circuit": 1,
            "wire": 2,
            "battery": 1
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "advanced_receiver": {
        "ingredients": {
            "receiver": 1,
            "galaxium": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "advanced_transmitter": {
        "ingredients": {
            "transmitter": 1,
            "galaxium": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "advanced_signal_booster": {
        "ingredients": {
            "signal_booster": 1,
            "galaxium": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    },
    "advanced_emergency_beacon": {
        "ingredients": {
            "emergency_beacon": 1,
            "galaxium": 2
        },
        "requirements": "crafting_bench",
        "quantity": 1
    }
    
}
food_template = {
    "apple": 5,
    "raw_meat": 15,
    "cooked_meat": 25,
    "lemon": 5,
    "coconut": 10,
    "orange": 5,
    "herbal_medicine": 0
}

drink_template = {
    "coconut_shell_with_salt_water": -5,
    "coconut_shell_with_fresh_water": 10,
    "bowl_with_salt_water": -10,
    "bowl_with_fresh_water": 25,
    "bucket_with_salt_water": -20,
    "bucket_with_fresh_water": 50,
    "coconut": 5,
    "coconut_shell_with_orange_juice": 5,
    "bowl_with_orange_juice": 10,
    "bucket_with_orange_juice": 20,
    "coconut_shell_with_apple_juice": 5,
    "bowl_with_apple_juice": 10,
    "bucket_with_apple_juice": 20,
    "coconut_shell_with_lemon_juice": 5,
    "bowl_with_lemon_juice": 10,
    "bucket_with_lemon_juice": 20,
    "apple": 5,
    "lemon": 5,
    "orange": 5
}

item_descriptions = {
    # Raw materials
    "rock": "It's a rock", "stick": "It's a stick", "vine": "Good for binding things together", "wooden_log": "It's wood",
    "wooden_plank": "It's wood but processed", "leaf": "It's a leaf", "large_leaf": "It's a bigger leaf",
    "fibre": "It's fibre (this means something apparently)", "flint": "No steel", "feather": "It's a feather",
    "rubber": "Good for insulation", "clay": "Malleable", "cloth": "It's cloth", "hide": "Skin", "fur": "Hair",
    "leather": "Tanned animal hide\nReliable material", "tusk": "When you neglect denistry", "shell": "Someone's home",
    "iron_ore": "Reliable metal\nKinda useless as an ore", "copper_ore": "Good for electronics\nKinda useless as an ore",
    "diamond_ore": "Blue gem\nKinda useless as an ore", "ruby_ore": "Red gem\nKinda useless as an ore",
    "galaxium_ore": "Metal from the cosmos\nKinda useless as an ore", "iron_ingot": "Reliable metal",
    "copper_ingot": "Good for electronics", "diamond": "Blue gem", "ruby": "Red gem", "galaxium": "Metal from the cosmos",
    "wire": "Good for electronics", "circuit": "Good for electronics",

    # Food
    "apple": "Keeps the doctor away", "orange": "It's an orange", "lemon": "It's a lemon", "coconut": "It's a coconut",
    "raw_meat": "I wouldn't risk eating that", "cooked_meat": "Medium rare", "herbal_medicine": "Treat illnesses",

    # Drinks and containers
    "coconut_shell": "Half a coconut", "bowl": "It's a bowl", "bucket": "It's a bucket", "coconut_shell_with_salt_water": "It's a coconut shell with salt water", "bowl_with_salt_water": "It's a bowl with salt water",
    "bucket_with_salt_water": "It's a bucket with salt water", "coconut_shell_with_fresh_water": "It's a coconut shell with fresh water", "bowl_with_fresh_water": "It's a bowl with fresh water",
    "bucket_with_fresh_water": "It's a bucket with fresh water", "coconut_shell_with_apple_juice": "It's a coconut shell with apple juice", "bowl_with_apple_juice": "It's a bowl with apple juice", "bucket_with_apple_juice": "It's a bucket with apple juice",
    "coconut_shell_with_orange_juice": "It's a coconut shell with orange juice", "bowl_with_orange_juice": "It's a bowl with orange juice", "bucket_with_orange_juice": "It's a bucket with orange juice",
    "coconut_shell_with_lemon_juice": "It's a coconut shell with lemon juice", "bowl_with_lemon_juice": "It's a bowl with lemon juice", "bucket_with_lemon_juice": "It's a bucket with lemon juice",

    # Tools
    "wooden_pickaxe": "Minecraft YouTubers love people who use this", "stone_pickaxe": "Minecraft YouTubers love people who use this", "iron_pickaxe": "Minecraft YouTubers love people who use this", "diamond_pickaxe": "Minecraft YouTubers love people who use this", "ruby_pickaxe": "Minecraft YouTubers love people who use this", "galaxium_pickaxe": "Minecraft YouTubers love people who use this",
    "wooden_axe": "Chop chop chop", "stone_axe": "Chop chop chop", "iron_axe": "Chop chop chop", "diamond_axe": "Chop chop chop", "ruby_axe": "Chop chop chop", "galaxium_axe": "Chop Away At My Heart",

    # Weapons
    "wooden_sword": "It's a sword", "stone_sword": "It's a sword", "iron_sword": "It's a sword", "diamond_sword": "It's a sword", "ruby_sword": "It's a sword", "galaxium_sword": "It's a sword",
    "wooden_spear": "Thrust and throw", "stone_spear": "Thrust and throw", "iron_spear": "Thrust and throw", "diamond_spear": "Thrust and throw", "ruby_spear": "Thrust and throw", "galaxium_spear": "Thrust and throw",
    "wooden_bow": "Arrows not included", "stone_bow": "Arrows not included", "iron_bow": "Arrows not included", "diamond_bow": "Arrows not included", "ruby_bow": "Arrows not included", "galaxium_bow": "Arrows not included", "arrow": "Bullseye",
    "blaster": "Pew pew", "omega_blaster": "PEW PEW",

    # Stations and shelters
    "crafting_bench": "The heart of crafting", "furnace": "Melting", "campfire": "Stove", "bedroll": "Bad night's rest", "shelter": "Good night's rest", "improved_shelter": "Safety first", "fortified_camp": "Fortress",
    "advanced_camp": "Superstructure",

    # Utility
    "bandage": "Patch that up", "rope": "Thick string", "small_backpack": "More storage", "large_backpack": "MORE storage", "tactical_backpack": "MORE STORAGE",

    # Comms
    "antenna": "Receive signals", "battery": "Power source", "receiver": "Listen for messages", "transmitter": "Send messages", "radio": "Communicate over distances", "signal_booster": "Enhance signal strength", "emergency_beacon": "Call for help",
    "advanced_receiver": "Listen for advanced signals", "advanced_transmitter": "Send advanced messages", "advanced_radio": "Communicate with advanced technology", "advanced_signal_booster": "Enhance advanced signal strength",
    "advanced_emergency_beacon": "Call for advanced help",
}

container_for_water = {
    "coconut_shell_with_salt_water": "coconut_shell",
    "bowl_with_salt_water": "bowl",
    "bucket_with_salt_water": "bucket"
}

day = 0

scavenge_chance = {
    "base": {
        "rock": 0.35,
        "stick": 0.4,
        "vine": 0.35,
        "apple": 0.15,
        "lemon": 0.15,
        "raw_meat": 0.1,
        "wooden_pickaxe": 0.05,
        "wooden_axe": 0.05,
        "stone_pickaxe": 0.01,
        "stone_axe": 0.01,
        "flint": 0.15,
        "coconut": 0.2,
        "leaf": 0.5,
        "feather": 0.1,
        "clay": 0.15
    },
    "wooden_axe": {
        "stick": 0.5,
        "vine": 0.5,
        "apple": 0.3,
        "lemon": 0.3,
        "wooden_log": 0.5,
        "large_leaf": 0.05,
        "fibre": 0.02,
        "coconut": 0.2,
        "leaf": 0.6
    },
    "wooden_pickaxe": {
        "rock": 0.5,
        "flint": 0.2
    },
    "stone_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.02,
        "flint": 0.25
    },
    "stone_axe": {
        "stick": 0.55,
        "vine": 0.5,
        "apple": 0.3,
        "lemon": 0.3,
        "wooden_log": 0.6,
        "rubber": 0.02,
        "large_leaf": 0.1,
        "fibre": 0.05,
        "coconut": 0.25,
        "leaf": 0.7
    },
    "iron_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.1,
        "diamond": 0.02,
        "copper_ore": 0.05,
        "flint": 0.5
    },
    "iron_axe": {
        "stick": 0.6,
        "vine": 0.51,
        "apple": 0.32,
        "lemon": 0.32,
        "wooden_log": 0.6,
        "rubber": 0.05,
        "large_leaf": 0.2,
        "fibre": 0.1,
        "coconut": 0.5,
        "leaf": 0.8
    },
    "diamond_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.2,
        "diamond_ore": 0.1,
        "ruby_ore": 0.02,
        "copper_ore": 0.1,
        "flint": 0.7
    },
    "diamond_axe": {
        "stick": 0.7,
        "vine": 0.6,
        "apple": 0.5,
        "lemon": 0.5,
        "wooden_log": 0.7,
        "rubber": 0.1,
        "large_leaf": 0.35,
        "fibre": 0.2,
        "coconut": 0.7,
        "leaf": 0.9
    },
    "ruby_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.5,
        "diamond_ore": 0.2,
        "ruby_ore": 0.1,
        "copper_ore": 0.2,
        "flint": 0.8
    },
    "ruby_axe": {
        "stick": 0.85,
        "vine": 0.7,
        "apple": 0.5,
        "lemon": 0.5,
        "wooden_log": 0.85,
        "rubber": 0.2,
        "large_leaf": 0.5,
        "fibre": 0.4,
        "coconut": 0.8,
        "leaf": 0.95
    },
    "galaxium_pickaxe": {
        "rock": 0.6,
        "iron_ore": 0.8,
        "diamond_ore": 0.5,
        "ruby_ore": 0.2,
        "copper_ore": 0.5,
        "flint": 1
    },
    "galaxium_axe": {
        "stick": 1,
        "vine": 0.8,
        "apple": 0.6,
        "lemon": 0.6,
        "wooden_log": 1,
        "rubber": 0.5,
        "large_leaf": 0.8,
        "fibre": 0.5,
        "coconut": 1,
        "leaf": 1
    },
    "coconut_shell": {
        "coconut_shell_with_salt_water": 0.1
    },
    "bowl": {
        "bowl_with_salt_water": 0.1
    },
    "bucket": {
        "bucket_with_salt_water": 0.1
    }
}

village_loot = {
    # Common food & drink
    "apple": 0.45,
    "orange": 0.40,
    "lemon": 0.35,
    "coconut": 0.40,
    "cooked_meat": 0.30,
    "raw_meat": 0.15,

    # Basic materials
    "wooden_log": 0.35,
    "stick": 0.40,
    "vine": 0.30,
    "fibre": 0.25,
    "leaf": 0.20,
    "large_leaf": 0.15,
    "rope": 0.12,
    "clay": 0.17,

    # Containers
    "coconut_shell": 0.20,
    "bowl": 0.12,
    "bucket": 0.05,

    # Useful items
    "bandage": 0.15,
    "herbal_medicine": 0.10,
    "leather": 0.12,
    "cloth": 0.08,

    # Weapons / tools (rarer)
    "wooden_sword": 0.08,
    "stone_sword": 0.04,
    "iron_sword": 0.015,
    "wooden_axe": 0.06,
    "stone_axe": 0.03,

    # Rare extras
    "iron_ingot": 0.04,
    "battery": 0.02,
    "wire": 0.03
}

washed_up = {
    "wooden_log": 0.35,
    "stick": 0.4,
    "vine": 0.3,
    "leaf": 0.2,
    "large_leaf": 0.15,
    "coconut": 0.1,
    "clay": 0.2
}

health = 100
stamina = 100
hydration = 100
hunger = 100
sick = 0

rejected = False
active_beacon = False
active_advanced_beacon = False
abandoned_ship = False
abandoned_ufo = False
mission1 = False
mission2 = False
mission3 = False
mission4 = False
mission5 = False
mission6 = False
mission7 = False
mission8 = False
main_mission = 0
selected_pickaxe = None
selected_axe = None
selected_sword = None
selected_container = None
selected_rest = None


inv_max = 15
inventory = {}

# --- 1. Initialize Root Window ---
game = Tk()
try:
    logo = PhotoImage(file=resource_path("IslandSurvivallogo.png"))
except:
    logo = None

try:
    pfp1 = Image.open(resource_path("pfp.png"))
    pfp1 = pfp1.resize((300, 300), Image.Resampling.LANCZOS)
    pfp = ImageTk.PhotoImage(pfp1)
except:
    pfp = None


game.iconphoto(True, logo)

game.title("Island Survival")
game.iconphoto(True, logo)
game.protocol("WM_DELETE_WINDOW", quit_game)
game.geometry("1920x1080")
# Note: We don't zoom or show the window yet. We wait for the menu.

# --- 2. Wrap UI Setup in a Function ---
def setup_game_ui():
    global healthbar, health_bar, hp, staminabar, stamina_bar, sp
    global hungerbar, hunger_bar, hup, hydrationbar, hydration_bar, hyp
    global scav, inv, craft, day_counter, sick_lbl, menubar
    
    # Menubar
    menubar = Menu(game)
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Save', command=save_game)
    file_menu.add_command(label='Save As', command=lambda: save_game(new=True))
    file_menu.add_command(label='Load Save', command=load_game)
    menubar.add_command(label='Quit', command=quit_game)
    menubar.add_command(label="Wiki", command=lambda: link("https://github.com/TrayVerse-Studios/Island-Survival/wiki"))
    game.config(menu=menubar)
    
    healthbar = Canvas(game, width=200, height=25, bg="#c0392b", highlightthickness=0)
    healthbar.place(relx = 0.18, rely = 0.05, anchor = "w")
    health_bar = healthbar.create_rectangle(0, 0, 200, 25, fill="#2ecc71", width=0)
    hp = Label(game, text = f"Health: {health}%", font=("Arial", 20, "bold"))
    hp.place(relx = 0, rely = 0.05, anchor = "w")
    
    staminabar = Canvas(game, width=200, height=25, bg="#2c3e50", highlightthickness=0)
    staminabar.place(relx = 0.18, rely = 0.1, anchor = "w")
    stamina_bar = staminabar.create_rectangle(0, 0, 200, 25, fill="#f1c40f", width=0)
    sp = Label(game, text = f"Stamina: {stamina}%", font=("Arial", 20, "bold"))
    sp.place(relx = 0, rely = 0.1, anchor = "w")
    
    hungerbar = Canvas(game, width=200, height=25, bg="#5d4e37", highlightthickness=0)
    hungerbar.place(relx = 0.18, rely = 0.15, anchor = "w")
    hunger_bar = hungerbar.create_rectangle(0, 0, 200, 25, fill="#e67e22", width=0)
    hup = Label(game, text = f"Hunger: {hunger}%", font=("Arial", 20, "bold"))
    hup.place(relx = 0, rely = 0.15, anchor = "w")
    
    hydrationbar = Canvas(game, width=200, height=25, bg="#1a5276", highlightthickness=0)
    hydrationbar.place(relx = 0.18, rely = 0.2, anchor = "w")
    hydration_bar = hydrationbar.create_rectangle(0, 0, 200, 25, fill="#3498db", width=0)
    hyp = Label(game, text = f"Hydration: {hydration}%", font=("Arial", 20, "bold"))
    hyp.place(relx = 0, rely = 0.2, anchor = "w")
    
    scav = Button(game, text="Scavenge", command=scavenge, font=("Arial", 20, "bold"))
    scav.place(relx = 1, rely = 0.05, anchor = "e")
    
    inv = Button(game, text="Inventory", command=invsee, font=("Arial", 20, "bold"))
    inv.place(relx = 1, rely = 0.15, anchor = "e")
    
    craft = Button(game, text="Crafting", command=crafting, font=("Arial", 20, "bold"))
    craft.place(relx=1, rely=0.25, anchor="e")

    day_counter = Label(game, text = f"Day {day}", font=("Arial", 20, "bold"))
    day_counter.place(relx = 0.5, rely = 0.05, anchor = CENTER)
    sick_lbl = Label(game, text="SICK", font=("Arial", 20, "bold"), fg="#94b21c")

def destroy_game_ui():
    global healthbar, health_bar, hp, staminabar, stamina_bar, sp
    global hungerbar, hunger_bar, hup, hydrationbar, hydration_bar, hyp
    global scav, inv, craft, day_counter, sick_lbl, menubar
    
    # Menubar
    game.config(menu=None)
    
    healthbar.destroy()
    hp.destroy()
    
    staminabar.destroy()
    sp.destroy()
    
    hungerbar.destroy()
    hup.destroy()
    
    hydrationbar.destroy()
    hyp.destroy()
    
    scav.destroy()
    
    inv.destroy()
    
    craft.destroy()

    day_counter.destroy()
    sick_lbl.destroy()

# --- 3. Create the Main Menu ---

wait_var = BooleanVar(value=False)
alive = True
escaped = False
sicklbl = False

def start_menu():
    menu_win = Toplevel(game)
    menu_win.title("Main Menu")
    menu_win.configure(bg="#222222")
    menu_win.grab_set()
    menu_win.focus_force()
    menu_win.iconphoto(True, logo)
    menu_win.geometry("1920x1080")
    menu_win.state("zoomed")
    menu_win.iconphoto(True, logo)

    Label(
        menu_win, image=logo, bg="#222222"
    ).place(relx=0.75, rely=0.5, anchor=CENTER)

    Label(
        menu_win, image=pfp, bg="#222222"
    ).place(relx=0.25, rely=0.75, anchor=CENTER)

    Label(
        menu_win,
        text="ISLAND SURVIVAL",
        font=("Arial", 36, "bold"),
        bg="#222222",
        fg="#eeeeee"
    ).place(relx=0.25, rely=0.1, anchor=CENTER)

    def on_new_game():
        menu_win.destroy()
        play_game(new=True)

    def on_load_game():
        if load_game():
            menu_win.destroy()
            play_game(new=False)

    def on_quit():
        game.destroy()

    Button(menu_win, text="New Game", font=("Arial", 20), width=15,
              command=on_new_game).place(relx=0.25, rely=0.3, anchor=CENTER)
    Button(menu_win, text="Load Game", font=("Arial", 20), width=15,
              command=on_load_game).place(relx=0.25, rely=0.4, anchor=CENTER)
    Button(menu_win, text="Quit", font=("Arial", 20), width=15,
              command=on_quit).place(relx=0.25, rely=0.5, anchor=CENTER)

# Hide the empty game window only AFTER the menu exists
game.withdraw()
start_menu()
game.mainloop()