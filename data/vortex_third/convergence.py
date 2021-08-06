import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import slugger as slug


def get_fname(sim_name, N):
    init = sim_name + str(N) + "_10000.slug"
    finl = sim_name + str(N) + "_10001.slug"

    return init, finl


def get_L1(sim_name, N):

    dx = 20.0/np.float64(N)
    dxdy = dx*dx
    L1 = {}

    init_fname, finl_fname = get_fname(sim_name, N)

    init_data = slug.load_data2d(init_fname)
    finl_data = slug.load_data2d(finl_fname)

    items = ["dens", "velx", "vely", "pres"]
    for item in items:

        init = getattr(init_data, item)
        finl = getattr(finl_data, item)

        ERR = 0.0

        delta = np.abs(init - finl)
        ERR = np.sum(delta)

        L1[item] = dxdy*ERR
    L1["eTime"] = finl_data.eTime

    return(L1)


def get_df(dir_name, fprefix, NN):

    sim_name = dir_name + "/" + fprefix

    L1_list = []

    for N in NN:
        L1 = get_L1(sim_name, N)
        L1_list.append(L1)

    df = pd.DataFrame(L1_list, index=NN)

    return(df)


NN = np.array([50, 100, 200, 400])

sf3_df = get_df('.', 'weno5_sf3_', NN)
pif_df = get_df('.', 'weno5_pif_', NN)
rk3_df = get_df('.', 'weno5_rk3_', NN)

for df in [sf3_df, pif_df, rk3_df]:
    df['order'] = np.nan
    df['speed_up'] = np.nan
    for i in range(NN.size-1):
        N = NN[i+1]
        n = NN[i]
        df['order'][N] = np.log10(df.dens[n]/df.dens[N])/np.log10(N/n)

    for res in NN:
        df['speed_up'][res] = np.round(df.eTime[res]/rk3_df.eTime[res], 2)
#
# a and b will be used for drawing a line
# a = np.float64(sf3_df.index[2])
# b = sf3_df["dens"][a]

print("======= SF3 =======")
print(sf3_df)
print("======= PIF =======")
print(pif_df)
print("======= RK3 =======")
print(rk3_df)
#

# save to csv
sf3_df.to_csv('./sf3.csv')
pif_df.to_csv('./pif.csv')
rk3_df.to_csv('./rk3.csv')

plt.show()
