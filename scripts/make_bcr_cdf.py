"""
Script to plot CDFs (reweighted and original)
"""
import logging.config

from bcr_pipeline.post_processing.bcr_plotting.main_analysis_plots import (
    pack_plotting_data,
)
from bcr_pipeline.post_processing.bcr_plotting.make_ranking_stat_probability_plot import (
    _add_rank_pdf,
)
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter
from settings import set_matplotlib_style_settings

logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})

set_matplotlib_style_settings()

INJECTION_REW = "data/chunk21_res/injection_res.csv"
BACKGROUND_REW = "data/chunk21_res/background_res.csv"
FOREGROUND_REW = "data/chunk21_res/foreground_res.csv"
INJECTION_ORIG = "data/chunk21_orig/injection.csv"
BACKGROUND_ORIG = "data/chunk21_orig/background.csv"
FOREGROUND_ORIG = "data/chunk21_orig/foreground.csv"
INJECTION = "INJECTION"
BACKGROUND = "BACKGROUND"
FOREGROUND = "FOREGROUND"

DATA = dict(
    orig=dict(
        INJECTION=INJECTION_ORIG,
        BACKGROUND=BACKGROUND_ORIG,
        FOREGROUND=FOREGROUND_ORIG,
    ),
    reweighted=dict(
        INJECTION=INJECTION_REW,
        BACKGROUND=BACKGROUND_REW,
        FOREGROUND=FOREGROUND_REW,
    ),
)


def plot(data_type, add_legend=False):
    plot_data = pack_plotting_data(
        foreground_csv=DATA[data_type][FOREGROUND],
        background_csv=DATA[data_type][BACKGROUND],
        injection_csv=DATA[data_type][INJECTION],
        rank="lnBCR",
        alpha=1.0e-6,
        beta=1.0e-4,
    )
    xrange = dict(min=-15, max=30)
    fig, ax_cdf = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))
    _add_rank_pdf(plot_data, xrange, ax_cdf, cdf=True)
    ax_cdf.set_ylim(0, 1)
    ax_cdf.set_ylabel("Survival Probability", fontsize="x-large")
    ax_cdf.set_xlabel(r"ln $\rho_{\mathrm{BCR}}$", fontsize="x-large")

    for idx, x_in_q in plot_data["foreground"]["df"].iterrows():
        c = "orange"
        xval = x_in_q["data"]
        event_txt = x_in_q["trigger_label"].split(":")[1]
        ax_cdf.axvline(x=xval, color=c)
        ax_cdf.annotate(
            event_txt,
            xy=(xval, 0.95),
            ha="left",
            va="top",
            rotation=-90,
            color="#ff8c00",
            fontweight="extra bold",
        )

    ax_cdf.grid(False)
    bbox_extra_artists = []
    if add_legend:
        lg_kwargs = dict(
            fontsize="small",
            loc="lower right",
            facecolor="white",
            framealpha=0.2,
            handlelength=0.75,
            handletextpad=0.3,
            labelspacing=0.2,
            markerscale=2,
        )

        l = ax_cdf.legend(
            [
                Line2D([0], [0], color="tab:gray", linewidth=4),
                Line2D([0], [0], color="skyblue", linewidth=4),
                Line2D([0], [0], color="tab:orange", linewidth=4),
            ],
            ["Background", "Simulated", "Foreground"],
            **lg_kwargs,
        )
        frame = l.get_frame()
        frame.set_linewidth(0)
        bbox_extra_artists.append(l)

    fname = f"images/{data_type}_bcr_cdf_smaller_legend.png"

    ax_cdf.yaxis.set_major_formatter(FormatStrFormatter("% 1.1f"))
    fig.savefig(
        fname,
        bbox_extra_artists=bbox_extra_artists,
        bbox_inches="tight",
        transparent=False,
    )


def main():
    print("Plotting CDFs")
    plot("orig")
    plot("reweighted")


if __name__ == "__main__":
    main()
