#Planet Hopper

This challenge focuses on implementing an AI captain for a spaceship that transports goods between planets. You will need to download
 the github repo to test your AI code, but only the Captain class (components\captain.py) should be modified. 

Github repo: https://github.com/reddit-pygame/planet-hopper



#How it Works

###Goal

Accumulate 100,000 units of each resource (other than food). Resources onboard the ship don't count towards these totals.


###Planets

Each planet is capable of producing a particular resource. Each colonist on the planet will produce 1 unit of the planet's resource per day. Each planet
 starts with 10 colonists and 1000 units of food.

###Resources

Each colonist needs .15 units of food each day to survive. Insufficient food will result in starvation of some or all of the colonists on the planet.


###Ship

The colonists have a single transport ship capable of interplanetary travel. The ship is responsible for distributing resources amongst the planets. Each time the
 ship docks on a planet all cargo and passengers are automatically offloaded.

###Captain

An instance of the Captain class is responsible for determining the destination and payload of the transport ship. Each day the ship is docked on a planet
 the Captain class's get_orders method will be called. Three dicts will be passed as arguments to Captain.get_orders: `world_info`, `ship_info` and `distances`. 
 
`world_info` contains a dict for each planet (keyed by planet name) with the following structure

    {"Planet name":
            {"pos": screen position of the planet,
            "inventory": {resource: amount of resource currently on the planet},
            "resource": name of the resource the planet produces,
            "consumption": {resource: planet's daily consumtion of resource},
            "num_colonists": number of colonists living on the planet}}            
    
`ship_info` a dict containg information about the transport ship

    {"speed": the distance (in pixels) that the ship can travel in a day    
      "destination": the planet name of the ship's destination (this will be None when Captain.update is called)
      "pos": the current screen position of the ship (this will be equal to the position of the planet the ship is docked at)
      "cargo": {resource: number of units of resource currently onboard}
      "colonists": number of colonists onboard}
    
`distances` a dict of dicts containing the distance between each planet

    {"planet name": {other_planet1: distance from planet to other_planet1,    
                             other_planet2: distance from planet to other_planet2,
                             ...}}
                             
These dicts are also passed to Captain.\_\_init\_\_.
                             
The Captain.get_orders method should return a dict representing the captain's orders

    {"destination": planet name,
     "cargo": {resource: num units of resource to carry to destination planet},
     "colonists": num colonists to bring to destination planet}

     
###Controls

**UP** Increase simulation speed
**DOWN** Decrease simulation speed
**SPACE** Pause simulation
**ESC** Exit

Hover mouse over ship or planet to display info window


#####Previous Challenges


[Draw Order Challenge](https://www.reddit.com/r/pygame/comments/3de4ng/challenge_drawing_in_the_right_order/) | 
[Spawn, Collide, Wrap](https://www.reddit.com/r/pygame/comments/3eddbp/challenge_spawn_collide_wrap/) | 
[Thruster Style Movement](https://www.reddit.com/r/pygame/comments/3fe60j/challenge_thruster_style_movement/) | 
[Conway User Interaction](https://www.reddit.com/r/pygame/comments/3iwdqq/challenge_conway_user_interaction/) |
[JSON Loading Challenge](https://www.reddit.com/r/pygame/comments/3lafr3/json_loading_challenge/) | 
[Map Distance Challenge](https://www.reddit.com/r/pygame/comments/3oc19d/map_distance_challenge/) | 
[Caching Pumpkins](https://www.reddit.com/r/pygame/comments/3qc9wm/challenge_caching_pumpkins/) | 
[A Puzzling World](https://www.reddit.com/r/pygame/comments/3s9m2j/challenge_a_puzzling_world/) | 
[Turkey Shoot](https://www.reddit.com/r/pygame/comments/3tvc5h/challenge_turkey_shoot/) | 
[All Downhill From Here](https://www.reddit.com/r/pygame/comments/3vsc5x/challenge_all_downhill_from_here/) | 
[Christmas Cannon](https://www.reddit.com/r/pygame/comments/3xpi6t/challenge_christmas_cannon/) | 
[Color Picker](https://www.reddit.com/r/pygame/comments/40mdi8/challenge_color_picker/) | 
[Minigolf Part I: Prototype](https://www.reddit.com/r/pygame/comments/4335cs/challenge_minigolf_part_1_prototype/) | 
[Skeet Shoot](https://www.reddit.com/r/pygame/comments/46xbxo/challenge_skeet_shoot/) | 
[Spin Class](https://www.reddit.com/r/pygame/comments/4aq3or/challenge_spin_class/) | 
[Egg Lob](https://www.reddit.com/r/pygame/comments/4dcvq4/challenge_egg_lob/) | 
[Build-A-Sprite](https://www.reddit.com/r/pygame/comments/4g3m7n/challenge_buildasprite/) | 
[Matrix Digital Rain](https://www.reddit.com/r/pygame/comments/4jg5cf/challenge_matrix_digital_rain/)


*Good luck, have fun and feel free to ask for help if you need it*