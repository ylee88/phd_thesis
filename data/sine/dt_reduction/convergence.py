import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DENS_VAR = 1
VELX_VAR = 2
PRES_VAR = 3


def get_fname(sim_name, N):
    init = sim_name + str(N) + "_10000.dat"
    finl = sim_name + str(N) + "_10001.dat"

    return init, finl


def get_L1(sim_name, N):

    dx = 1.0/np.float64(N)
    L1 = {}

    init_fname, finl_fname = get_fname(sim_name, N)

    init_data = np.loadtxt(init_fname)
    finl_data = np.loadtxt(finl_fname)

    nvars = [DENS_VAR, VELX_VAR, PRES_VAR]
    items = ["dens", "velx", "pres"]

    for nvar, item in zip(nvars, items):

        init = init_data[:, nvar]
        finl = finl_data[:, nvar]

        ERR = 0.0

        for i in range(len(init)):

            ref = init[i]

            delta = abs(finl[i]-ref)
            ERR = ERR + delta

        L1[item] = dx*ERR

    return(L1)


def get_df(dir_name, fprefix, NN):

    sim_name = dir_name + "/" + fprefix

    L1_list = []

    for N in NN:
        L1 = get_L1(sim_name, N)
        L1_list.append(L1)

    df = pd.DataFrame(L1_list, index=NN)

    return(df)


NN = np.array([16, 32, 64, 128, 256, 512, 1024])

sf3_df = get_df('.', 'slug_weno5_sf3_', NN)
rk3_df = get_df('.', 'slug_weno5_rk3_', NN)
pif_df = get_df('.', 'slug_weno5_pif_', NN)

for df in [sf3_df, rk3_df, pif_df]:
    df['order'] = np.nan
    for i in range(NN.size-1):
        N = NN[i+1]
        n = NN[i]
        df['order'][N] = np.log10(df.dens[n]/df.dens[N])/np.log10(N/n)

print("======= ADER-SF3 =======")
print(sf3_df)
print("========= RK 3 =========")
print(rk3_df)
print("========= PIF =========")
print(pif_df)

sf3_df.to_csv('./sf3.csv')
rk3_df.to_csv('./rk3.csv')
pif_df.to_csv('./pif.csv')

a = np.float64(sf3_df.index[3])
b = sf3_df["dens"][a]
fig = plt.figure(dpi=160)

soln = fig.add_subplot(1, 1, 1)

soln.plot(NN, (b*a**3)*(NN)**(-3.), 'b--', label='$\Delta x^3$')
soln.plot(NN, (b*a**4)*(NN)**(-4.), 'r--', label='$\Delta x^4$')

soln.plot(rk3_df["dens"], 'gs', label="WENO5_RK3")
soln.plot(sf3_df["dens"], 'bx', label="WENO5_SF3")
soln.plot(pif_df["dens"], 'cd', label="WENO5_PIF")

soln.loglog()
soln.legend()

soln.set_xlabel("Grid Resolution")
soln.set_ylabel("$L_{1}$ Error")


plt.show()
