import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def deferencias_maximas():
    data = pd.read_csv("../DATA/maximas.csv")
    data = data.values
    fc_data = data[:,1:6]
    wing_data = data[:,6]
    ciclo_data = data[:, 7]
    cinta_data = data[:,8]
    yoyot1_data = data[:, 9]
    tivre_data = data[:, 10]
    mean_fc = np.nanmean(fc_data, axis=1)

    all_data = np.zeros((10, 6))
    all_data[:, 0] = mean_fc
    all_data[:, 1] = wing_data
    all_data[:, 2] = ciclo_data
    all_data[:, 3] = cinta_data
    all_data[:, 4] = yoyot1_data
    all_data[:, 5] = tivre_data

    #plt.boxplot(all_data)
    #plt.ylabel('FC')
    #plt.xticks([1,2,3,4,5,6], ('Partidos', 'Wing', 'Ciclo', 'Cinta','Yo Yo T1', 'Tivre'))
    #plt.show()

    f, p = stats.f_oneway(mean_fc, wing_data, ciclo_data, cinta_data, yoyot1_data, tivre_data)
    print(f)
    print(p)

    f, p = stats.f_oneway(mean_fc, ciclo_data, cinta_data, yoyot1_data, tivre_data)
    print(f)
    print(p)

    #Devuelve The computed F-value of the test. y The associated p-value from the F-distribution