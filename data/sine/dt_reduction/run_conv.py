if __name__ == '__main__':

    import os
    import sys
    import slugger as slug

    switch = sys.argv[1]

    run_slug = "/Users/ylee/Documents/research/project-git/SlugCode/FDM/1D/Hydro/slugEuler1d > dump.dat"

    ref_par_file = './conv.init'

    sim_pars = slug.pars2dict(ref_par_file)

    cfl = 0.7
    sim_pars['sim_cfl'] = cfl
    sim_pars['sim_fixDt'] = '.true.'
    dt0 = 0.0218        # dt0; with Nx=16

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

    NN = [16, 32, 64, 128, 256, 512, 1024]

    dt = 0.
    for N in NN:
        dt = dt0*(NN[0]/N)**(5/3)        # dt reduction
        sim_pars['sim_dt'] = dt
        sim_pars['sim_name'] = "'" + prefix + str(N) + "'"
        sim_pars['gr_nx'] = N

        slug.dict2file(sim_pars)

        print("N = ", N, "dt = ", dt, "...")
        os.system(run_slug)
        print("done!")
