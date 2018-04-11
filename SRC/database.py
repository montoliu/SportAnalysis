import xlrd
import csv


def convert_datafile(out_filename, in_filename, cabecera):
    with xlrd.open_workbook(in_filename) as wb:
        sh = wb.sheet_by_index(0)
        with open(out_filename, 'w', newline="") as f:
            c = csv.writer(f)
            for r in range(sh.nrows):
                if r == 0:
                    c.writerow(cabecera)
                else:
                    c.writerow(sh.row_values(r))

def create_database():

    do_maximas = False
    do_jugadores = False
    do_partidos = True

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

            out_filename_general = "../DATA/g" + "{0}".format(i) + "_game.csv"
            out_filename_jugadores = "../DATA/g" + "{0}".format(i) + "_players.csv"
            out_filename_fc = "../DATA/g" + "{0}".format(i) + "_fc.csv"

            cabecera_general = ['game', 'second', 'livetime', 'ingame', 'quarter', 'atdef', 'pospoints', 'negpoints', 'difference']
            cabecera_jugadores = ['game', 'second', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']
            cabecera_fc = ['second', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10']

            convert_datafile(out_filename_general, in_filename_general, cabecera_general)
            convert_datafile(out_filename_jugadores, in_filename_jugadores, cabecera_jugadores)
            convert_datafile(out_filename_fc, in_filename_fc, cabecera_fc)