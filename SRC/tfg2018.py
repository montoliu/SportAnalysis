import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def diferencias_maximas():
    data = pd.read_csv("../DATA/max_fc.csv")
    data = data.values

    ciclo_data = data[:, 1]
    cinta_data = data[:, 2]
    wing_data = data[:, 5]
    fc_data = data[:, 6]

    all_data = np.zeros((10, 4))
    all_data[:, 0] = fc_data
    all_data[:, 1] = wing_data
    all_data[:, 2] = ciclo_data
    all_data[:, 3] = cinta_data

    plt.boxplot(all_data)
    plt.ylabel('FC')
    plt.xticks([1,2,3,4], ('Partidos', 'Wing', 'Ciclo', 'Cinta'))
    plt.show()

    f, p = stats.f_oneway(fc_data, wing_data, ciclo_data, cinta_data)
    print(f)
    print(p)

    f, p = stats.f_oneway(fc_data, ciclo_data, cinta_data)
    print(f)
    print(p)


# -------------------------------------------------------------------------------------
def go_tabla_edwards():
    n_games = 5
    n_edwards = 5
    n_players = 10

    ed_data = pd.read_csv("../DATA/PRE/edwards.csv")
    ed_data = ed_data.values
    #0:game, 1:second, 2:player, 3:edwards, 4: time, 5:playing

    pct_data = np.zeros((n_games*n_players*3, 9))
    #0:game, 1:player, 2:time, 3:pct0, 4:pct1, 5:pct2, 6:pct3, 7:pct4, 8:pct5

    i = 0
    for i_game in range(n_games):
        game_id = i_game + 1
        for i_player in range(n_players):
            player_id = i_player + 1

            idx = np.logical_and(ed_data[:, 0] == game_id, ed_data[:, 2] == player_id)

            if np.sum(ed_data[idx, 5] == -1) > 0:
                pct_data[i, :] = np.zeros((1, 9)) + -1
                pct_data[i + 1, :] = np.zeros((1, 9)) + -1
                pct_data[i + 2, :] = np.zeros((1, 9)) + -1
            else:
                # wt
                N = sum(idx)
                pct_data[i, 0] = game_id
                pct_data[i, 1] = player_id
                pct_data[i, 2] = 3
                pct_data[i, 3] = np.sum(ed_data[idx, 3] == 0) / N
                pct_data[i, 4] = np.sum(ed_data[idx, 3] == 1) / N
                pct_data[i, 5] = np.sum(ed_data[idx, 3] == 2) / N
                pct_data[i, 6] = np.sum(ed_data[idx, 3] == 3) / N
                pct_data[i, 7] = np.sum(ed_data[idx, 3] == 4) / N
                pct_data[i, 8] = np.sum(ed_data[idx, 3] == 5) / N

                #tt
                idx_tt = np.logical_and(idx, ed_data[:, 5] == 1)  # esta jugando
                idx_tt = np.logical_and(idx_tt, ed_data[:, 4] <= 2)  # el tiempo es TT o LT
                N = np.sum(idx_tt)
                pct_data[i + 1, 0] = game_id
                pct_data[i + 1, 1] = player_id
                pct_data[i + 1, 2] = 2
                pct_data[i + 1, 3] = np.sum(ed_data[idx_tt, 3] == 0) / N
                pct_data[i + 1, 4] = np.sum(ed_data[idx_tt, 3] == 1) / N
                pct_data[i + 1, 5] = np.sum(ed_data[idx_tt, 3] == 2) / N
                pct_data[i + 1, 6] = np.sum(ed_data[idx_tt, 3] == 3) / N
                pct_data[i + 1, 7] = np.sum(ed_data[idx_tt, 3] == 4) / N
                pct_data[i + 1, 8] = np.sum(ed_data[idx_tt, 3] == 5) / N

                # tt
                idx_lt = np.logical_and(idx, ed_data[:, 5] == 1)  # esta jugando
                idx_lt = np.logical_and(idx_lt, ed_data[:, 4] == 1)  # el timepo es LT
                N = np.sum(idx_lt)
                pct_data[i + 2, 0] = game_id
                pct_data[i + 2, 1] = player_id
                pct_data[i + 2, 2] = 1

                pct_data[i + 2, 3] = np.sum(ed_data[idx_lt, 3] == 0) / N
                pct_data[i + 2, 4] = np.sum(ed_data[idx_lt, 3] == 1) / N
                pct_data[i + 2, 5] = np.sum(ed_data[idx_lt, 3] == 2) / N
                pct_data[i + 2, 6] = np.sum(ed_data[idx_lt, 3] == 3) / N
                pct_data[i + 2, 7] = np.sum(ed_data[idx_lt, 3] == 4) / N
                pct_data[i + 2, 8] = np.sum(ed_data[idx_lt, 3] == 5) / N

            i = i + 3

    # 0:game, 1:player, 2:time, 3:pct0, 4:pct1, 5:pct2, 6:pct3, 7:pct4, 8:pct5
    # ahora las medias

    print(["{0:0.2f}".format(100*k) for k in np.mean(pct_data[pct_data[:, 2] == 3, 3:9], axis=0)])
    print(["{0:0.2f}".format(100*k) for k in np.mean(pct_data[pct_data[:, 2] == 2, 3:9], axis=0)])
    print(["{0:0.2f}".format(100*k) for k in np.mean(pct_data[pct_data[:, 2] == 1, 3:9], axis=0)])

    print(["{0:0.2f}".format(100*k) for k in np.std(pct_data[pct_data[:, 2] == 3, 3:9], axis=0)])
    print(["{0:0.2f}".format(100*k) for k in np.std(pct_data[pct_data[:, 2] == 2, 3:9], axis=0)])
    print(["{0:0.2f}".format(100*k) for k in np.std(pct_data[pct_data[:, 2] == 1, 3:9], axis=0)])


