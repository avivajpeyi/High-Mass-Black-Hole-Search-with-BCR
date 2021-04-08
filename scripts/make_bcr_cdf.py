import matplotlib.font_manager
from bcr_pipeline.post_processing.bcr_plotting.main_analysis_plots import \
    pack_plotting_data
from bcr_pipeline.post_processing.bcr_plotting.make_ranking_stat_probability_plot import (
    _add_rank_pdf)
from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.ticker import (FormatStrFormatter)

# matplotlib.font_manager.findfont("font.sans-serif", rebuild_if_missing=False)
all_fonts = matplotlib.font_manager.findSystemFonts()
print(f"Avail fonts: {all_fonts}")

font_path = "/Users/avaj0001/Library/Fonts/ScopeOn-Regular.ttf"
# prop = matplotlib.font_manager.FontProperties(fname=font_path)


rc('text.latex', preamble=r'\usepackage{cmbright}')
rcParams["font.size"] = 30
rcParams["font.family"] = "sans-serif"
# rcParams["font.sans-serif"] = ["/Users/avaj0001/Library/Fonts/ScopeOn-Regular.ttf"]
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
INJECTION_REW = "../data/chunk21_res/injection_res.csv"
BACKGROUND_REW = "../data/chunk21_res/background_res.csv"
FOREGROUND_REW = "../data/chunk21_res/foreground_res.csv"
INJECTION_ORIG = "../data/chunk21_orig/injection.csv"
BACKGROUND_ORIG = "../data/chunk21_orig/background.csv"
FOREGROUND_ORIG = "../data/chunk21_orig/foreground.csv"
INJECTION="INJECTION"
BACKGROUND="BACKGROUND"
FOREGROUND="FOREGROUND"

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

CATALOG = "../data/catalog.csv"


def plot(data_type='orig', add_legend=False):
    plot_data = pack_plotting_data(
        foreground_csv=DATA[data_type][FOREGROUND],
        background_csv=DATA[data_type][BACKGROUND],
        injection_csv=DATA[data_type][INJECTION],
        rank='lnBCR',
        alpha=1.0e-6,
        beta=1.0e-4,
    )
    xrange = dict(min=-15, max=30)
    fig, ax_cdf = plt.subplots(nrows=1, ncols=1, figsize=(7, 5))
    cdf_data = _add_rank_pdf(plot_data, xrange, ax_cdf, cdf=True)
    ax_cdf.set_ylim(0, 1)
    ax_cdf.set_ylabel('Survival Probability', fontsize="x-large")
    ax_cdf.set_xlabel(r'ln $\rho_{\mathrm{BCR}}$', fontsize="x-large")

    for idx, x_in_q in plot_data['foreground']['df'].iterrows():
        c = 'orange'
        xval = x_in_q["data"]
        event_txt = x_in_q["trigger_label"].split(":")[1]
        ax_cdf.axvline(x=xval, color=c)
        ax_cdf.annotate(
            event_txt, xy=(xval, 0.95), ha='left', va='top', rotation=-90,
            color="#ff8c00", fontweight="extra bold")

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
    bbox_extra_artists = []
    if add_legend:
        lg_kwargs = dict(fontsize="small", loc="lower right",
                         facecolor='white', framealpha=0.2, handlelength=0.75,
                         handletextpad=0.3, labelspacing=0.2, markerscale=2)
        
        l = ax_cdf.legend(
            [Line2D([0], [0], color="tab:gray", linewidth=4),
             Line2D([0], [0], color="skyblue", linewidth=4),
             Line2D([0], [0], color="tab:orange", linewidth=4), ],
            ["Background", "Simulated", "Foreground"],
            **lg_kwargs
        )
        frame = l.get_frame()
        frame.set_linewidth(0)
        bbox_extra_artists.append(l)

    fname = f'../images/{data_type}_bcr_cdf_smaller_legend.png'

    ax_cdf.yaxis.set_major_formatter(FormatStrFormatter('% 1.1f'))
    fig.savefig(fname, bbox_extra_artists=bbox_extra_artists, bbox_inches='tight', transparent=False)
    print(f"current font family: {plt.rcParams['font.family']}")
    print(f"Avail fonts: {plt.rcParams['font.sans-serif']}")
    print("Saved fig")


def main():
    plot('orig')
    plot('reweighted')


if __name__ == "__main__":
    main()
