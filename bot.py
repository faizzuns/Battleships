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
        shots = [(3,3), (1,5), (5,5), (5,1), (1,1), (4,4), (2,2), (4,2), (2,4),
                 (0,4), (3,1), (6,2), (3,5), (0,6), (6,6), (5,3), (1,3), (2,0),
                 (4,0), (2,6), (6,4), (0,0), (4,6), (6,0), (0,2)]
    else if (map_size == 10)
        shots = [(4,5), (6,7), (5,2), (1,6), (6,9), (9,2), (2,1), (7,6), (5,4),
                 (9,0), (3,8), (1,2), (8,3), (7,8), (1,8), (6,1), (0,9), (9,6),
                 (6,5), (3,2), (1,4), (8,1), (4,9), (9,4), (3,6), (9,8), (0,3),
                 (7,4), (1,0), (5,6), (0,5), (4,7), (7,0), (8,9), (5,8), (6,3),
                 (2,3), (8,7), (0,1), (3,0), (0,7), (7,2), (4,1), (2,9), (2,7),
                 (4,3), (8,5), (2,5), (5,0), (3,4)]
    else


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
