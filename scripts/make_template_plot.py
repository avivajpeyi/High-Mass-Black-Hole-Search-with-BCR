import numpy as np
from tqdm import tqdm
from bilby.gw import conversion
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams
rcParams["font.size"] = 20
rcParams["font.family"] = "serif"
rcParams["font.sans-serif"] = ["Computer Modern Sans"]
rcParams["text.usetex"] = False
rcParams['axes.labelsize'] = 30
rcParams['axes.titlesize'] = 30
rcParams['axes.labelpad'] = 20



BANK = "../data/template_bank.csv"
CATALOG = "../data/catalog.csv"


def get_m1m2_grid(m1_range, m2_range, filtering_criteria):
    """Return a meshgrid of m1, m2, z points based on filtering criteria.

    The returned meshgrid can be used to create a contour plot based on the filtering
    criteria

    :param m1_range:
    :param m2_range:
    :param filtering_criteria:
    :return:
    """
    print("plotting m1-m2 contour")
    xs = np.linspace(m1_range[0], m1_range[1], 1000)
    ys = np.linspace(m2_range[0], m2_range[1], 1000)[::-1]
    m1, m2 = np.meshgrid(xs, ys)
    z = np.zeros(shape=(len(xs), len(ys)))
    for nrx, loop_m1 in enumerate(tqdm(xs)):
        for nry, loop_m2 in enumerate(ys):
            if loop_m2 > loop_m1:
                pass  # by definition, we choose only m2 smaller than m1
            if loop_m2 < loop_m1:
                mc = conversion.component_masses_to_chirp_mass(loop_m1, loop_m2)
                M = conversion.component_masses_to_total_mass(loop_m1, loop_m2)
                q = conversion.component_masses_to_mass_ratio(loop_m1, loop_m2)
                if filtering_criteria(loop_m1, loop_m2, mc, q, M) == 1:
                    z[nry][nrx] = 1
    return m1, m2, z


def contour_condition(m1: float, m2: float, mc: float, q: float, M: float) -> int:
    """
    :param m1: mass1 val
    :param m2: mass2 val
    :param mc: chirp mass val
    :param q: mass ratio val
    :param M: total mass val
    :return: 1 if above parameters inside criteria (defined in function), otherwise 0
    """
    if (
        31 <= m1 <= 491
        and 1.32 <= m2 <= 121
        and 0.01 <= q <= 0.98
        and 8 <= mc <= 174
        and 56 <= M <= 496
    ):
        return 1
    else:
        return 0

    
    
def plot_template_bank():
    template_bank = pd.read_csv(BANK, index_col=0)
    catalogs_df = pd.read_csv(CATALOG, index_col=0)
    catalogs_to_keep = ['GWTC-1-confident','IAS', 'PyCBC']
    catalogs_df = catalogs_df[catalogs_df['catalog.shortName'].isin(catalogs_to_keep)]
    
    
    scatter_points = [
                # TEMPLATE BANK
                dict(
                    data=template_bank,
                    plot_kwargs=dict(
                        color="pink", s=0.5, marker=".", alpha=0.05, label="Template Bank"
                    ),
                ),
                # ALL CATALOGUE EVENTS
                dict(
                    data=pd.DataFrame(dict(mass_1=catalogs_df.mass_1_source, mass_2=catalogs_df.mass_2_source)),
                    plot_kwargs=dict(color="blue", s=5, marker="o", label="Catalogue Events"),
                ),
            ]

    prior_line = dict(
            contour_condition=contour_condition,
            plot_kwargs=dict(colors="k", linestyles="--", linewidths=2.0, label="Prior")
        )



    m1_range = [1, 500]
    m2_range = [1, 200]


    fig, ax_m1m2 = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))

    axis_label_kwargs = dict(fontsize="x-large")

    # set labels
    ax_m1m2.set_xlabel("Mass 1", **axis_label_kwargs)
    ax_m1m2.set_ylabel("Mass 2", **axis_label_kwargs)

    # set scales
    ax_m1m2.set_yscale("log")
    ax_m1m2.set_xscale("log")

    # set scale limits
    ax_m1m2.set_xlim(m1_range[0], m1_range[1])
    ax_m1m2.set_ylim(m2_range[0], m2_range[1])

    # contour line
    m1_line, m2_line, m1m2_z = get_m1m2_grid(m1_range, m2_range, prior_line["contour_condition"])

    ax_m1m2.contour(m1_line, m2_line, m1m2_z, [0], **prior_line["plot_kwargs"])

    for scatter_data in scatter_points:
        ax_m1m2.scatter(scatter_data["data"].mass_1, scatter_data["data"].mass_2, **scatter_data["plot_kwargs"])

    ax_m1m2.legend()
    plt.tight_layout()
    plt.savefig("../images/template_bank.png")

plot_template_bank()

