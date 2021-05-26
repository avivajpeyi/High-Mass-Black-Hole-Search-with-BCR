"""
Script to plot known events (not used in paper but useful for presentations)
"""
import matplotlib.font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.patches import Polygon

from settings import set_matplotlib_style_settings, logger

set_matplotlib_style_settings()

COLS = {"LVK": "tab:purple", "IAS": "tab:pink", "LVK Candidates": "tab:orange"}


def plot_masses(catalog_df):
    df = catalog_df.copy()
    df = df.replace("GWTC-1-confident", "LVK")
    df = df.replace("GWTC-2", "LVK")
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    ax.set_xlabel("$\\mathrm{Primary\\ Mass\\ M}_\\odot$")
    ax.set_ylabel("$\\mathrm{Secondary\\ Mass\\ M}_\\odot$")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_xlim(10, 400)
    ax.set_ylim(10, 400)

    pisn_poly = Polygon(
        [(0, 55), (55, 55), (55, 0), (120, 0), (120, 120), (0, 120)],
        facecolor="tab:cyan",
        alpha=0.1,
    )
    ax.add_patch(pisn_poly)
    mirror_poly = Polygon([(0, 0), (1000, 1000), (0, 1000)], facecolor="0.9")
    ax.add_patch(mirror_poly)

    different_catalogs = ["LVK Candidates", "LVK", "IAS"]
    for cat_name in different_catalogs:
        data = df[df["catalog.shortName"] == cat_name]
        if cat_name in ["IAS", "PyCBC"]:
            for i in [1, 2]:
                for err in ["upper", "lower"]:
                    data[f"mass_{i}_source_{err}"] = (
                        data[f"mass_{i}_source_{err}"] - data[f"mass_{i}_source"]
                    )
        y, x = data["mass_2_source"], data["mass_1_source"]

        pt_color = COLS[cat_name]
        if cat_name == "LVK Candidates":
            ax.scatter(x, y, color=pt_color, s=1, marker=".", alpha=0.05)
            ax.scatter([], [], color=pt_color, label=cat_name)
        else:
            ax.scatter(x, y, label=cat_name, color=pt_color)
            x_error = [abs(data["mass_1_source_lower"]), data["mass_1_source_upper"]]
            y_error = [abs(data["mass_2_source_lower"]), data["mass_2_source_upper"]]
            ax.errorbar(
                x,
                y,
                yerr=y_error,
                fmt="o",
                xerr=x_error,
                lw=2,
                capsize=4,
                capthick=4,
                color=pt_color,
                alpha=0.2,
            )
    leg_kwargs = dict(
        loc="upper left",
        frameon=True,
        ncol=2,
        handletextpad=0.1,
        columnspacing=0.5,
        labelspacing=0.2,
    )
    ax.legend(**leg_kwargs)
    handles, labels = ax.get_legend_handles_labels()

    ax.xaxis.set_major_formatter(matplotlib.ticker.LogFormatter(labelOnlyBase=False))
    ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter(labelOnlyBase=False))

    patch = Patch(color="tab:cyan", alpha=0.1, label="PISN Gap")
    handles = [patch] + handles
    plt.legend(handles=handles, markerscale=2, **leg_kwargs)
    plt.tight_layout()
    plt.savefig("images/known_events.png", transparent=True)


if __name__ == "__main__":
    catalog_df = pd.read_csv("data/catalog.csv")
    candidates = pd.read_csv("data/candidates.csv")
    candidates["mass_1_source"] = candidates["m1"]
    candidates["mass_2_source"] = candidates["m2"]
    candidates["catalog.shortName"] = "LVK Candidates"
    catalog_df = catalog_df.append(candidates)
    plot_masses(catalog_df)
