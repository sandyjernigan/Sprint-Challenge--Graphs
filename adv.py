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
current_path = []

# Rooms to visit
rooms_to_visit = Queue()
rooms_to_visit.enqueue(player.current_room.id)

# Rooms Completed
rooms_completed = []

# Create traversal graph
traversal_graph = {}
room_connections = {}

# while the plan_to_visit queue is not Empty:
while rooms_to_visit.size() > 0:
    current_path.append(player.current_room.id)
    # Check if room is in the Traversal Graph
    if not player.current_room.id in traversal_graph.keys():
        # If not in graph, then check room and add to graph
        room_connections = {}
        # Add each connection as unknown
        for room in player.current_room.get_exits():
            room_connections.update({room: "?"})
        # Add connections to graph
        traversal_graph.update({player.current_room.id: room_connections})
    else:
        # If in graph, need to check if any connections are ?
        print ("In graph")
        # Remove room if all paths are checked        
        player.current_room.id = rooms_to_visit.dequeue()
    
    room_connections = traversal_graph.get(player.current_room.id)
    print (f"Room: {room_connections}")

print (traversal_graph)
print (current_path)

            # # Add to Rooms to Visit
            # if room not in rooms_completed:
            #     rooms_to_visit.enqueue(room)


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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
