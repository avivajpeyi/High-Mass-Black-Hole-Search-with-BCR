"""
Module to plot "template_bank.png"
"""

import numpy as np
import pandas as pd
from bilby.gw import conversion
from matplotlib import pyplot as plt
from settings import set_matplotlib_style_settings, line_annotate
from matplotlib.patches import Polygon
import matplotlib.patches as mpatches
from tqdm import tqdm
from matplotlib import rcParams

BANK = "data/template_bank.csv"
INJECTION = "data/chunk14/injection_triggers.csv"
BACKGROUND = "data/chunk14/background_triggers.csv"
FOREGROUND = "data/chunk14/foreground_triggers.csv"
CATALOG = "data/catalog.csv"

ZORDER = dict(
    qline=3,
    regions=0,
    region_text=4,
    upper_shade=1,
    prior=1,
    filter=2,

)

N = 1000
PRI_COL, FILT_COL = "teal", "gold"


def add_shaded_regions(ax):
    xlim, ylim = ax.get_xlim()[1], ax.get_ylim()[1]

    # Make the shaded region for m2 > m1
    verts = [(0, 0), (0, 1000), (1000,1000)]
    poly = Polygon(verts, facecolor='white', alpha=0.6, zorder=ZORDER['upper_shade'])
    ax.add_patch(poly)

    BNS = dict(min=[1,1], max=[3,3])
    BBH = dict(min=[5,5], max=[95,95])
    IMBH = dict(min=[5, 5], max=[1000,1000])
    NSBH = dict(min=[5,1], max=[1000,3])
    BNS_COL = "tab:blue"
    GAP_COL = "tab:green"
    BBH_COL = "tab:red"
    IMBH_COL = "tab:purple"
    NSBH_COL = "tab:orange"

    alpha = 0.5
    # Make the BNS region

    verts = [
        (BNS['min'][0], BNS['min'][1]),
        (BNS['min'][0], BNS['max'][1]),
        (BNS['max'][0], BNS['max'][1]),
        (BNS['max'][0], BNS['min'][1])
    ]
    poly = Polygon(verts, facecolor=BNS_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    ax.annotate("BNS", xy=(BNS['min'][0], BNS['max'][1]), ha='left', va='top', xycoords='data',
                c=BNS_COL, zorder=ZORDER['region_text'])

    # Make the mass-gap region
    verts = [
        (BNS['max'][0], BNS['min'][1]),
        (BNS['max'][0], BNS['max'][1]),
        (BNS['min'][0], BNS['max'][1]),
        (BNS['min'][0], NSBH['min'][0]),
        (BNS['max'][0], NSBH['min'][0]),
        (BNS['max'][0], NSBH['max'][0]),
        (NSBH['min'][0], NSBH['max'][0]),
        (NSBH['min'][0], NSBH['min'][0]),
        (NSBH['max'][0], NSBH['min'][0]),
        (NSBH['max'][0], BNS['max'][1]),
        (NSBH['min'][0], NSBH['max'][1]),
        (NSBH['min'][0], NSBH['min'][1]),
    ]
    poly = Polygon(verts, facecolor=GAP_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    ax.annotate("MASS GAP", xy=(BNS['max'][0], ylim), ha='left', va='top', xycoords='data',
                c=GAP_COL, zorder=ZORDER['region_text'], rotation=90)

    # Make the NSBH region
    verts = [
        (NSBH['min'][0], NSBH['min'][1]),
        (NSBH['min'][0], NSBH['max'][1]),
        (NSBH['max'][0], NSBH['max'][1]),
        (NSBH['max'][0], NSBH['min'][1])
    ]
    poly = Polygon(verts, facecolor=NSBH_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    verts = [
        (NSBH['min'][1], NSBH['min'][0]),
        (NSBH['max'][1], NSBH['min'][0]),
        (NSBH['max'][1], NSBH['max'][0]),
        (NSBH['min'][1], NSBH['max'][0])
    ]
    poly = Polygon(verts, facecolor=NSBH_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    ax.annotate("NSBH", xy=(1.5, ylim), ha='left', va='top', xycoords='data',
                c=NSBH_COL, zorder=ZORDER['region_text'], rotation=90)

    # Make the BBH region
    m1s = np.linspace(BBH['min'][0], BBH['max'][0], 1000)
    m2s = _get_m2_from_m1_for_imbh_boundary(m1s)
    verts = [
        (BBH['max'][0], BBH['min'][1]),
        (BBH['min'][0], BBH['min'][1]),
        (BBH['min'][0], BBH['max'][1]),
        *zip(m1s, m2s),
        # IMBH boundary curve
    ]
    poly = Polygon(verts, facecolor=BBH_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    ax.annotate("BBH", xy=(5, 75), ha='left', va='top', xycoords='data',
                c=BBH_COL, zorder=ZORDER['region_text'], rotation=90)

    # Make the IMBH region
    m1s = np.linspace(BBH['max'][0], BBH['min'][0], 1000)
    m2s = _get_m2_from_m1_for_imbh_boundary(m1s)
    verts = [
        (IMBH['max'][0], IMBH['min'][1]),
        (BBH['max'][0], IMBH['min'][1]),
        *zip(m1s, m2s),
        (IMBH['min'][0], BBH['max'][1]),
        (IMBH['min'][0], IMBH['max'][1]),
        (IMBH['max'][0], IMBH['max'][1]),
        # IMBH boundary curve
    ]
    poly = Polygon(verts, facecolor=IMBH_COL, alpha=alpha, zorder=ZORDER['regions'])
    ax.add_patch(poly)
    ax.annotate("IMBH", xy=(5, ylim), ha='left', va='top', xycoords='data',
                c=IMBH_COL, zorder=ZORDER['region_text'], rotation=90)

def _get_m2_from_m1_for_imbh_boundary(m1):
    return 100 - m1



def get_m1m2_grid(m1_range, m2_range, filtering_criteria):
    """Return a meshgrid of m1, m2, z points based on filtering criteria.

    The returned meshgrid can be used to create a contour plot based on the filtering
    criteria

    :param m1_range:
    :param m2_range:
    :param filtering_criteria:
    :return:
    """
    xs = np.geomspace(m1_range[0], m1_range[1], N)
    ys = np.geomspace(m2_range[0], m2_range[1], N)[::-1]
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


def add_q_lines(ax):
    m1 = np.array([1.0, 10000.0])
    kwargs = dict(c='k', linestyle='--', zorder=ZORDER['qline'], lw=3.0)
    for q, m1_text in zip([1.0, 1.0 / 10.0, 1.0/100.0], [325, 375, 525]):
        m2 = m1 * q
        line,  = ax.plot(m1, m2, **kwargs)
        xytext=(0, 10)
        if q==1.0/10.0:
            xytext=(0, -25)
        line_annotate( f'$q={q}$', line, m1_text, fontsize='medium', ha='right', xytext=xytext, zorder=ZORDER['qline'])





def add_contours(ax, m1_range, m2_range):

    prior_line = dict(
        contour_condition=pe_space,
        plot_kwargs=dict(colors=PRI_COL, linestyles="-", linewidths=2, zorder=ZORDER['prior']),
        contourf_kwargs = dict(hatches=['\\\\'], colors='none', zorder=ZORDER['prior'])
    )
    filter_line = dict(
        contour_condition=filter_space,
        plot_kwargs=dict(colors=FILT_COL, linestyles="-", linewidths=2, zorder=ZORDER['filter']),
        contourf_kwargs = dict(hatches=['//'], colors='none', zorder=ZORDER['filter'])
    )

    # contour lines
    for idx, condition in enumerate([prior_line, filter_line]):
        m1_line, m2_line, m1m2_z = get_m1m2_grid(
            m1_range, m2_range, condition["contour_condition"])

        ax.contour(m1_line, m2_line, m1m2_z, [0.5, 1], **condition["plot_kwargs"])
        cs = ax.contourf(m1_line, m2_line, m1m2_z, [0.5, 1], **condition["contourf_kwargs"])
        cmap = cs.cmap.copy()
        cmap.set_under("#00000000")


        for i, collection in enumerate(cs.collections):
            collection.set_edgecolor(condition["plot_kwargs"]['colors'])
            # Doing this also colors in the box around each level
            # We can remove the colored line around the levels by setting the linewidth to 0
        for collection in cs.collections:
            collection.set_linewidth(0.)



def adjust_axes(fig, ax):
    # removing the default axis on all sides:
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # defining custom minor tick locations:
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
    ax.yaxis.set_minor_formatter(plt.FormatStrFormatter('%d'))
    ax.yaxis.set_major_locator(plt.FixedLocator([]))
    ax.yaxis.set_minor_locator(plt.FixedLocator([5, 25, 150, 400]))
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%d'))
    ax.xaxis.set_minor_formatter(plt.FormatStrFormatter('%d'))
    ax.xaxis.set_minor_locator(plt.FixedLocator([1,3, 5, 10, 25, 45, 100, 400]))
    ax.tick_params(axis='both',reset=False,which='both',length=8,width=2)

    # Add arrowheads
    ax.plot(1, 1, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize= 15)
    ax.plot(1, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize = 15)


def filter_space(m1: float, m2: float, mc: float, q: float, M: float) -> int:
    """
    Component Mass 1 [\msun] & 31.54 & 491.68\\
    Component Mass 2 [\msun] & 1.32 & 121.01\\
    Total Mass [\msun] & 56.93 & 496.72\\
    Chirp Mass [\msun] & 8.00 & 174.56\\
    Mass Ratio & 0.01 & 0.98\\
    """
    if (
            31.54 <= m1 <= 491.68
            and 1.32 <= m2 <= 121.01
            and 0.1 <= q <= 0.98
            and 8.0 <= mc <= 174.56
            and 56.93 <= M <= 496.72
    ):
        return 1
    else:
        return 0


def pe_space(m1: float, m2: float, mc: float, q: float, M: float) -> int:
    """
    $\mathcal{M}/\msun$           & Uniform & 7--180  \\
    $q$                           & Uniform & 0.1--1  \\
    $M/\msun$                     & Constraint & 50--500  \\
    # this sets m1(25.4, 492.3) and m2(1.1, 204.6)
    """
    if (
            # 25.4 <= m1 <= 492.3
            # and 1.1 <= m2 <= 204.6 and
            0.1 <= q <= 1
            and 7.0 <= mc <= 180
            and 50.0 <= M <= 500.0
    ):
        return 1
    else:
        return 0



def get_event_status(catalogue_df):
    data = []
    for rowid, event in catalogue_df.iterrows():
        m1 = event.mass_1_source
        m2 = event.mass_2_source
        mc = conversion.component_masses_to_chirp_mass(m1, m2)
        M = conversion.component_masses_to_total_mass(m1, m2)
        q = conversion.component_masses_to_mass_ratio(m1, m2)
        data.append(
            {
                "event": event.commonName,
                "catalog": event["catalog.shortName"],
                "in_prior": pe_space(m1, m2, mc, q, M) == 1,
                "in_filter": filter_space(m1, m2, mc, q, M) == 1,
                "m1_source": m1,
                "m2_source": m2,
                "M": M,
            }
        )
    return pd.DataFrame(data)


def plot_template_bank():
    m1_range = [1, 600]
    m2_range = [1, 600]

    set_matplotlib_style_settings(major=15, minor=8, linewidth=1.5, grid=False, mirror=False)
    rcParams["xtick.direction"] = "out"
    rcParams["ytick.direction"] = "out"
    rcParams['hatch.linewidth'] = 2.5

    fig, ax_m1m2 = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))  # 3, 2

    axis_label_kwargs = dict(fontsize="x-large", labelpad=8)

    # set labels
    ax_m1m2.set_xlabel(r"Mass 1 $[M_{\odot}]$", **axis_label_kwargs)
    ax_m1m2.set_ylabel(r"Mass 2 $[M_{\odot}]$", **axis_label_kwargs)

    # set scales
    ax_m1m2.set_yscale("log")
    ax_m1m2.set_xscale("log")

    # set scale limits
    ax_m1m2.set_xlim(m1_range[0], m1_range[1])
    ax_m1m2.set_ylim(m2_range[0], m2_range[1])



    add_shaded_regions(ax_m1m2)
    add_q_lines(ax_m1m2)
    add_contours(ax_m1m2, m1_range, m2_range)
    adjust_axes(fig, ax_m1m2)
    add_legend(ax_m1m2)

    plt.tight_layout()
    fname = "images/template_bank.png"
    plt.savefig(fname)


def add_legend(ax):
    patch1 = mpatches.Patch(facecolor='none', label='Prior', edgecolor=PRI_COL, hatch="\\\\")
    patch2 = mpatches.Patch(facecolor='none', label='Search\nSpace', edgecolor=FILT_COL, hatch="//")

    ax.legend(
        handles=[patch1, patch2],
        fontsize="large",
        markerscale=3,
        bbox_to_anchor=(1, 1),
        loc="upper left",
        frameon=False,
    )


def save_accepted_events():
    catalogs_df = pd.read_csv(CATALOG, index_col=0)
    catalogs_to_keep = ["GWTC-1-confident", "IAS", "PyCBC"]
    catalogs_df = catalogs_df[catalogs_df["catalog.shortName"].isin(catalogs_to_keep)]
    event_status = get_event_status(catalogs_df)
    event_status.to_csv("data/accepted_events.csv")


def main():
    print("Plotting Template Bank")
    save_accepted_events()
    plot_template_bank()


if __name__ == "__main__":
    main()
