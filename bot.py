import argparse
import json
import os
from random import choice
from pprint import pprint
import json

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0
count = 0


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships(map_size)
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    if (map_size == 7)

    else if (map_size == 10)

    else
        shots = [(4,5),(10,9),(3,12),(8,3),(1,2),(8,9),(5,8),(7,6),(7,12),(5,4),
                 (10,7),(2,9),(6,1),(5,6),(10,11),(2,5),(13,0),(0,13),(13,2),(1,0),
                 (6,11),(1,6),(10,5),(12,9),(2,11),(11,2),(0,9),(3,6),(13,12),(5,0),
                 (6,13,(11,0),(0,3),(11,6),(4,11),(4,1),(12,11),(9,2),(6,7),(0,5),
                 (13,4),(5,10),(4,13),(3,2),(7,4),(9,12),(2,7),(8,1),(0,1),(13,8),
                 (3,0),(11,12),(12,7),(4,7),(3,10),(10,1),(10,3),(9,4),(3,4),(2,1),
                 (11,10),(8,13),(1,12),(6,5),(7,8),(10,13),(13,6),(12,13),(1,10),(7,2),
                 (5,2),(7,10),(0,7),(0,11),(11,4),(8,7),(8,11),(13,10),(2,13),(2,3),
                 (9,0),(8,5),(4,3),(1,4),(3,8),(5,12),(6,9),(11,8),(7,0),(6,3),
                 (12,1),(12,3),(1,8),(12,5),(9,6),(4,9),(9,8),(9,10)]

    targets = []
    for cell in opponent_map:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)
    output_shot(*target)
    return


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    if (map_size == 7)
        ships = ['Battleship 0 4 East',
                 'Carrier 6 2 north',
                 'Cruiser 1 0 north',
                 'Destroyer 1 6 East',
                 'Submarine 3 1 East'
                 ]
    else if (map_size == 10)
        ships = ['Battleship 2 6 East',
                 'Carrier 8 4 north',
                 'Cruiser 1 2 north',
                 'Destroyer 1 8 East',
                 'Submarine 6 1 East'
                 ]
    else
        ships = ['Battleship 5 7 East',
                 'Carrier 11 12 south',
                 'Cruiser 2 3 north',
                 'Destroyer 3 10 East',
                 'Submarine 9 2 East'
                 ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
