import xlrd
import csv
import pandas as pd
import numpy as np


def convert_datafile(out_filename, in_filename, cabecera):
    with xlrd.open_workbook(in_filename) as wb:
        sh = wb.sheet_by_index(0)
        with open(out_filename, 'w', newline="") as f:
            c = csv.writer(f)
            for r in range(sh.nrows):
                if r == 0:
                    c.writerow(cabecera)
                else:
                    data = sh.row_values(r)
                    #c.writerow([int(i) for i in data])
                    c.writerow(data)


def excel_to_csv():
    do_maximas = False
    do_jugadores = False
    do_partidos = False
    do_pruebas = True

    if do_jugadores:
        out_filename = "../DATA/players.csv"
        in_filename = "../ORIGINAL/JUGADORES.xlsx"
        cabecera = ['playerid', 'type', 'age', 'height', 'weight', 'fcmax', 'bmi', 'body fat']
        convert_datafile(out_filename, in_filename, cabecera)

    if do_maximas:
        out_filename = "../DATA/maximum.csv"
        in_filename = "../ORIGINAL/MAXIMAS.xlsx"
        cabecera = ['playerid', 'g1', 'g2', 'g3', 'g4', 'g5', 'wing', 'cycloergometer', 'treadmill', 'yoyo', 'tivre']

        convert_datafile(out_filename, in_filename, cabecera)

    if do_partidos:
        for i in range(1, 6):
            in_filename_general = "../ORIGINAL/PARTIDOS/P" + "{0}".format(i) + "_general.xlsx"
            in_filename_jugadores = "../ORIGINAL/PARTIDOS/P" + "{0}".format(i) + "_jugadores.xlsx"
            in_filename_fc = "../ORIGINAL/PARTIDOS/P" + "{0}".format(i) + "_fc.xlsx"

            out_filename_general = "../DATA/PRE/g" + "{0}".format(i) + "_game.csv"
            out_filename_jugadores = "../DATA/PRE/g" + "{0}".format(i) + "_players.csv"
            out_filename_fc = "../DATA/PRE/g" + "{0}".format(i) + "_fc.csv"

            cabecera_general = ['game', 'second', 'livetime', 'ingame', 'quarter', 'atdef', 'pospoints', 'negpoints', 'difference']
            cabecera_jugadores = ['game', 'second', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']
            cabecera_fc = ['second', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']

            convert_datafile(out_filename_general, in_filename_general, cabecera_general)
            convert_datafile(out_filename_jugadores, in_filename_jugadores, cabecera_jugadores)
            convert_datafile(out_filename_fc, in_filename_fc, cabecera_fc)

    if do_pruebas:
        for i in range(1,11):
            in_cinta = "../ORIGINAL/PRUEBAS/CINTA/P" + "{0}".format(i) + ".xlsx"
            in_ciclo = "../ORIGINAL/PRUEBAS/CICLO/P" + "{0}".format(i) + ".xlsx"
            in_wing = "../ORIGINAL/PRUEBAS/WINGATE/P" + "{0}".format(i) + ".xlsx"
            in_yoyo = "../ORIGINAL/PRUEBAS/YOYOTEST/P" + "{0}".format(i) + ".xlsx"
            in_tivre = "../ORIGINAL/PRUEBAS/TIVRE/P" + "{0}".format(i) + ".xlsx"

            out_cinta = "../DATA/PRE/cinta_p" + "{0}".format(i) + ".csv"
            out_ciclo = "../DATA/PRE/ciclo_p" + "{0}".format(i) + ".csv"
            out_wing = "../DATA/PRE/wing_p" + "{0}".format(i) + ".csv"
            out_yoyo = "../DATA/PRE/yoyo_p" + "{0}".format(i) + ".csv"
            out_tivre = "../DATA/PRE/tivre_p" + "{0}".format(i) + ".csv"

            cabecera = ['second','fc']

            convert_datafile(out_cinta, in_cinta, cabecera)
            convert_datafile(out_ciclo, in_ciclo, cabecera)
            convert_datafile(out_wing, in_wing, cabecera)
            convert_datafile(out_yoyo, in_yoyo, cabecera)
            convert_datafile(out_tivre, in_tivre, cabecera)

# <50 -> 0
# <60 -> 1
# <70 -> 2
# <80 -> 3
# <90 -> 4
# <100 -> 5
# de la FC max
def create_edwards():
    fc_data = pd.read_csv("../DATA/fc_database.csv")
    gm_data = pd.read_csv("../DATA/gm_database.csv")

    merge_data = pd.merge(fc_data, gm_data, left_on=['game', 'second'], right_on=['game', 'second'])
    merge_data = merge_data.values
    # 0:game, 1:second, 2:player, 3:fc, 4:playing, 5:state, 6: quarter, 7:atdef, 8:pos, 9:neg, 10:diff
    n_players = 10
    n_games = 5

    # Obtener la FC max de cada jugador en cada partido
    fc_max = pd.read_csv("../DATA/max_fc.csv")
    fc_max = fc_max.values

    my_file = open("../DATA/PRE/edwards.csv", 'wt')
    my_file.write("game,second,player,edwards,time,playing\n")
    for i in range(merge_data.shape[0]):
        game = merge_data[i, 0]
        second = merge_data[i, 1]
        player = merge_data[i, 2]
        fc = merge_data[i, 3]
        playing = merge_data[i, 4]
        state = merge_data[i, 5]

        ed = get_edwards(fc, fc_max[player-1, 6])
        type_time = get_time_from_state(state)

        s = str(game) + "," + str(second) + "," + str(player) + "," + str(ed) + "," + str(type_time)+ "," + str(playing)
        my_file.write(s + "\n")
    my_file.close()


def get_time_from_state(state):
    if state == 1:
        t = 1
    elif state > 1:
        t = 2
    else:
        t = 3
    return t


def get_edwards(fc, fc_max):
    if np.isnan(fc):
        ed = -1
    else:
        pct_fc = fc / fc_max
        if pct_fc < 0.5:
            ed = 0
        elif pct_fc < 0.6:
            ed = 1
        elif pct_fc < 0.7:
            ed = 2
        elif pct_fc < 0.8:
            ed = 3
        elif pct_fc < 0.9:
            ed = 4
        else:
            ed = 5
    return ed


def create_definitive_database_fc(output_filename):
    my_file = open(output_filename, 'wt')
    my_file.write("game,second,player,fc,playing\n")

    n_games = 5
    n_players = 10
    for i_game in range(n_games):
        print(i_game + 1)
        fc_filename = "../DATA/g" + str(i_game + 1) + "_fc.csv"
        pl_filename = "../DATA/g" + str(i_game + 1) + "_players.csv"
        fc_data = pd.read_csv(fc_filename)
        pl_data = pd.read_csv(pl_filename)

        fc_data = fc_data.values
        pl_data = pl_data.values

        for i_second in range(fc_data.shape[0]):
            for i_player in range(n_players):
                fc = fc_data[i_second, i_player + 1]
                pl = pl_data[i_second, i_player + 2]
                if np.isnan(fc):
                    fc = -1
                    pl = -1

                line = str(i_game + 1) + "," + str(i_second + 1) + "," + str(i_player+1) + "," + str(int(fc)) + "," + str(int(pl)) + "\n"
                my_file.write(line)
    my_file.close()

def create_definitive_database_gm(output_filename):
    my_file = open(output_filename, 'wt')
    my_file.write("game,second,state,quarter,atdef,pospoints,negpoints,diff\n")

    n_games = 5
    for i_game in range(n_games):
        print(i_game + 1)
        gm_filename = "../DATA/g" + str(i_game + 1) + "_game.csv"
        gm_data = pd.read_csv(gm_filename)
        gm_data.fillna('', inplace=True)  # empty values are empty strings
        gm_data = gm_data.values

        for i_second in range(gm_data.shape[0]):
            state = gm_data[i_second, 3]
            quarter = gm_data[i_second, 4]
            atdef = gm_data[i_second, 5]
            pos = gm_data[i_second, 6]
            neg = gm_data[i_second, 7]
            diff = gm_data[i_second, 8]

            if atdef == "AT":
                atdef = 1
            elif atdef == "DEF":
                atdef = 0
            else:
                atdef = -1

            if state == "BLJ":
                state = 1
            elif state == "JP":
                state = 2
            elif state == "TL":
                state = 3
            elif state == "TIEMPO":
                state = 4
            else:
                state = 0

            if quarter == "1Q":
                quarter = 1
            elif quarter == "2Q":
                quarter = 2
            elif quarter == "3Q":
                quarter = 3
            elif quarter == "4Q":
                quarter = 4
            elif quarter == "PRO":
                quarter = 5
            else:
                quarter = 0

            line = str(i_game + 1) + "," + str(i_second + 1) + "," + str(state) + "," + str(quarter) + "," + str(atdef) + "," + str(pos) + "," + str(neg) + "," + str(diff) + "\n"
            my_file.write(line)

    my_file.close()

