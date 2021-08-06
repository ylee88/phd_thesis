if __name__ == '__main__':

    import os
    import sys
    import slugger as slug

    switch = sys.argv[1]

    run_slug = "/Users/ylee/Documents/research/project-git/SlugCode/FDM/1D/Hydro/slugEuler1d > dump.dat"

    ref_par_file = './conv.init'

    sim_pars = slug.pars2dict(ref_par_file)

    sim_pars['sim_cfl'] = 0.7

    if switch == 'rk4':
        prefix = 'weno5_rk4_'
        sim_pars['sim_Torder'] = '4'
        sim_pars['sim_RK'] = '.true.'
    elif switch == 'rk3':
        prefix = 'weno5_rk3_'
        sim_pars['sim_Torder'] = '3'
        sim_pars['sim_RK'] = '.true.'
    elif switch == 'sf3':
        prefix = 'weno5_sf3_'
        sim_pars['sim_Torder'] = '103'
        sim_pars['sim_RK'] = '.false.'
    elif switch == 'pif':
        prefix = 'weno5_pif_'
        sim_pars['sim_Torder'] = '113'
        sim_pars['sim_RK'] = '.false.'

    NN = [32, 64, 128, 256, 512, 1024]

    for N in NN:
        sim_pars['sim_name'] = "'" + prefix + str(N) + "'"
        sim_pars['gr_nx'] = N

        slug.dict2file(sim_pars)

        print("N = ", N, "...")
        os.system(run_slug)
        print("done!")
