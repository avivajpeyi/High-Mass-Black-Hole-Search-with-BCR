from matplotlib import rcParams


def set_matplotlib_style_settings(major=7, minor=3, linewidth=1.5, grid=False):
    rcParams["font.size"] = 30
    rcParams["font.family"] = "serif"
    rcParams["font.sans-serif"] = ["Computer Modern Sans"]
    rcParams["text.usetex"] = True
    rcParams["axes.labelsize"] = 30
    rcParams["axes.titlesize"] = 30
    rcParams["axes.labelpad"] = 10
    rcParams["axes.linewidth"] = linewidth
    rcParams["axes.edgecolor"] = "black"
    rcParams["xtick.labelsize"] = 25
    rcParams["ytick.labelsize"] = 25
    rcParams["xtick.direction"] = "in"
    rcParams["ytick.direction"] = "in"
    rcParams["xtick.major.size"] = major
    rcParams["xtick.minor.size"] = minor
    rcParams["ytick.major.size"] = major
    rcParams["ytick.minor.size"] = minor
    rcParams["xtick.minor.width"] = linewidth
    rcParams["xtick.major.width"] = linewidth
    rcParams["ytick.minor.width"] = linewidth
    rcParams["ytick.major.width"] = linewidth
    rcParams["xtick.top"] = True
    rcParams["ytick.right"] = True
    rcParams["axes.grid"] = grid
    rcParams["axes.titlepad"] = 8
