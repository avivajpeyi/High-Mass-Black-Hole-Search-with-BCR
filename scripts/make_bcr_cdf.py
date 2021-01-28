from bcr_pipeline.post_processing.bcr_plotting.main_analysis_plots import \
    pack_plotting_data
from bcr_pipeline.post_processing.bcr_plotting.make_ranking_stat_probability_plot import (
    _add_rank_pdf, add_foreground_events_to_plot)
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D

rcParams["font.size"] = 30
rcParams["font.family"] = "serif"
rcParams["font.sans-serif"] = ["Computer Modern Sans"]
rcParams["text.usetex"] = True
rcParams['axes.labelsize'] = 30
rcParams['xtick.labelsize'] = 25
rcParams['ytick.labelsize'] = 25
rcParams['axes.titlesize'] = 30
rcParams['axes.labelpad'] = 10

BANK = "../data/template_bank.csv"
INJECTION = "../data/chunk21_res/injection_res.csv"
BACKGROUND = "../data/chunk21_res/background_res.csv"
FOREGROUND = "../data/chunk21_res/foreground_res.csv"
CATALOG = "../data/catalog.csv"


def plot():
    plot_data = pack_plotting_data(
        foreground_csv=FOREGROUND,
        background_csv=BACKGROUND,
        injection_csv=INJECTION,
        rank='lnBCR',
        alpha=1.0e-6,
        beta=1.0e-4,
    )
    xrange = dict(min=-15, max=30)
    fig, ax_cdf = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))
    cdf_data = _add_rank_pdf(plot_data, xrange, ax_cdf, cdf=True)
    add_foreground_events_to_plot(ax_cdf, plot_data['foreground']['df'],
                                  x_vals=cdf_data['bins'],
                                  y_vals=cdf_data['background_counts'],
                                  make_annotation=False,
                                  plot_x=False)
    ax_cdf.set_ylim(0, 1)
    ax_cdf.set_ylabel('1-CDF', fontsize="x-large")
    ax_cdf.set_xlabel(r'$\rho_{\mathrm{BCR}}$', fontsize="x-large")
    labels = ["Background Triggers", "Simulated Triggers", "GW170814", "GW170817A"]
    colors = ["#d8d8d8", "#daf0f8", "#0173b2", "#e9b457"]
    custom_lines = [Line2D([0], [0], color=c, lw=4) for c in colors]
    l = ax_cdf.legend(custom_lines, labels, fontsize="large",
                      bbox_to_anchor=(1, 1), loc="upper left", frameon=False)
    fname = '../images/bcr_cdf.png'
    fig.savefig(fname, bbox_extra_artists=[l], bbox_inches='tight')
    print("Saved fig")


def main():
    plot()


if __name__ == "__main__":
    main()
