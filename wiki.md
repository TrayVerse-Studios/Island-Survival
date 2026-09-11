# Island Survival Wiki

A player guide to surviving the island, crafting your way out, and going home.

---

## Contents

1. [Goal](#goal)
2. [Main Menu](#main-menu)
3. [Difficulty](#difficulty)
4. [The Screen](#the-screen)
5. [Stats](#stats)
6. [How a Day Works](#how-a-day-works)
7. [Inventory](#inventory)
8. [Selecting Tools](#selecting-tools)
9. [Scavenging](#scavenging)
10. [Crafting](#crafting)
11. [Food, Water, and Medicine](#food-water-and-medicine)
12. [Shelters and Rest](#shelters-and-rest)
13. [Combat](#combat)
14. [Random Events](#random-events)
15. [Rescue Missions](#rescue-missions)
16. [Saving and Loading](#saving-and-loading)
17. [Item Catalog](#item-catalog)
18. [Tips](#tips)

---

## Goal

You wake up on a desert island with no supplies and no memory of how you got there.

You win by **escaping**. You lose if **Health** reaches 0.

There are two escape routes:

- **Cruise ship** — craft a receiver or radio, a signal booster, and an emergency beacon. Talk to the captain, activate the beacon, then board when the ship arrives. Do **not** be carrying galaxium items or advanced devices when you board, or the captain will refuse you.
- **UFO** — after the ship path is blocked or abandoned, craft the advanced versions of those devices. Call the pilot, activate the advanced beacon, then fight the Alien Goliath and take the craft.

Until you escape, every day is about staying alive: food, water, stamina, shelter, and better tools.

---

## Main Menu

| Button | What it does |
| --- | --- |
| **New Game** | Starts a fresh run. You pick a difficulty, then begin at Day 0 with empty inventory and full stats. |
| **Load Game** | Opens a saved `.json` file and continues that run (including its stored difficulty). |
| **Quit** | Closes the game. |

On a new game you may find a small pile of materials washed up on the shore (about a 1-in-5 chance). That is luck, not a guarantee.

If you have never saved before, the game offers to open the online wiki for tips.

Saves are stored in `Documents/IslandSurvivalSaves` by default.

---

## Difficulty

Chosen once at the start of a new game. It is stored in the save.

| Setting | Multiplier |
| --- | --- |
| Very Easy | 0.5 |
| Easy | 0.75 |
| Normal | 1 |
| Hard | 1.25 |
| Very Hard | 1.5 |

The multiplier scales:

- Damage you take (storms, thirst, starvation, sickness, combat hits that land)
- Daily thirst
- Hunger lost when converting food into stamina
- How fast sickness builds when something makes you ill
- How tired scavenging makes you
- Enemy health, reaction, and attack speed in combat

Healing, eating, drinking, and rest bonuses are **not** scaled. A bandage still heals 5. Cooked meat still gives 25 hunger.

On Normal, the numbers in this wiki are exact. On harder settings, plan more water and a stronger camp.

---

## The Screen

While a run is active you will see:

- **Health, Stamina, Hunger, Hydration** bars in the top left
- **Day** counter in the top centre
- **SICK** label if you are ill
- **Scavenge**, **Inventory**, and **Crafting** on the right
- **Advance** at the bottom — this ends the current day
- **File** menu: Save, Save As, Load Save
- **Quit** — asks to confirm, then saves if you already have a file (or offers Save As)
- **Wiki** — opens the project's GitHub wiki in a browser

You can scavenge, open inventory, and craft as many times as you want **during** a day, as long as you have the stamina and space. Press **Advance** only when you are ready for the next day and its event.

Event and choice windows must be closed with their own buttons. The window close (X) button is disabled on those popups so you cannot skip them by accident.

---

## Stats

All four bars run from **0 to 100**.

### Health

Your life. At 0 the run ends.

Health is lost from:

- Storms (10, or 5 if your shelter is destroyed)
- Dehydration (40 if Hydration is already 0 at the daily thirst tick)
- Starvation (8 if Hunger is 0 and you cannot convert food into stamina)
- Sickness (10 per sick morning)
- Combat and some village outcomes

Those losses are multiplied by difficulty.

Health is restored by **herbal medicine** (+15) and **bandages** (+5).

### Stamina

Energy for work. **Scavenging costs 5 stamina** (scaled by difficulty).

Each morning:

- If you have a selected rest item, you have a 50% chance to wake well-rested and gain bonus stamina **without** spending hunger:
  - Bedroll: 1–10
  - Shelter: 11–20
  - Improved Shelter: 21–30
  - Fortified Camp: 31–40
  - Advanced Camp: 41–50
- Then the game tries to convert up to **5 Hunger into 5 Stamina** (only as much as you can actually use)

If Hunger is 0 and you still needed that conversion, you take starvation damage instead.

### Hunger

How well fed you are. Eating food raises it. Daily stamina conversion lowers it.

Eat from Inventory with **Consume**. Nutrition values are listed in the [Item Catalog](#item-catalog).

### Hydration

How thirsty you are. Every morning you lose **5 Hydration** (scaled by difficulty). If you are already at 0, you also lose **40 Health** (also scaled).

Drink fresh water or juice. Salt water **lowers** Hydration. Fruit also gives a little water.

### Sickness

A hidden counter. While it is above 0:

- The **SICK** label appears
- You lose 10 Health each morning (scaled by difficulty)
- The counter drops by 1 each morning

Raw meat has a 30% chance per consume action to add sickness (2 per serving, scaled up on harder difficulties). **Herbal medicine** heals 15 Health and reduces sickness by 4 per serving.

---

## How a Day Works

1. You act: scavenge, craft, eat, drink, choose tools.
2. You press **Advance**.
3. The day number goes up.
4. Sickness ticks.
5. Rest bonus may apply.
6. Thirst ticks. Dehydration damage if Hydration is 0.
7. Hunger converts into stamina, or you take starvation damage.
8. A random event is rolled.
9. Repeat until you die or escape.

Nothing on the island is on a timer except this day loop. If you are low on water or food, deal with that **before** you Advance.

---

## Inventory

Default capacity is **15** items. Every single object counts as 1 space, including each tool.

| Backpack | Capacity |
| --- | --- |
| None | 15 |
| Small Backpack | 30 |
| Large Backpack | 45 |
| Tactical Backpack | 60 |

Owning any backpack of that tier sets your cap. You cannot drop a backpack if the remaining cap would be smaller than what you are carrying.

### Inventory window

- Search box filters item names
- Click an item to see quantity, durability, nutrition, hydration, damage, and its description
- **Select** equips a pickaxe, axe, sword, container, or rest item
- **Consume** / **Use** eats, drinks, or applies a typed amount (food, drink, medicine, bandages)
- **Drop** removes a typed amount forever

If inventory is full you cannot scavenge or pick up more loot. Crafting that produces more items than it consumes also needs free space.

---

## Selecting Tools

Five slots matter. The game auto-equips the best owned item in each slot at the start of a day if the slot is empty.

| Slot | Items (best first) | Why it matters |
| --- | --- | --- |
| Pickaxe | Galaxium → Ruby → Diamond → Iron → Stone → Wooden | Better ore while scavenging; required for the rare galaxium cave |
| Axe | Galaxium → Ruby → Diamond → Iron → Stone → Wooden | Better wood, plants, and fruit while scavenging |
| Sword | Galaxium → Ruby → Diamond → Iron → Stone → Wooden | Used as your “decent weapon” check when raiding a village |
| Container | Bucket → Bowl → Coconut Shell | Lets scavenging find salt water in that container |
| Rest | Advanced Camp → Fortified Camp → Improved Shelter → Shelter → Bedroll | Morning stamina bonus and storm protection |

Tools and weapons have **durability**. Scavenging can wear the selected pickaxe or axe. Combat wears the weapon you attack with. When durability hits 0, that copy breaks and is removed.

You can carry several copies of the same tool. The game uses the first durability value in the list.

---

## Scavenging

Requirements:

- Health above 0
- At least **5** stamina
- At least 1 free inventory space

Each scavenge rolls **10** times against your current chance table:

- Start from the **base** table (rocks, sticks, vines, fruit, flint, leaves, feathers, a little raw meat, rare wooden/stone tools)
- Merge in bonuses from your **selected pickaxe**
- Merge in bonuses from your **selected axe**
- Merge in water fills from your **selected container**

Higher-tier tools do not just find more of the same thing. They unlock new materials:

| Pickaxe | New finds |
| --- | --- |
| Wooden | More rock and flint |
| Stone | Iron ore |
| Iron | Copper ore, occasional diamond |
| Diamond | Diamond ore, ruby ore |
| Ruby | Much more ore |
| Galaxium | Almost guaranteed high-tier ore rolls |

| Axe | New finds |
| --- | --- |
| Wooden | Wooden logs, large leaves, a little fibre |
| Stone | Rubber |
| Iron and above | Steadily more wood, fruit, fibre, rubber, coconuts |

If a container is selected you can also roll salt water, which **uses up** one empty container of that type.

Scavenging always costs 5 stamina (scaled by difficulty), even if you find nothing.

---

## Crafting

Open **Crafting**, search a recipe, and read the right-hand panel:

- What it produces
- Ingredients you own vs ingredients you need
- Station requirement
- Whether you have space

Press **Craft** only when the status line is green.

### Stations

Some recipes need an item in your inventory, not just ingredients:

| Requirement | Used for |
| --- | --- |
| None | Basic woodwork, rope, campfire, shelters, some containers |
| Crafting Bench | Most tools, weapons, electronics, backpacks, medicine |
| Furnace | Smelting ores and gems, firing a clay bowl |
| Campfire | Cooked meat, boiling salt water into fresh water |

The station is **not** consumed. Keep one bench, one furnace, and one campfire.

### Important craft chains

**Wood**

`Stick ×4 → Wooden Log`  
`Wooden Log → Stick ×4` or `Wooden Log → Wooden Plank ×4`  
`Wooden Plank ×4 → Crafting Bench`

**Stone / metal**

`Rock ×8 + Crafting Bench → Furnace`  
`Iron Ore ×2 + Wooden Log + Furnace → Iron Ingot ×2`  
Same pattern for copper, diamond, ruby, and galaxium.

**Electronics**

`Copper Ingot + Rubber → Wire ×5`  
`Wire + Copper + Iron → Circuit`  
`Iron + Copper + Lemon → Battery`  
`Iron + Wire + Rubber → Antenna`  
Then Receiver, Transmitter, Radio, Signal Booster, Emergency Beacon.  
Add Galaxium to upgrade each of those into the advanced versions.

**Water**

`Coconut → Coconut Shell ×2`  
`Clay ×3 + Furnace → Bowl`  
`Iron Ingot ×3 → Bucket`  
Fill by scavenging with that container selected, then boil:

`Salt-water container + Wooden Log + Campfire → Fresh-water container`

---

## Food, Water, and Medicine

### Eating and drinking

In Inventory, pick the item, type how many, press **Consume**.

| Item | Hunger | Hydration | Notes |
| --- | --- | --- | --- |
| Apple | +5 | +5 | Also a drink |
| Orange | +5 | +5 | Also a drink |
| Lemon | +5 | +5 | Also used to craft batteries |
| Coconut | +10 | +5 | Can be split into shells |
| Raw Meat | +15 | — | 30% chance to cause sickness |
| Cooked Meat | +25 | — | Needs campfire |
| Herbal Medicine | 0 | — | +15 Health, −4 sickness per serving |
| Bandage | — | — | Use from Inventory: +5 Health per bandage |
| Shell / Bowl / Bucket of fresh water | 0 | +10 / +25 / +50 | Boiled |
| Shell / Bowl / Bucket of salt water | 0 | −5 / −10 / −20 | Makes you thirstier |
| Fruit juices | 0 | +5 / +10 / +20 | Shell / bowl / bucket |

Cook meat. Boil water. Do not drink seawater.

### Medicine

- **Bandage** — fibre + vine at a crafting bench. Use it from Inventory to heal 5 Health.
- **Herbal Medicine** — leaf + coconut at a crafting bench. This is your sickness cure and a stronger heal.

---

## Shelters and Rest

Craft in this order when you can:

1. **Bedroll** — fibre, vine, large leaf
2. **Shelter** — logs, large leaves, vines, bedroll
3. **Improved Shelter** — shelter + planks + leaves
4. **Fortified Camp** — improved shelter + iron + planks
5. **Advanced Camp** — fortified camp + galaxium + ruby + diamond

Select the camp in Inventory so it is your rest item.

**Storms** (a common daily event):

- Advanced Camp, or Fortified Camp half the time: you stay safe
- Any other selected shelter: you lose 5 Health and **that shelter is destroyed**
- No shelter: you lose 10 Health

Storm damage is scaled by difficulty. A destroyed shelter is removed from inventory. Rebuild before the next storm.

---

## Combat

Animals and later alien troops can appear as events. You choose **Fight** or **Ignore**.

If you fight, a battle window opens:

1. Click **Melee Weapons** or **Ranged Weapons**
2. Pick a weapon
3. Click **ATTACK!**
4. Click **Next Turn**
5. When the enemy attacks, a yellow **CLICK!** button appears. Press it in time to block. Miss it and you take the attack’s damage

Enemy health, how often they dodge, and how short the block window is all rise with difficulty.

### Rules of thumb

- You can always punch (5 damage). It never breaks.
- Swords are melee only.
- Axes can be used as melee weapons.
- Spears work as melee **and** thrown ranged weapons (no ammo).
- Bows need **Arrows**.
- Blaster and Omega Blaster are strong ranged weapons with no ammo.
- Weapons lose 1 durability per attack and can break mid-fight.
- Enemies can dodge. Higher “reaction” enemies dodge less; faster enemies give you a shorter block window.
- About 12% of your hits are critical (1.6× damage).

### Animals

| Animal | Rough threat | Typical drops |
| --- | --- | --- |
| Island Snake | Fast, low health | None |
| Island Wolf | Fast | Raw meat, fur |
| Wild Boar | Medium | Raw meat, hide, tusk |
| Giant Crab | Slow, tanky | Raw meat, shell |
| Komodo Dragon | High | None |

### Aliens

These only start appearing after the UFO climax is in motion (`mission8`, and you did not hide from the UFO).

| Enemy | Notes | Rare drop |
| --- | --- | --- |
| Alien Troop | Tough soldier | Blaster |
| Alien Goliath | Final fight at the UFO | Omega Blaster |

Win loot is rolled several times against that enemy’s drop table. If you lose the fight you are left wounded (you do not automatically die unless Health hit 0).

Village raids also check whether your **selected sword** is iron or better. A weak weapon means a much worse beating if you are caught.

---

## Random Events

Each morning after needs are applied, the game rolls **1 to 101**.

| Roll | Event |
| --- | --- |
| 1–10 | Storm |
| 11–20 | Hidden food stash (+20 Hunger) |
| 21–30 | Village — raid or walk away |
| 31–40 | Mission signal / ship / UFO scene (depends on your gear) |
| 41–50 | Animal encounter |
| 51–60 | Alien encounter (only after the UFO arrival scene, if you did not abandon it) |
| 61–100 | Quiet day |
| 101 | Mysterious cave — only if your selected pickaxe is Ruby or Galaxium |

The cave can dump a large amount of **Galaxium Ore** into your pack, wearing the pickaxe once per ore you actually pick up. Make space first.

### Village raid outcomes

- Clean getaway and loot
- Spotted: fight them off (5 Health if you have an iron-or-better selected sword, otherwise 20 Health and no loot)
- Spotted early and you flee with nothing

Walking away is always safe.

---

## Rescue Missions

The story does not use a quest log. Progress is inferred from what you are carrying.

### Ship route

1. Craft a **Receiver** or **Radio**.
2. On a mission event, listen, then respond when you also have a way to transmit (radio, or transmitter + receiver).
3. Craft a **Signal Booster** so they can keep talking.
4. Craft an **Emergency Beacon**. When the captain asks for your location, activate it. The beacon is consumed.
5. Next mission event: the ship is at the shore.
   - **Board** — you escape, unless you are carrying galaxium or any “advanced” item. Then you are rejected.
   - **Abandon** — the ship leaves for good.

If you are rejected or you abandon the ship, the UFO route is the way out.

### UFO route

1. Craft an **Advanced Receiver** or **Advanced Radio** (base device + galaxium).
2. Respond to the pilot.
3. Add an **Advanced Signal Booster**.
4. Activate an **Advanced Emergency Beacon** when asked for a location.
5. The UFO lands.
   - **Board** — an Alien Goliath climbs out. Defeat it to steal the craft and escape.
   - **Abandon** — it leaves. Alien patrols no longer spawn from that story beat.

You can keep playing after abandoning both rescues, but there is no third ending.

---

## Saving and Loading

**File → Save** writes to the current file if you already have one, otherwise asks where to put it.

**File → Save As** always asks for a new path.

Each save writes:

- a `.json` file of stats, inventory, missions, selected tools, difficulty, and the event log
- a matching `.md` copy of the text log

**File → Load Save** reads a `.json` and updates the live bars.

**Quit** asks if you are sure. If a save file is already linked to this run it is written automatically. Otherwise you are asked whether to save first.

Saves do not pause the current event window. Save between days when the main screen is idle.

Default folder: `Documents/IslandSurvivalSaves`.

---

## Item Catalog

Descriptions match the in-game inventory text.

### Raw materials

| Item | Description |
| --- | --- |
| Rock | It's a rock |
| Stick | It's a stick |
| Vine | Good for binding things together |
| Wooden Log | It's wood |
| Wooden Plank | It's wood but processed |
| Leaf | It's a leaf |
| Large Leaf | It's a bigger leaf |
| Fibre | It's fibre (this means something apparently) |
| Flint | No steel |
| Feather | It's a feather |
| Rubber | Good for insulation |
| Clay | Malleable |
| Cloth | It's cloth |
| Hide | Skin |
| Fur | Hair |
| Leather | Tanned animal hide. Reliable material |
| Tusk | When you neglect denistry |
| Shell | Someone's home |
| Iron Ore | Reliable metal. Kinda useless as an ore |
| Copper Ore | Good for electronics. Kinda useless as an ore |
| Diamond Ore | Blue gem. Kinda useless as an ore |
| Ruby Ore | Red gem. Kinda useless as an ore |
| Galaxium Ore | Metal from the cosmos. Kinda useless as an ore |
| Iron Ingot | Reliable metal |
| Copper Ingot | Good for electronics |
| Diamond | Blue gem |
| Ruby | Red gem |
| Galaxium | Metal from the cosmos |
| Wire | Good for electronics |
| Circuit | Good for electronics |

### Food

| Item | Description |
| --- | --- |
| Apple | Keeps the doctor away |
| Orange | It's an orange |
| Lemon | It's a lemon |
| Coconut | It's a coconut |
| Raw Meat | I wouldn't risk eating that |
| Cooked Meat | Medium rare |
| Herbal Medicine | Treat illnesses |

### Containers and drinks

| Item | Description |
| --- | --- |
| Coconut Shell | Half a coconut |
| Bowl | It's a bowl |
| Bucket | It's a bucket |
| Any salt-water fill | Salt water in that container — drinking it makes you thirstier |
| Any fresh-water fill | Boiled water in that container |
| Any fruit juice | Juice in that container |

### Tools

Pickaxes: *Minecraft YouTubers love people who use this*  
Axes: *Chop chop chop* (Galaxium Axe: *Chop Away At My Heart*)

Durability: Wooden 20, Stone 50, Iron 75, Diamond 150, Ruby 250, Galaxium 500.

### Weapons

| Type | Description | Wooden | Stone | Iron | Diamond | Ruby | Galaxium |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sword (melee) | It's a sword | 2 | 5 | 15 | 25 | 50 | 200 |
| Axe (melee) | Chop chop chop | 5 | 10 | 20 | 30 | 65 | 250 |
| Spear (melee or ranged) | Thrust and throw | 5 | 10 | 18 | 30 | 75 | 300 |
| Bow (needs arrows) | Arrows not included | 5 | 10 | 18 | 30 | 75 | 300 |

| Item | Description | Damage |
| --- | --- | --- |
| Arrow | Bullseye | — |
| Blaster | Pew pew | 350 |
| Omega Blaster | PEW PEW | 500 |

Punch is not an item. It always deals 5. Blaster and Omega Blaster have 500 durability.

### Stations and shelters

| Item | Description |
| --- | --- |
| Crafting Bench | The heart of crafting |
| Furnace | Melting |
| Campfire | Stove |
| Bedroll | Bad night's rest |
| Shelter | Good night's rest |
| Improved Shelter | Safety first |
| Fortified Camp | Fortress |
| Advanced Camp | Superstructure |

### Utility

| Item | Description |
| --- | --- |
| Bandage | Patch that up |
| Rope | Thick string |
| Small Backpack | More storage |
| Large Backpack | MORE storage |
| Tactical Backpack | MORE STORAGE |

### Comms

| Item | Description |
| --- | --- |
| Antenna | Receive signals |
| Battery | Power source |
| Receiver | Listen for messages |
| Transmitter | Send messages |
| Radio | Communicate over distances |
| Signal Booster | Enhance signal strength |
| Emergency Beacon | Call for help |
| Advanced Receiver | Listen for advanced signals |
| Advanced Transmitter | Send advanced messages |
| Advanced Radio | Communicate with advanced technology |
| Advanced Signal Booster | Enhance advanced signal strength |
| Advanced Emergency Beacon | Call for advanced help |

---

## Tips

1. **Water first.** A dry morning can deal 40 damage (more on hard). Craft a container early, scavenge with it selected, and boil what you find.
2. **Do not Advance hungry and thirsty.** Eat and drink on the same day you gather.
3. **Build a campfire and cook meat.** Raw meat is a sickness lottery.
4. **Make a crafting bench, then stone tools.** Stone is the first real upgrade over punching the ground with wood.
5. **Keep inventory space.** A full pack wastes scavenge rolls and cave ore. Base cap is 15 — craft a backpack before you stockpile ore.
6. **Select your best tools.** Auto-equip helps, but after a break or a craft, open Inventory and Select.
7. **Fortify before you get greedy.** Storms delete weak shelters.
8. **Iron sword before raiding.** Village loot is nice. A 20 Health beating is not.
9. **Carry bandages.** They are cheap and heal 5 on use.
10. **Ship ending is the simple ending.** If you want it, do not smelt galaxium until after you board — galaxium and advanced gear make the captain turn you away.
11. **Galaxium is the UFO ending.** Save a ruby or galaxium pickaxe for roll 101, empty some pack space, and enter the cave.
12. **Difficulty is permanent for that save.** If Very Hard is chewing through your water, that is working as designed.