def go_tabla_fc():
    fc_filename = "../DATA/fc_database.csv"
    gm_filename = "../DATA/gm_database.csv"

    fc_data = pd.read_csv(fc_filename)
    gm_data = pd.read_csv(gm_filename)

    new_data = pd.merge(fc_data, gm_data, left_on=['game', 'second'], right_on=['game', 'second'])
    new_data = new_data.values
    # 0:game, 1:second, 2:player, 3:fc, 4:playing, 5:state, 6: quarter, 7:atdef, 8:pos, 9:neg, 10:diff
    n_players = 10
    n_games = 5

    fc_table_abs = np.zeros((n_players*n_games*3, 7))
    fc_table_rel = np.zeros((n_players*n_games*3, 7))

    # 0:game, 1:player, 2:time, 3:fc_mean, 4:fc_std, 5:min, 6:max

    fc_max = np.zeros((n_players, 1))
    i = 0
    for i_game in range(n_games):
        game_id = i_game + 1
        for i_player in range(n_players):
            player_id = i_player + 1
            idx_wt = np.logical_and(new_data[:, 0] == game_id, new_data[:, 2] == player_id)  # todas las filas del jugador en ese partido
            idx_tt = np.logical_and(idx_wt, new_data[:, 5] > 0)  # solo las que el estado es no break (0)
            idx_tt = np.logical_and(idx_tt, new_data[:, 4] == 1)  # y esta jugando
            idx_lt = np.logical_and(idx_wt, new_data[:, 5] == 1)  # solo las que el estado es Live ball (1)
            idx_lt = np.logical_and(idx_lt, new_data[:, 4] == 1)  # y esta jugando

            if np.max(new_data[idx_wt, 3]) > fc_max[i_player]:
                fc_max[i_player] = np.max(new_data[idx_wt, 3])

            mean_wt = np.mean(new_data[idx_wt, 3])

            if mean_wt > 0:  #ha jugado
                mean_tt = np.mean(new_data[idx_tt, 3])
                mean_lt = np.mean(new_data[idx_lt, 3])

                std_wt = np.std(new_data[idx_wt, 3])
                std_tt = np.std(new_data[idx_tt, 3])
                std_lt = np.std(new_data[idx_lt, 3])

                min_wt = np.min(new_data[idx_wt, 3])
                min_tt = np.min(new_data[idx_tt, 3])
                min_lt = np.min(new_data[idx_lt, 3])

                max_wt = np.max(new_data[idx_wt, 3])
                max_tt = np.max(new_data[idx_tt, 3])
                max_lt = np.max(new_data[idx_lt, 3])
                
                
            else:
                mean_tt = -1
                mean_lt = -1

                std_wt = -1
                std_tt = -1
                std_lt = -1

                min_wt = -1
                min_tt = -1
                min_lt = -1

                max_wt = -1
                max_tt = -1
                max_lt = -1

            fc_table_abs[i, 0] = game_id
            fc_table_abs[i, 1] = player_id
            fc_table_abs[i, 2] = 1  #WT
            fc_table_abs[i, 3] = mean_wt
            fc_table_abs[i, 4] = std_wt
            fc_table_abs[i, 5] = min_wt
            fc_table_abs[i, 6] = max_wt

            fc_table_abs[i+1, 0] = game_id
            fc_table_abs[i+1, 1] = player_id
            fc_table_abs[i+1, 2] = 2  #WT
            fc_table_abs[i+1, 3] = mean_tt
            fc_table_abs[i+1, 4] = std_tt
            fc_table_abs[i+1, 5] = min_tt
            fc_table_abs[i+1, 6] = max_tt

            fc_table_abs[i+2, 0] = game_id
            fc_table_abs[i+2, 1] = player_id
            fc_table_abs[i+2, 2] = 3  #WT
            fc_table_abs[i+2, 3] = mean_lt
            fc_table_abs[i+2, 4] = std_lt
            fc_table_abs[i+2, 5] = min_lt
            fc_table_abs[i+2, 6] = max_lt

            # relativo
            mean_wt = np.mean(new_data[idx_wt, 3] / fc_max[i_player, 0])

            if mean_wt > 0:  # ha jugado
                mean_tt = np.mean(new_data[idx_tt, 3] / fc_max[i_player, 0])
                mean_lt = np.mean(new_data[idx_lt, 3] / fc_max[i_player, 0])

                std_wt = np.std(new_data[idx_wt, 3] / fc_max[i_player, 0])
                std_tt = np.std(new_data[idx_tt, 3] / fc_max[i_player, 0])
                std_lt = np.std(new_data[idx_lt, 3] / fc_max[i_player, 0])

                min_wt = np.min(new_data[idx_wt, 3] / fc_max[i_player, 0])
                min_tt = np.min(new_data[idx_tt, 3] / fc_max[i_player, 0])
                min_lt = np.min(new_data[idx_lt, 3] / fc_max[i_player, 0])

                max_wt = np.max(new_data[idx_wt, 3] / fc_max[i_player, 0])
                max_tt = np.max(new_data[idx_tt, 3] / fc_max[i_player, 0])
                max_lt = np.max(new_data[idx_lt, 3] / fc_max[i_player, 0])
            else:
                mean_tt = -1
                mean_lt = -1

                std_wt = -1
                std_tt = -1
                std_lt = -1

                min_wt = -1
                min_tt = -1
                min_lt = -1

                max_wt = -1
                max_tt = -1
                max_lt = -1
           
            fc_table_rel[i, 0] = game_id
            fc_table_rel[i, 1] = player_id
            fc_table_rel[i, 2] = 1  #WT
            fc_table_rel[i, 3] = mean_wt 
            fc_table_rel[i, 4] = std_wt
            fc_table_rel[i, 5] = min_wt
            fc_table_rel[i, 6] = max_wt

            fc_table_rel[i+1, 0] = game_id
            fc_table_rel[i+1, 1] = player_id
            fc_table_rel[i+1, 2] = 2  #WT
            fc_table_rel[i+1, 3] = mean_tt
            fc_table_rel[i+1, 4] = std_tt
            fc_table_rel[i+1, 5] = min_tt
            fc_table_rel[i+1, 6] = max_tt

            fc_table_rel[i+2, 0] = game_id
            fc_table_rel[i+2, 1] = player_id
            fc_table_rel[i+2, 2] = 3  #WT
            fc_table_rel[i+2, 3] = mean_lt
            fc_table_rel[i+2, 4] = std_lt
            fc_table_rel[i+2, 5] = min_lt
            fc_table_rel[i+2, 6] = max_lt

            i = i + 3

    # calcular valores tabla final
    idx_wt = np.logical_and(fc_table_abs[:, 2] == 1, fc_table_abs[:, 3] > 0)
    idx_tt = np.logical_and(fc_table_abs[:, 2] == 2, fc_table_abs[:, 3] > 0)
    idx_lt = np.logical_and(fc_table_abs[:, 2] == 3, fc_table_abs[:, 3] > 0)

    line_wt = str(np.mean(fc_table_abs[idx_wt, 3])) + "," + str(np.std(fc_table_abs[idx_wt, 3])) + "," + str(np.min(fc_table_abs[idx_wt, 5])) + "," + str(np.max(fc_table_abs[idx_wt, 6]))
    line_tt = str(np.mean(fc_table_abs[idx_tt, 3])) + "," + str(np.std(fc_table_abs[idx_tt, 3])) + "," + str(np.min(fc_table_abs[idx_tt, 5])) + "," + str(np.max(fc_table_abs[idx_tt, 6]))
    line_lt = str(np.mean(fc_table_abs[idx_lt, 3])) + "," + str(np.std(fc_table_abs[idx_lt, 3])) + "," + str(np.min(fc_table_abs[idx_lt, 5])) + "," + str(np.max(fc_table_abs[idx_lt, 6]))

    print(line_wt)
    print(line_tt)
    print(line_lt)

    line_wt = str(np.mean(fc_table_rel[idx_wt, 3])) + "," + str(np.std(fc_table_rel[idx_wt, 3])) + "," + str(np.min(fc_table_rel[idx_wt, 5])) + "," + str(np.max(fc_table_rel[idx_wt, 6]))
    line_tt = str(np.mean(fc_table_rel[idx_tt, 3])) + "," + str(np.std(fc_table_rel[idx_tt, 3])) + "," + str(np.min(fc_table_rel[idx_tt, 5])) + "," + str(np.max(fc_table_rel[idx_tt, 6]))
    line_lt = str(np.mean(fc_table_rel[idx_lt, 3])) + "," + str(np.std(fc_table_rel[idx_lt, 3])) + "," + str(np.min(fc_table_rel[idx_lt, 5])) + "," + str(np.max(fc_table_rel[idx_lt, 6]))

    print(line_wt)
    print(line_tt)
    print(line_lt)


