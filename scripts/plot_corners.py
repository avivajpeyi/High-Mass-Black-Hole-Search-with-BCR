"""
Script to plot "170222_prior_posterior.png" and "170222_source_posterior.png"
"""

import bilby
import numpy as np
from settings import set_matplotlib_style_settings

RES_PATH = "data/corner_data/170222_result.json"
PRIOR = "data/corner_data/454ns.prior"

set_matplotlib_style_settings()

PARAMS = dict(
    chi_eff=dict(latex_label=r"$\mathbf{\chi_{eff}}$", range=(-0.8, 0.8)),
    chi_p=dict(latex_label=r"$\mathbf{\chi_{p}}$", range=(0, 1)),
    a_1=dict(latex_label=r"$\mathbf{a_1}$", range=(0, 1)),
    chi_1=dict(latex_label=r"$\mathbf{\chi_1}$", range=(-1, 1)),
    cos_tilt_1=dict(latex_label=r"$\mathbf{\cos(t1)}$", range=(-1, 1)),
    cos_tilt_2=dict(latex_label=r"$\mathbf{\cos(t2)}$", range=(-1, 1)),
    cos_theta_12=dict(latex_label=r"$\mathbf{\cos \theta_{12}}$", range=(-1, 1)),
    tilt_1=dict(latex_label=r"$tilt_{1}$", range=(0, np.pi)),
    remnant_kick_mag=dict(latex_label=r"$|\vec{v}_k|\ $km/s", range=(0, 3000)),
    chirp_mass=dict(latex_label=r"$\mathbf{M_{c}}$", range=(5, 100)),
    mass_1_source=dict(latex_label=r"$\mathbf{m_1^{source}}$", range=(25, 80)),
    mass_2_source=dict(latex_label=r"$\mathbf{m_2^{source}}$", range=(15, 60)),
    luminosity_distance=dict(latex_label="$\mathbf{d_L}$", range=(50, 4000)),
    log_snr=dict(latex_label="$\\rm{log}_{10}\ \\rho$)", range=(-1, 3)),
    redshift=dict(latex_label=r"$\mathbf{z}$", range=(0, 1)),
    mass_ratio=dict(latex_label=r"$\mathbf{q}$", range=(0, 1)),
)




def plot_result_corner(r, parameters, fname, prior=None):

    plt_range = [PARAMS[p]["range"] for p in parameters]
    if prior:
        plt_range = [(prior[p].minimum, prior[p].maximum) for p in parameters]

    fig = r.plot_corner(
        parameters=parameters, priors=prior,
        range=plt_range,
        labels=[PARAMS[p]["latex_label"] for p in parameters],
        color="tab:orange", label_kwargs=dict(fontsize=35, labelpad=12), labelpad=0.05,
        title_kwargs=dict(fontsize=25, pad=12), save=False
    )
    fig.savefig(fname, bbox_inches='tight', pad_inches=0.1)


def main():
    print("Plotting Corners")
    prior = bilby.gw.prior.BBHPriorDict(filename=PRIOR)
    r = bilby.gw.result.CBCResult.from_json(RES_PATH)
    r.outdir = "images"

    plot_result_corner(
        r,
        parameters=["mass_1_source", "mass_2_source", "chi_eff", "redshift"],
        fname="images/170222_source_posterior.png",
    )
    plot_result_corner(
        r,
        parameters=["chirp_mass", "mass_ratio", "a_1", "luminosity_distance"],
        fname="images/170222_prior_posterior.png",
        prior=prior

    )


if __name__ == "__main__":
    main()
