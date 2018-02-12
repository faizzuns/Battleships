import argparse
import json
import os
from random import choice

commandFile = "command.txt" #command placement
shipFile = "place.txt" #ship placement location
stateFile = "state.json" #current game state
gameengine_path = '.' #Untuk directory game engine
mapsize = 0 #Ukuran Peta
epr = 3 #Energy Per Round

def main(player_key):
    #Fungsi utama dari bot
    global mapsize
    global epr
    # Membaca current state game
    with open(os.path.join(gameengine_path, stateFile), 'r') as f_in:
        state = json.load(f_in)

    #inisialisasi mapsize dan energy per round
    mapsize = state['MapDimension']
    if mapsize == 7:
        epr = 2
    elif mapsize == 10:
        epr = 3
    else:
        epr = 4

    #Melakukan aksi sesuai phase
    if state['Phase'] == 1:
        initShots()
        placeShips()
    else:
        if (state['PlayerMap']['Owner']['Shield']['CurrentCharges'] == 4 and not(state['PlayerMap']['Owner']['Shield']['Active'])):
            #jika energi cukup, menyalakan shield
            applyShield(state)
        else:
            shotCommand(state['OpponentMap']['Cells'], state['PlayerMap']['Owner'])

def applyShield(state):
    #Fungsi yang mengaktifkan shield sesuai kapal yang ingin dilindungi
    if not(state['PlayerMap']['Owner']['Ships'][1]['Destroyed']):
        x = state['PlayerMap']['Owner']['Ships'][1]['Cells'][1]['X']
        y = state['PlayerMap']['Owner']['Ships'][1]['Cells'][1]['Y']-1
    elif not(state['PlayerMap']['Owner']['Ships'][2]['Destroyed']):
        x = state['PlayerMap']['Owner']['Ships'][2]['Cells'][2]['X']
        y = state['PlayerMap']['Owner']['Ships'][2]['Cells'][2]['Y']
    elif not(state['PlayerMap']['Owner']['Ships'][3]['Destroyed']):
        x = state['PlayerMap']['Owner']['Ships'][3]['Cells'][3]['X']
        y = state['PlayerMap']['Owner']['Ships'][3]['Cells'][3]['Y']
    elif not(state['PlayerMap']['Owner']['Ships'][4]['Destroyed']):
        x = state['PlayerMap']['Owner']['Ships'][4]['Cells'][1]['X']
        y = state['PlayerMap']['Owner']['Ships'][4]['Cells'][1]['Y']
    elif not(state['PlayerMap']['Owner']['Ships'][0]['Destroyed']):
        x = state['PlayerMap']['Owner']['Ships'][0]['Cells'][1]['X']
        y = state['PlayerMap']['Owner']['Ships'][0]['Cells'][1]['Y']
    else:
        x=4
        y=6

    writeCommand(8,x,y)

def initShots():
    #Menginisialisasi target utama secara manual sesuai ukuran peta
    if (mapsize == 7):
        shots = [(3,3), (1,5), (5,5), (5,1), (1,1), (4,4), (2,2), (4,2), (2,4),
                 (0,4), (3,1), (6,2), (3,5), (0,6), (6,6), (5,3), (1,3), (2,0),
                 (4,0), (2,6), (6,4), (0,0), (4,6), (6,0), (0,2)]
    elif (mapsize == 10):
        shots = [(4,5), (6,7), (5,2), (1,6), (6,9), (9,2), (2,1), (7,6), (5,4),
                 (9,0), (3,8), (1,2), (8,3), (7,8), (1,8), (6,1), (0,9), (9,6),
                 (6,5), (3,2), (1,4), (8,1), (4,9), (9,4), (3,6), (9,8), (0,3),
                 (7,4), (1,0), (5,6), (0,5), (4,7), (7,0), (8,9), (5,8), (6,3),
                 (2,3), (8,7), (0,1), (3,0), (0,7), (7,2), (4,1), (2,9), (2,7),
                 (4,3), (8,5), (2,5), (5,0), (3,4)]
    else:
        shots = [(4,5),(10,9),(3,12),(8,3),(1,2),(8,9),(5,8),(7,6),(7,12),(5,4),
                 (10,7),(2,9),(6,1),(5,6),(10,11),(2,5),(13,0),(0,13),(13,2),(1,0),
                 (6,11),(1,6),(10,5),(12,9),(2,11),(11,2),(0,9),(3,6),(13,12),(5,0),
                 (6,13),(11,0),(0,3),(11,6),(4,11),(4,1),(12,11),(9,2),(6,7),(0,5),
                 (13,4),(5,10),(4,13),(3,2),(7,4),(9,12),(2,7),(8,1),(0,1),(13,8),
                 (3,0),(11,12),(12,7),(4,7),(3,10),(10,1),(10,3),(9,4),(3,4),(2,1),
                 (11,10),(8,13),(1,12),(6,5),(7,8),(10,13),(13,6),(12,13),(1,10),(7,2),
                 (5,2),(7,10),(0,7),(0,11),(11,4),(8,7),(8,11),(13,10),(2,13),(2,3),
                 (9,0),(8,5),(4,3),(1,4),(3,8),(5,12),(6,9),(11,8),(7,0),(6,3),
                 (12,1),(12,3),(1,8),(12,5),(9,6),(4,9),(9,8),(9,10)]
    #menaruh shots kedalam file shots.txt
    with open('shots.txt', 'w') as f:
        for shot in shots :
            f.write(str(shot[0]))
            f.write(",")
            f.write(str(shot[1]))
            f.write("\n")