def get_max_fc_pruebas():
    n_players = 10
    fc_max = np.zeros((n_players, 7))
    for i in range(n_players):
        in_ciclo = "../DATA/ciclo_p" + "{0}".format(i+1) + ".csv"
        in_cinta = "../DATA/cinta_p" + "{0}".format(i+1) + ".csv"
        in_tivre = "../DATA/tivre_p" + "{0}".format(i+1) + ".csv"
        in_yoyo = "../DATA/yoyo_p" + "{0}".format(i+1) + ".csv"
        in_wing = "../DATA/wing_p" + "{0}".format(i+1) + ".csv"

        data_ciclo = pd.read_csv(in_ciclo)
        data_cinta = pd.read_csv(in_cinta)
        data_tivre = pd.read_csv(in_tivre)
        data_yoyo = pd.read_csv(in_yoyo)
        data_wing = pd.read_csv(in_wing)

        data_ciclo = data_ciclo.values
        data_cinta = data_cinta.values
        data_tivre = data_tivre.values
        data_yoyo = data_yoyo.values
        data_wing = data_wing.values

        fc_max[i, 0] = i+1
        fc_max[i, 1] = np.max(data_ciclo[:, 1])
        fc_max[i, 2] = np.max(data_cinta[:, 1])
        fc_max[i, 3] = np.max(data_tivre[:, 1])
        fc_max[i, 4] = np.max(data_yoyo[:, 1])
        fc_max[i, 5] = np.max(data_wing[:, 1])

    #partido
    data_games = pd.read_csv("../DATA/fc_database.csv")
    data_games = data_games.values
    for i in range(n_players):
        idx = data_games[:, 2] == i+1
        fc_max[i, 6] = np.max(data_games[idx, 3])

    print(fc_max)

    df = pd.DataFrame(fc_max, columns= ['player', 'ciclo', 'cinta', 'tivre', 'yoyo', 'wing', 'game'])
    df.to_csv("../DATA/max_fc.csv", index=False)


