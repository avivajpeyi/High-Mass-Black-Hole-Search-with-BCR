import bilby
from matplotlib import rcParams


def set_matplotlib_style_settings():
    major, minor = 7, 3
    linewidth = 1.5
    rcParams["font.size"] = 30
    rcParams["font.family"] = "serif"
    rcParams["font.sans-serif"] = ["Computer Modern Sans"]
    rcParams["text.usetex"] = True
    rcParams['axes.labelsize'] = 30
    rcParams['axes.titlesize'] = 30
    rcParams['axes.labelpad'] = 10
    rcParams['axes.linewidth'] = linewidth
    rcParams['axes.edgecolor'] = 'black'
    rcParams['xtick.labelsize'] = 25
    rcParams['ytick.labelsize'] = 25
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'
    rcParams['xtick.major.size'] = major
    rcParams['xtick.minor.size'] = minor
    rcParams['ytick.major.size'] = major
    rcParams['ytick.minor.size'] = minor
    rcParams['xtick.minor.width'] = linewidth
    rcParams['xtick.major.width'] = linewidth
    rcParams['ytick.minor.width'] = linewidth
    rcParams['ytick.major.width'] = linewidth
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True
    rcParams['axes.grid'] = False
    rcParams["axes.titlepad"] = 8


PARAMS = dict(
    chi_eff=dict(latex_label=r"$\chi_{eff}$", range=(-0.8, 0.8)),
    chi_p=dict(latex_label=r"$\chi_{p}$", range=(0, 1)),
    chi_1=dict(latex_label=r"$\chi_1$", range=(0, 1)),
    cos_tilt_1=dict(latex_label=r"$\cos(t1)$", range=(-1, 1)),
    cos_tilt_2=dict(latex_label=r"$\cos(t2)$", range=(-1, 1)),
    cos_theta_12=dict(latex_label=r"$\cos \theta_{12}$", range=(-1, 1)),
    tilt_1=dict(latex_label=r"$tilt_{1}$", range=(0, np.pi)),
    remnant_kick_mag=dict(latex_label=r'$|\vec{v}_k|\ $km/s', range=(0, 3000)),
    chirp_mass=dict(latex_label=r"$M_{c}$", range=(5, 200)),
    mass_1_source=dict(latex_label=r'$m_1^{\mathrm{source}}$', range=(25, 80)),
    mass_2_source=dict(latex_label=r'$m_2^{\mathrm{source}}$', range=(15, 60)),
    luminosity_distance=dict(latex_label='$d_L$', range=(50, 20000)),
    log_snr=dict(latex_label='$\\rm{log}_{10}\ \\rho$)', range=(-1, 3)),
    redshift=dict(latex_label=r'$z$', range=(0, 0.75)),
    mass_ratio=dict(latex_label=r'$q$', range=(0, 1)),
)

set_matplotlib_style_settings()

f = "/hdfs/user/avi.vajpeyi/out_O2_BCRs/chunk7/pe_outdir/out_foreground/result/bcr_O2_chunk7_foreground_data1_1171814476-971924_analysis_H1L1_dynesty_result.json"
prior = bilby.gw.prior.BBHPriorDict(
    filename="/home/avi.vajpeyi/projects/bcr_pipeline/bcr_pipeline/priors/454ns.prior")

r = bilby.gw.result.CBCResult.from_json(f)

r.outdir = '170222_posteriors'
parameters = ["mass_1_source", "mass_2_source", "chi_eff", "redshift"]
r.plot_corner(
    parameters=parameters,
    color="tab:orange",
    labels=[PARAMS[p]['latex_label'] for p in parameters],
    label_kwargs=dict(fontsize=35),
    title_kwargs=dict(fontsize=25),
    labelpad=3,
    range=[PARAMS[p]['range'] for p in parameters],
    plot_datapoints=False,
    max_n_ticks=3,
    filename="170222_source_posterior.png",
    save=True,
)
parameters = ["chirp_mass", "mass_ratio", "chi_1", "luminosity_distance"]
r.plot_corner(
    parameters=parameters,
    color="tab:orange",
    labels=[PARAMS[p]['latex_label'] for p in parameters],
    priors=prior,
    label_kwargs=dict(fontsize=35),
    title_kwargs=dict(fontsize=25),
    labelpad=3,
    #     range=[PARAMS[p]['range'] for p in parameters],
    plot_datapoints=False,
    max_n_ticks=3,
    filename="170222_prior_posterior.png",
    save=True,
)
