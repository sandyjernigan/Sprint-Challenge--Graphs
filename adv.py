from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# Create traversal graph
traversal_graph = {}
# Dict for Connections
room_connections = {}

# Setup Visited List
rooms_to_visit = []
rooms_visited = []
paths_taken = []

# Get first room
current_room = player.current_room.id
# Room Connections
for each in player.current_room.get_exits():
    room_connections.update({each: "?"})
# Loop Thru Connections - returns 1 -> direction = next(key for key, value in room_connections.items() if value == "?")
for direction, room in room_connections.items():
    if room == "?":
        rooms_to_visit.append([player.current_room.id, direction])
# Add first connection to graph
traversal_graph.update({player.current_room.id: room_connections})

# List for Rooms Completed
# rooms_completed = []
# full_path = []
path_taken = []
last_room_direction = None
comment = ""

def reverseDirection(direction):
    if direction == "n": return "s"
    if direction == "s": return "n"
    if direction == "w": return "e"
    if direction == "e": return "w"

# while the rooms_to_visit list is not Empty:
while len(rooms_to_visit) > 0:
    current_room = player.current_room.id
    
    print (f"Current Room: {current_room} ")
    comment = f"Comment - Current Room: {current_room} "

    # Check Connected Rooms in Graph
    room_connections = traversal_graph.get(current_room)

    # Update were came from
    if last_room_direction is not None and last_room is not None:
        new_direction = reverseDirection(last_room_direction)
        room_connections[new_direction] = last_room
        print(f"Add Last Room {last_room}: {room_connections}")

    # Count how many ?
    unknown_connections = list(room_connections.values()).count("?")
    comment += f"- Connections: {room_connections} - Unknown Connections: {unknown_connections}"
    
    if unknown_connections > 0:
        # Get direction
        direction = next(key for key, value in room_connections.items() if value == "?")
        
        # Remove Current Room and direction from que
        if [current_room, direction] in rooms_to_visit:
            rooms_to_visit.remove([current_room, direction])
        comment += f"- Remove Path: {[current_room, direction]} "
        comment += f"- Rooms to Visit: {rooms_to_visit} "

        # Move Player new direction
        player.travel(direction)
        # Add Path to Traversal Path
        traversal_path.append(direction)
        # Set last room direction
        last_room_direction = direction
        # Append to current path reference
        path_taken.append([current_room, direction])
        # Set Last Room, to previous current room
        last_room = current_room
        # Update Connection
        current_room = player.current_room.id
        room_connections[direction] = current_room
                
        # Check if room is in the Traversal Graph
        if not current_room in traversal_graph.keys():
            # If not in graph, then check room and add to graph
            room_connections = {}
            # Add each connection as unknown
            for direction in player.current_room.get_exits():
                room_connections.update({direction: "?"})
                if [current_room, direction] not in rooms_to_visit:
                    rooms_to_visit.append([current_room, direction])
            # Add connections to graph
            traversal_graph.update({player.current_room.id: room_connections})

        # TODO: remove print
        print (f"Graph: {traversal_graph}")


    # If 0 connections, then room completed. Check path for incomplete
    else:
        comment += f"- Room Complete: {last_room}"
        # Go to last room
        last_path = path_taken.pop(-1)
        print (f"Last Path {last_path}")
        direction = last_path[1]
        # Move Player new direction
        player.travel(direction)
        # Add Path to Traversal Path
        traversal_path.append(direction)
        # Set last room direction
        last_room_direction = direction
        # Set Last Room, to previous current room
        last_room = current_room
        # Update Connection
        current_room = player.current_room.id
        # room_connections[direction] = current_room

    # else:
    #     # If Room listed as completed, go back
    #     # if last_room in rooms_to_visit:
    #     #     rooms_to_visit.remove(last_room)
    #     #     comment += f"- Remove: {last_room}"
        
    #     # If room complete remove from need to visit
    #     # for room in rooms_completed:
    #     #     if room in rooms_to_visit:
    #     #         rooms_to_visit.remove(room)

    #     # Go to last room
    #     # comment += f"- Last Room {last_room}"
    #     print(f"Last Room {last_room}")
    #     print (traversal_graph)
    #     print (f"Rooms to Visit: {rooms_to_visit}")
        
    #     # last_room_direction = next(key for key, value in room_connections.items() if value == last_room)
    #     # comment += f"- Goto Last Room: {last_room_direction}"
    #     # # update last room
    #     # last_room = player.current_room.id
    #     # # move to last room
    #     # traversal_path.append(last_room_direction)
    #     # player.travel(last_room_direction)
    #     # lr = path_taken.pop(-1)
    
    print (f"Graph: {traversal_graph}")
    comment += f"- Last Move: {last_room_direction} "
    print(comment)

# print (f"Path: {traversal_path}")
# print (traversal_graph)
# print (f"Path Taken: {path_taken}")
# print (f"Rooms to Visit: {rooms_to_visit}")
# print (f"Rooms Completed: {rooms_completed}")


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
