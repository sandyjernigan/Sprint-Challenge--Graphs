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
rooms_to_visit = []
rooms_to_visit.append(player.current_room.id)

# Rooms Completed
rooms_completed = []

# Create traversal graph
traversal_graph = {}
room_connections = {}

i = 1

# while the plan_to_visit queue is not Empty:
#while len(rooms_to_visit) > 0:
while i < 5:
    i += 1
    print (f" Current Room: {player.current_room.id}")

    # Check if in completed list
    if player.current_room.id not in rooms_completed:

        # Check if room is in the Traversal Graph
        if not player.current_room.id in traversal_graph.keys():
            # If not in graph, then check room and add to graph
            room_connections = {}
            # Add each connection as unknown
            for each in player.current_room.get_exits():
                room_connections.update({each: "?"})
            # Add connections to graph
            traversal_graph.update({player.current_room.id: room_connections})
        
        # Check Connected Rooms in Graph
        room_connections = traversal_graph.get(player.current_room.id)
        print(traversal_graph)

        # Count how many ?
        # More than 1 means we need to come back
        if list(room_connections.values()).count("?") > 1:
            # Add to list to visit
            if player.current_room.id not in rooms_to_visit:
                rooms_to_visit.append(player.current_room.id)
        # More Than 0, we need to check room
        if list(room_connections.values()).count("?") > 0:
            # Go to next Room
            direction = next(key for key, value in room_connections.items() if value == "?")
            print (direction)
            # Set Last Room, before moving
            last_room = player.current_room.id
            # Move to new Room
            traversal_path.append(direction)
            player.travel(direction)
            # Update Connection
            room_connections[direction] = player.current_room.id
            # Find room
            # for direction in room_connections:
            #     if room_connections.get(direction) == "?":
            #         # Set Last Room, before moving
            #         last_room = player.current_room.id
            #         # Move to new Room
            #         traversal_path.append(direction)
            #         player.travel(direction)
            #         # Update Connection
            #         room_connections[direction] = player.current_room.id
            #         # Leave For Loop
            #         break
        
            #     else:
            #         print (f"No New Connections: {rooms_to_visit}")
            #         rooms_completed.append(player.current_room.id)
    else:
        # If Room listed as completed, go back
        if player.current_room.id in rooms_to_visit:
            rooms_to_visit.remove(player.current_room.id)
        print (f"Completed: {player.current_room.id}")
        for direction, room in traversal_graph.get(player.current_room.id).items():
            print(f"Last Room: {room} {direction}")
            if room == last_room:
                traversal_path.append(direction)
                player.travel(direction)
                break

print (f"Path: {traversal_path}")
print (traversal_graph)
print (f"Rooms to Visit: {rooms_to_visit}")
print (f"Rooms Completed: {rooms_completed}")


# # TRAVERSAL TEST - DO NOT MODIFY
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