def go_tabla_pct_pruebas():
    n_players = 10
    n_games = 5

    fc_pruebas = pd.read_csv("../DATA/max_fc.csv")
    fc_pruebas = fc_pruebas.values

    fc_data = pd.read_csv("../DATA/fc_database.csv")
    gm_data = pd.read_csv("../DATA/gm_database.csv")

    fc_games = pd.merge(fc_data, gm_data, left_on=['game', 'second'], right_on=['game', 'second'])
    fc_games = fc_games.values
    # 0:game, 1:second, 2:player, 3:fc, 4:playing, 5:state, 6: quarter, 7:atdef, 8:pos, 9:neg, 10:diff

    out_data = np.zeros((n_games*n_players*3,6))
    # 0:game, 1:player, 2:time, 3: pct_ciclo, 4: pct_cinta, 5:pct_wing

    i = 0
    for i_game in range(n_games):
        game_id = i_game + 1
        for i_player in range(n_players):
            player_id = i_player + 1
            fc_cinta = fc_pruebas[i_player, 1]
            fc_ciclo = fc_pruebas[i_player, 2]
            fc_wing = fc_pruebas[i_player, 5]

            idx = np.logical_and(fc_games[:, 0] == game_id, fc_games[:, 2] == player_id)

            #wt
            idx_wt_cinta = np.logical_and(idx, fc_games[:, 3] > fc_cinta)
            idx_wt_ciclo = np.logical_and(idx, fc_games[:, 3] > fc_ciclo)
            idx_wt_wing = np.logical_and(idx, fc_games[:, 3] > fc_wing)

            # tt
            idx_tt = np.logical_and(idx, fc_games[:, 5] > 0)
            idx_tt_cinta = np.logical_and(idx_tt, fc_games[:, 3] > fc_cinta)
            idx_tt_ciclo = np.logical_and(idx_tt, fc_games[:, 3] > fc_ciclo)
            idx_tt_wing = np.logical_and(idx_tt, fc_games[:, 3] > fc_wing)

            # tt
            idx_lt = np.logical_and(idx, fc_games[:, 5] == 1)
            idx_lt_cinta = np.logical_and(idx_lt, fc_games[:, 3] > fc_cinta)
            idx_lt_ciclo = np.logical_and(idx_lt, fc_games[:, 3] > fc_ciclo)
            idx_lt_wing = np.logical_and(idx_lt, fc_games[:, 3] > fc_wing)

            out_data[i, 0] = game_id
            out_data[i, 1] = player_id
            out_data[i, 2] = 1
            out_data[i + 1, 0] = game_id
            out_data[i + 1, 1] = player_id
            out_data[i + 1, 2] = 2
            out_data[i + 2, 0] = game_id
            out_data[i + 2, 1] = player_id
            out_data[i + 2, 2] = 3

            if np.sum(idx) > 0:  #the player played the game
                out_data[i, 3] = np.sum(idx_wt_cinta) / np.sum(idx)
                out_data[i, 4] = np.sum(idx_wt_ciclo) / np.sum(idx)
                out_data[i, 5] = np.sum(idx_wt_wing) / np.sum(idx)

                out_data[i+1, 3] = np.sum(idx_tt_cinta) / np.sum(idx_tt)
                out_data[i+1, 4] = np.sum(idx_tt_ciclo) / np.sum(idx_tt)
                out_data[i+1, 5] = np.sum(idx_tt_wing) / np.sum(idx_tt)

                out_data[i+2, 3] = np.sum(idx_lt_cinta) / np.sum(idx_lt)
                out_data[i+2, 4] = np.sum(idx_lt_ciclo) / np.sum(idx_lt)
                out_data[i+2, 5] = np.sum(idx_lt_wing) / np.sum(idx_lt)
            else:
                out_data[i, 3] = -1
                out_data[i, 4] = -1
                out_data[i, 5] = -1

                out_data[i+1, 3] = -1
                out_data[i+1, 4] = -1
                out_data[i+1, 5] = -1

                out_data[i+2, 3] = -1
                out_data[i+2, 4] = -1
                out_data[i+2, 5] = -1
            i = i + 3
    # tabla final

    for i_game in range(n_games):
        game_id = i_game + 1

        idx_wt = np.logical_and(out_data[:, 0] == game_id, out_data[:, 2] == 1)
        idx_wt = np.logical_and(idx_wt, out_data[:, 3] > 0)

        idx_tt = np.logical_and(out_data[:, 0] == game_id, out_data[:, 2] == 2)
        idx_tt = np.logical_and(idx_tt, out_data[:, 3] > 0)

        idx_lt = np.logical_and(out_data[:, 0] == game_id, out_data[:, 2] == 3)
        idx_lt = np.logical_and(idx_lt, out_data[:, 3] > 0)

        #WT
        mean_ciclo = np.mean(out_data[idx_wt, 3])
        mean_cinta = np.mean(out_data[idx_wt, 4])
        mean_wing = np.mean(out_data[idx_wt, 5])

        std_ciclo = np.std(out_data[idx_wt, 3])
        std_cinta = np.std(out_data[idx_wt, 4])
        std_wing = np.std(out_data[idx_wt, 5])

        linea = str(game_id) + " WT " + "{0:0.2f}".format(100*mean_ciclo) + " " + "{0:0.2f}".format(100*std_ciclo) + " " + "{0:0.2f}".format(100*mean_cinta) + " " + "{0:0.2f}".format(100*std_cinta) + " " + "{0:0.2f}".format(100*mean_wing) + " " + "{0:0.2f}".format(100*std_wing)
        print(linea)

        #TT
        mean_ciclo = np.mean(out_data[idx_tt, 3])
        mean_cinta = np.mean(out_data[idx_tt, 4])
        mean_wing = np.mean(out_data[idx_tt, 5])

        std_ciclo = np.std(out_data[idx_tt, 3])
        std_cinta = np.std(out_data[idx_tt, 4])
        std_wing = np.std(out_data[idx_tt, 5])

        linea = str(game_id) + " TT " + "{0:0.2f}".format(100*mean_ciclo) + " " + "{0:0.2f}".format(100*std_ciclo) + " " + "{0:0.2f}".format(100*mean_cinta) + " " + "{0:0.2f}".format(100*std_cinta) + " " + "{0:0.2f}".format(100*mean_wing) + " " + "{0:0.2f}".format(100*std_wing)
        print(linea)

        #LT
        mean_ciclo = np.mean(out_data[idx_lt, 3])
        mean_cinta = np.mean(out_data[idx_lt, 4])
        mean_wing = np.mean(out_data[idx_lt, 5])

        std_ciclo = np.std(out_data[idx_lt, 3])
        std_cinta = np.std(out_data[idx_lt, 4])
        std_wing = np.std(out_data[idx_lt, 5])

        linea = str(game_id) + " LT " + "{0:0.2f}".format(100*mean_ciclo) + " " + "{0:0.2f}".format(100*std_ciclo) + " " + "{0:0.2f}".format(100*mean_cinta) + " " + "{0:0.2f}".format(100*std_cinta) + " " + "{0:0.2f}".format(100*mean_wing) + " " + "{0:0.2f}".format(100*std_wing)
        print(linea)