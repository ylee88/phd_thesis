import slugger as slug

if __name__ == '__main__':

    import os
    import sys

    switch = sys.argv[1]

    run_slug = "cafrun -np 4 /Users/ylee/Documents/research/project-git/SlugCode/FDM/2D/Hydro/unsplit/slugEuler2d > dump.dat"

    ref_par_file = './conv.init'

    sim_pars = slug.pars2dict(ref_par_file)

    if switch == 'rk3':
        prefix = 'weno5_rk3_'
        sim_pars['sim_cfl'] = 0.4
        sim_pars['sim_Torder'] = '3'
        sim_pars['sim_RK'] = '.true.'

    elif switch == 'sf3':
        prefix = 'weno5_sf3_'
        sim_pars['sim_cfl'] = 0.4
        sim_pars['sim_Torder'] = '103'
        sim_pars['sim_RK'] = '.false.'

    elif switch == 'pif':
        prefix = 'weno5_pif_'
        sim_pars['sim_cfl'] = 0.4
        sim_pars['sim_Torder'] = '113'
        sim_pars['sim_RK'] = '.false.'

    NN = [50, 100, 200, 400]

    for N in NN:
        sim_pars['sim_name'] = "'" + prefix + str(N) + "'"
        sim_pars['gr_nx'] = N
        sim_pars['gr_ny'] = N

        slug.dict2file(sim_pars)

        print("N = ", N, "...")
        os.system(run_slug)
        print("done!")
