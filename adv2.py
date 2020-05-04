from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
rooms_to_visit = []
rooms_to_visit.append(player.current_room.id)

# Rooms Completed
rooms_completed = []

# Create traversal graph
traversal_graph = {}
room_connections = {}

full_path = []
path_taken = []
last_room = None
last_room_direction = None
comment = ""

i = 1

# while the plan_to_visit queue is not Empty:
# while len(rooms_to_visit) > 0:
while len(rooms_to_visit) > 0:
    i += 1

    # Set Current Room, before moving
    current_room = player.current_room.id
    full_path.append(current_room)
    path_taken.append(current_room)

    comment = f"Current Room: {current_room} "

    # Check if in completed list
    if current_room not in rooms_completed:

        # Check if room is in the Traversal Graph
        if not current_room in traversal_graph.keys():
            # If not in graph, then check room and add to graph
            room_connections = {}
            # Add each connection as unknown
            for each in player.current_room.get_exits():
                room_connections.update({each: "?"})
            # Add connections to graph
            traversal_graph.update({current_room: room_connections})
        
        # Check Connected Rooms in Graph
        room_connections = traversal_graph.get(current_room)

        # Update were came from
        if last_room_direction is not None and last_room is not None:
            if last_room_direction == "n": new_direction = "s"
            if last_room_direction == "e": new_direction = "w"
            if last_room_direction == "s": new_direction = "n"
            if last_room_direction == "w": new_direction = "e"

            room_connections[new_direction] = last_room

        # Count how many ?
        unknown_connections = list(room_connections.values()).count("?")
        # More than 1 means we need to come back
        comment += f"- Connections: {room_connections} - Unknown Connections: {unknown_connections}"
        
        if unknown_connections > 0:
            # Add to list to visit
            if current_room not in rooms_to_visit:
                rooms_to_visit.append(current_room)
                
            direction = next(key for key, value in room_connections.items() if value =="?")

            # Go to new direction if it is not from the old direction
            traversal_path.append(direction)
            player.travel(direction)
            last_room_direction = direction
            
            # Update Connection
            room_connections[direction] = player.current_room.id
            
            # Update Last Room
            last_room = current_room

        # If 0 connections, then room completed
        if unknown_connections == 0:
            comment += f"- Room Complete: {current_room}"
            rooms_completed.append(current_room)

    else:
        
        # If Room listed as completed, go back
        if current_room in rooms_to_visit:
            rooms_to_visit.remove(current_room)
            comment += f"- Remove: {current_room}"
        
        # If room complete remove from need to visit
        for room in rooms_completed:
            if room in rooms_to_visit:
                rooms_to_visit.remove(room)

        if len(path_taken) > 0: 
            last_path = path_taken.pop(-1)

            if current_room == last_path:
                if len(path_taken) > 0: 
                    last_path = path_taken.pop(-1)
                else: 
                    last_path = None
        else:
            last_path = None

        if last_path is not None:
            if last_path in room_connections.values(): 
                direction = next(key for key, value in room_connections.items() if value == last_path)
            elif current_room in room_connections.values():
                direction = next(key for key, value in room_connections.items() if value == current_room)
            else:
                print(last_path)
                print(path_taken)
                print("break")
                direction = None
                # break

        else: 
            # Check rooms to visit
            last_path = rooms_to_visit.pop(-1)

            if last_path in room_connections.values(): 
                direction = next(key for key, value in room_connections.items() if value == last_path)
            elif current_room in room_connections.values():
                direction = next(key for key, value in room_connections.items() if value == current_room)
            else:
                print(room_connections)

        # Travel Back to last path
        if direction is not None:         
            traversal_path.append(direction)
            player.travel(direction)
            last_room_direction = direction

        print (f"Current: {current_room}, Last: {last_path}, Connections: {room_connections}, Direction: {direction}")

    comment += f"- Last Move: {last_room_direction} "
    print(comment)
    print (f"Rooms to Visit: {rooms_to_visit}")

# print (f"Path: {traversal_path}")
# print (traversal_graph)
# print (f"Path Taken: {path_taken}")
print (f"Rooms to Visit: {rooms_to_visit}")
# print (f"Rooms Completed: {rooms_completed}")


# TRAVERSAL TEST - DO NOT MODIFY
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