def writeCommand(cmd, x, y):
    #menulis command untuk gameengine
    with open(os.path.join(gameengine_path, commandFile), 'w') as f_out:
        f_out.write('{},{},{}'.format(cmd, x, y))
        f_out.write('\n')
    pass

def checkSpecial(opponent_map, Owner, shots):
    #Mengecek dan mengembalikan command+kordinat tembakan jika bisa Melakukan
    #special shot
    if Owner['Energy']>=(8*epr) and not(Owner['Ships'][1]['Destroyed']) :
        if shots[0][0]==shots[1][0] and abs(shots[0][1]-shots[1][1])==2:
            x = shots[0][0]
            if shots[0][1]>shots[1][1]:
                y = shots[0][1]-1
            else:
                y = shots[0][1]+1
            return (2,x,y)
        elif shots[0][1]==shots[1][1] and abs(shots[0][0]-shots[1][0])==2:
            y = shots[0][1]
            if shots[0][0]>shots[1][0]:
                x = shots[0][0]-1
            else:
                x = shots[0][0]+1
            return (3,x,y)
    if Owner['Energy']>=(10*epr) and not(Owner['Ships'][3]['Destroyed']):
        if (mapsize==7):
            if (shots[0][0]+shots[0][1])%2==0 and CrossWorth(shots,shots[0][0],shots[0][1])>=3:
                return (4,shots[0][0],shots[0][1])
        else:
            if (shots[0][0]+shots[0][1])%2==1 and CrossWorth(shots,shots[0][0],shots[0][1])>=3:
                return (4,shots[0][0],shots[0][1])
    if Owner['Energy']>=(12*epr) and not(Owner['Ships'][2]['Destroyed']):
        if (mapsize==7):
            if (shots[0][0]+shots[0][1])%2==0 and CrossWorth(shots,shots[0][0],shots[0][1])>=2:
                return (5,shots[0][0],shots[0][1])
        else:
            if (shots[0][0]+shots[0][1])%2==1 and CrossWorth(shots,shots[0][0],shots[0][1])>=2:
                return (5,shots[0][0],shots[0][1])
    if Owner['Energy']>=(10*epr) and (Owner['Ships'][3]['Destroyed']) and (Owner['Ships'][2]['Destroyed']) and not(Owner['Ships'][0]['Destroyed']):
            if (mapsize==7):
                if (shots[0][0]+shots[0][1])%2==0:
                    return (7,shots[0][0],shots[0][1])
            else:
                if (shots[0][0]+shots[0][1])%2==1:
                    return (7,shots[0][0],shots[0][1])
    if Owner['Energy']>=(14*epr) and (Owner['Ships'][3]['Destroyed']) and (Owner['Ships'][2]['Destroyed']) and (Owner['Ships'][0]['Destroyed']) and (Owner['Ships'][1]['Destroyed']):
        if not(Owner['Ships'][4]['Destroyed']):
            return(6,shots[0][0],shots[0][1])
    return (0,0,0)

