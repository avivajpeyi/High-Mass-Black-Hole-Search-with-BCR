"""
Module to plot "template_bank.png"
"""
import numpy as np
import pandas as pd
from bilby.gw import conversion
from matplotlib import pyplot as plt
from settings import set_matplotlib_style_settings
from tqdm import tqdm



BANK = "data/template_bank.csv"
INJECTION = "data/chunk14/injection_triggers.csv"
BACKGROUND = "data/chunk14/background_triggers.csv"
FOREGROUND = "data/chunk14/foreground_triggers.csv"
CATALOG = "data/catalog.csv"


def get_m1m2_grid(m1_range, m2_range, filtering_criteria):
    """Return a meshgrid of m1, m2, z points based on filtering criteria.

    The returned meshgrid can be used to create a contour plot based on the filtering
    criteria

    :param m1_range:
    :param m2_range:
    :param filtering_criteria:
    :return:
    """
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
        26 <= m1 <= 500
        and 1.1 <= m2 <= 115
        and 0.01 <= q <= 0.99
        and 7 <= mc <= 166
        and 47 <= M <= 500
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
                "in_prior": contour_condition(m1, m2, mc, q, M) == 1,
                "m1_source": m1,
                "m2_source": m2,
                "M": M,
            }
        )
    return pd.DataFrame(data)


def plot_template_bank():
    template_bank = pd.read_csv(BANK, index_col=0)
    foreground = pd.read_csv(FOREGROUND, index_col=False)
    background = pd.read_csv(BACKGROUND, index_col=False)
    injection = pd.read_csv(INJECTION, index_col=False)

    scatter_points = [
        # TEMPLATE BANK
        dict(
            data=template_bank,
            plot_kwargs=dict(
                color="pink", s=0.2, marker=".", alpha=0.2, label="Template Bank"
            ),
        ),
        dict(
            data=background,
            plot_kwargs=dict(
                color="gray", s=20, marker=".", alpha=0.1, label="Background Triggers"
            ),
        ),
        dict(
            data=injection,
            plot_kwargs=dict(
                color="skyblue", s=30, marker="o", alpha=0.1, label="Simulated Triggers"
            ),
        ),
        dict(
            data=foreground,
            plot_kwargs=dict(
                color="orange", s=40, marker="s", alpha=1, label="Candidate Triggers"
            ),
        ),
    ]

    prior_line = dict(
        contour_condition=contour_condition,
        plot_kwargs=dict(colors="k", linestyles="--", linewidths=2.0, label="Prior"),
    )

    m1_range = [1, 500]
    m2_range = [1, 200]

    set_matplotlib_style_settings(major=15, minor=8, linewidth=1.5, grid=True)
    fig, ax_m1m2 = plt.subplots(nrows=1, ncols=1, figsize=(13, 6))  # 3, 2

    axis_label_kwargs = dict(fontsize="x-large", labelpad=8)

    # set labels
    ax_m1m2.set_xlabel("Mass 1", **axis_label_kwargs)
    ax_m1m2.set_ylabel("Mass 2", **axis_label_kwargs)

    tick_params = dict(pad=8)
    ax_m1m2.tick_params(axis='both', **tick_params)

    # set scales
    ax_m1m2.set_yscale("log")
    ax_m1m2.set_xscale("log")

    # set scale limits
    ax_m1m2.set_xlim(m1_range[0], m1_range[1] + 100)
    ax_m1m2.set_ylim(m2_range[0], m2_range[1])

    # contour line
    m1_line, m2_line, m1m2_z = get_m1m2_grid(
        m1_range, m2_range, prior_line["contour_condition"]
    )

    ax_m1m2.contour(m1_line, m2_line, m1m2_z, [0], **prior_line["plot_kwargs"])

    for scatter_data in scatter_points:
        ax_m1m2.scatter(
            scatter_data["data"].mass_1,
            scatter_data["data"].mass_2,
            **scatter_data["plot_kwargs"]
        )

    bank_patch = ax_m1m2.scatter(
        [], [], label="Template Bank", marker=".", color="pink"
    )
    (prior_patch,) = ax_m1m2.plot([], [], label="Prior", linestyle="--", color="k")
    fg_patch = ax_m1m2.scatter(
        [], [], label="Candidate Triggers", marker="s", color="orange"
    )
    bg_patch = ax_m1m2.scatter(
        [], [], label="Background Triggers", marker=".", color="gray"
    )
    inj_patch = ax_m1m2.scatter(
        [], [], label="Simulated Triggers", marker=".", color="skyblue"
    )
    handles = [bank_patch, prior_patch, fg_patch, bg_patch, inj_patch]
    ax_m1m2.legend(
        handles=handles,
        fontsize="large",
        markerscale=3,
        bbox_to_anchor=(1, 1),
        loc="upper left",
        frameon=False,
    )

    plt.tight_layout()
    fname = "images/template_bank.png"
    plt.savefig(fname)


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
