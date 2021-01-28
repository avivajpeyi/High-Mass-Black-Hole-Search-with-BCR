from bcr_pipeline.post_processing.bcr_plotting.main_analysis_plots import \
    pack_plotting_data
from bcr_pipeline.post_processing.bcr_plotting.make_ranking_stat_probability_plot import (
    _add_rank_pdf)
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D


rcParams["font.size"] = 30
rcParams["font.family"] = "serif"
rcParams["font.sans-serif"] = ["Computer Modern Sans"]
rcParams["text.usetex"] = True
rcParams['axes.labelsize'] = 30
rcParams['axes.titlesize'] = 30
rcParams['axes.labelpad'] = 10
rcParams['axes.linewidth'] = 2.5
rcParams['axes.edgecolor'] = 'black'
rcParams['xtick.labelsize'] = 25
rcParams['xtick.major.size'] = 10.0
rcParams['xtick.minor.size'] = 5.0
rcParams['ytick.labelsize'] = 25
rcParams['ytick.major.size'] = 10.0
rcParams['ytick.minor.size'] = 5.0
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['xtick.major.width'] = 3
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams['ytick.major.width'] = 2.5
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True



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
    ax_cdf.set_ylim(0, 1)
    ax_cdf.set_ylabel('1-CDF', fontsize="x-large")
    ax_cdf.set_xlabel(r'$\rho_{\mathrm{BCR}}$', fontsize="x-large")


    for idx, x_in_q in plot_data['foreground']['df'].iterrows():
        c = 'orange'
        xval = x_in_q["data"]
        event_txt = x_in_q["trigger_label"].split(":")[1]
        ax_cdf.axvline(x=xval, color=c)
        ax_cdf.annotate(
            event_txt, xy=(xval, 0.95), ha='left', va='top', rotation=-90,
            color="#ff8c00", fontweight="extra bold", fontfamily='sans-serif')

    # add_foreground_events_to_plot(ax_cdf, plot_data['foreground']['df'],
    #                               x_vals=cdf_data['bins'],
    #                               y_vals=cdf_data['background_counts'],
    #                               make_annotation=False,
    #                               plot_x=False)
    # lg_kwargs = dict(fontsize="large", bbox_to_anchor=(1, 1), loc="upper left",
    #                  frameon=False)
    # labels = ["Background Triggers", "Simulated Triggers", "GW170814", "GW170817A"]
    # colors = ["#d8d8d8", "#daf0f8", "#0173b2", "#e9b457"]
    # custom_lines = [Line2D([0], [0], color=c, lw=4) for c in colors]
    # l = ax_cdf.legend(custom_lines, labels, **lg_kwargs)

    lg_kwargs = dict(fontsize="small", loc="lower right",
                     facecolor='white', framealpha=0.2, handlelength=0.75,  handletextpad=0.3, labelspacing=0.2)

    l = ax_cdf.legend(
        [Line2D([0], [0], color="#d8d8d8", lw=2),
         Line2D([0], [0], color="#daf0f8", lw=2)],
        ["Background", "Simulated"],
        **lg_kwargs
    )
    frame = l.get_frame()
    frame.set_linewidth(0)

    fname = '../images/bcr_cdf_smaller_legend.png'
    fig.savefig(fname, bbox_extra_artists=[l], bbox_inches='tight')
    print("Saved fig")


def main():
    plot()


if __name__ == "__main__":
    main()