def CrossWorth(shots,x, y):
    #Mengembalikan jumlah petak silang dengan titik pusat(x,y) yang belum tertembak
    N = 0
    for cell in shots:
        if (cell[0]==x+1 and cell[1]==y+1):
            N += 1
        if (cell[0]==x-1 and cell[1]==y+1):
            N += 1
        if (cell[0]==x+1 and cell[1]==y-1):
            N += 1
        if (cell[0]==x-1 and cell[1]==y-1):
            N += 1
    return N


def shotCommand(opponent_map, Owner):
    #Melakukan command shot

    with open('shots.txt', 'r') as f:
        shots = [tuple(map(int, shot.split(','))) for shot in f]

    #Mengupdate list shots
    shotsDummy = list(shots)
    for shot in shotsDummy:
        cell = searchCell(opponent_map, shot[0], shot[1])
        if (cell['Missed']):
            shots.remove(shot)
        elif cell['Damaged']:
            if (shot[1]+1 != mapsize):
                myCell = searchCell(opponent_map, shot[0], shot[1]+1)
                if (not(myCell['Damaged']) and not(myCell['Missed'])):
                    myShot = shot[0],shot[1]+1
                    shots.insert(0,myShot)
            if (shot[1] != 0):
                myCell = searchCell(opponent_map, shot[0], shot[1]-1)
                if (not(myCell['Damaged']) and not(myCell['Missed'])):
                    myShot = shot[0],shot[1]-1
                    shots.insert(0,myShot)
            if (shot[0] != 0):
                myCell = searchCell(opponent_map, shot[0]-1, shot[1])
                if (not(myCell['Damaged']) and not(myCell['Missed'])):
                    myShot = shot[0]-1,shot[1]
                    shots.insert(0,myShot)
            if (shot[0]+1 != mapsize):
                myCell = searchCell(opponent_map, shot[0]+1, shot[1])
                if (not(myCell['Damaged']) and not(myCell['Missed'])):
                    myShot = shot[0]+1,shot[1]
                    shots.insert(0,myShot)
            shots.remove(shot)

    #Command utama (Menembak)
    tryspecial = checkSpecial(opponent_map, Owner, shots)
    if tryspecial!=(0,0,0):
        writeCommand(tryspecial[0],tryspecial[1],tryspecial[2])
    else:
        #Menembak single shot
        i = 0
        check = False
        while (i<len(shots) and not(check)):
            x = shots[i][0]
            y = shots[i][1]

            for cell in opponent_map:
                if ((cell['X']==x) and (cell['Y']==y)):
                    if not(cell['Damaged']) and not(cell['Missed']) and not(cell['ShieldHit']) :
                        check = True
                    break
            if not(check) :
                i+=1

        if check :
            target = shots[i]
            writeCommand(1,shots[i][0],shots[i][1])
        else:
            writeCommand(0,0,0)

    #Mengupdate file eksternal shots.txt setelah diupdate dan melakukan command
    with open('shots.txt', 'w') as f:
        for shot in shots :
            f.write(str(shot[0]))
            f.write(",")
            f.write(str(shot[1]))
            f.write("\n")
    return


def searchCell(opponent_map, x, y):
    #mengembalikan cell dari state.json dimana x dan y ditemukan
    for cell in opponent_map:
        if ((cell['X']==x) and (cell['Y']==y)):
            return cell

def placeShips():
    #Meletakan kapal untuk phase 1
    #format : <jenis kapal> <x> <y> <Arah menghadap>
    if (mapsize == 7):
        ships = ['Battleship 0 4 East',
                 'Carrier 6 2 north',
                 'Cruiser 1 0 north',
                 'Destroyer 1 6 East',
                 'Submarine 3 1 East'
                 ]
    elif (mapsize == 10):
        ships = ['Battleship 2 6 East',
                 'Carrier 8 4 north',
                 'Cruiser 1 2 north',
                 'Destroyer 1 8 East',
                 'Submarine 6 1 East'
                 ]
    else:
        ships = ['Battleship 5 7 East',
                 'Carrier 11 12 south',
                 'Cruiser 2 3 north',
                 'Destroyer 3 10 East',
                 'Submarine 9 2 East'
                 ]
    #menuliskan list peletakan kapal ke gameengine
    with open(os.path.join(gameengine_path, shipFile), 'w') as f_out:
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
    gameengine_path = args.WorkingDirectory
    main(args.PlayerKey)
