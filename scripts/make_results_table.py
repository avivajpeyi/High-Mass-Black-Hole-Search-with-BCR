"""
Example table:
\begin{table*}
\centering
\caption{}
\label{tab:results}
\def\arraystretch{1.5}
\setlength{\tabcolsep}{0.5em}
\begin{NiceTabular}{@{}ll!{\quad}|c|!{\quad}cc!{\quad}c!{\quad}c!{\quad}ccc!{\quad}|c@{}}
\CodeBefore
    \rowcolor{white}{1-3}
    \rowcolors{2}{white}{gray!5}
\Body
Col1 & Col1 & AA                & b.1  & b.2                 & CC   & DD   & e.1              & e.2   & e.3   & Col4       \\
\midrule
dat1 & 111  & 0.00              & 1.00            & 1.00     &      & 1.00 &                  & 1.00  &       & 111111.00  \\
dat2 & 222  & 0.00              &                 & 1.00     & 1.00 & 0.50 &                  & 1.00  & 1.00  & 222222.00  \\
dat3 & 333  & 0.00              &                 &          &      &      &                  &       &       & 333333.00  \\
dat4 & 444  & 0.00              &                 &          &      &      &                  &       &       & 444444.00  \\
% \bottomrule
\end{NiceTabular}
\end{table*}

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RES = "data/results.csv"

MAIN_TABLE_CAPTION = """
$\pastrobcr$ table for gravitational wave events and candidates in our search space with $\pastrobcr>0.2$.   
Displayed for comparison are significances of events taken from: 
GstLAL \pastroGwtcGstlal~\cite{GWTC1}, 
PyCBC \pastroGwtcPycbc~\cite{GWTC1}, 
IAS \pastroIas~\cite{IAS1, IAS2},  
\pastroPrat~\cite{bayesian_odds}, 
PyCBC `single-search' \pastroSing~\cite{pycbc_single_det}, 
PyCBC OGC-2 \pastroOgcTwo~\cite{pycbc_ogc_2} and
PyCBC OGC-3 \pastroOgcThree~\cite{pycbc_ogc_2}.
The $\\tc$ column contains the `GPS' coalescence-times of the gravitational wave events. 
The catalog column reports the first catalog in which the event has been reported (the catalogs labelled IAS-1 and IAS-2 correspond to the candidates published in \citet{IAS1} and \citet{IAS2}). 
"""

TUNED_CAPTION = r"""
Table of \pastrobcr using ``tuned'' prior odds and  \pastrobcr using uninformed prior odds of 
$\hat{\pi}^S=1$ and $\hat{\pi}^G=1$ (represented by \untunedpastrobcr).  
Details of other columns provided in Table~\ref{tab:results}.
"""

MAIN_COL_HEADERS = {
    'Event': "Event",
    'Catalogue': "Catalog",
    'pastro_bcr': "\ pastrobcr",
    'pycbc_gwtc1_pastro': "\ pastroGwtcPycbc",
    'gstlal_gwtc1_pastro': "\ pastroGwtcGstlal",
    'ias_pastro': "\ pastroIas",
    'pratten_pastro': "\ pastroPrat",
    'pycbc_single': "\ pastroSing",
    'pastro_2OGC': "\ pastroOgcTwo",
    'pastro_3OGC': "\ pastroOgcThree",
    'trigger_time': "\ tc",
}

MAIN_TOP = r"""
\def\arraystretch{1.5} 
\setlength{\tabcolsep}{0.5em}
\begin{NiceTabular}{@{}ll!{\quad}|c|cc!{\quad}c!{\quad}c!{\quad}ccc!{\quad}|c@{}}
\CodeBefore
\rowcolors{2}{white}{gray!10}
\Body
"""


def load_data():
    df = pd.read_csv(RES, na_values='na')
    df = df.replace(" IMBHc", "GWTC-1")
    df = df.replace("PyCBC Trigger", "-")
    df = df.replace("Trigger", "-")
    return df


def create_main_table(df, fname):
    df = df[df['pastro_bcr'] > 0.2]

    latex_code = df.to_latex(
        columns=list(MAIN_COL_HEADERS.keys()),
        header=list(MAIN_COL_HEADERS.values()),
        index=False,
        na_rep=" ",
        float_format='%.2f',
        caption=MAIN_TABLE_CAPTION.strip(),
        label="tab:results",
        escape=True
    )

    latex_code = latex_code.replace("{table}", "{table*}")
    latex_code = latex_code.replace("\\midrule", "\hline")
    latex_code = latex_code.replace("\\bottomrule", "")
    latex_code = latex_code.replace("\\toprule", "")
    latex_code = latex_code.replace('textbackslash  ', '')
    latex_code = latex_code.replace(
        r"\begin{tabular}{llrrrrrrrrr}",
        MAIN_TOP
    )

    latex_code = latex_code.replace(
        "\\end{tabular}",
        "\\end{NiceTabular}"
    )
    with open(fname, "w") as f:
        f.write(latex_code)
    print(latex_code)
    print('\n\n')
    print(f"Completed result {fname} generation")


def generate_tuned_vs_untuned_bcr_pastro_comparison(
        df,
        fname="tuning_results_table.tex"
):
    df = df[df['pastro_bcr'] > 0.2]
    long_caption = TUNED_CAPTION.strip()
    latex_code = df.to_latex(
        columns=["Event", "Catalogue", "pastro_bcr", "pastro_bcr_0", "trigger_time"],
        header=["Event", "Catalog", "\ tunedpastrobcr", "\ untunedpastrobcr", "\ tc"],
        index=False,
        column_format="ll|c c| c",
        na_rep="-",
        float_format='%.2f',
        caption=long_caption,
        label="tab:tuningresults",
        escape=True
    )
    latex_code = latex_code.replace('textbackslash  ', '')
    latex_code = latex_code.replace("\$", "$")
    latex_code = latex_code.replace("\{", "{")
    latex_code = latex_code.replace("\}", "}")
    latex_code = latex_code.replace("\\midrule", "\hline")
    latex_code = latex_code.replace("\\bottomrule", "")
    latex_code = latex_code.replace("\\toprule", "")
    latex_code = latex_code.replace(" IMBHc", "GWTC-1")
    latex_code = latex_code.replace("PyCBC Trigger", "-")
    latex_code = latex_code.replace("Trigger", "-")
    latex_code = latex_code.replace(
        "\\begin{tabular}",
        "\\def\\arraystretch{1.5} \n \setlength{\\tabcolsep}{0.5em}\n\\begin{tabular}"
    )
    with open(fname, "w") as f:
        f.write(latex_code)
    print(latex_code)
    print('\n')
    print(f"Completed result {fname} generation")


def make_summary(df):
    df = df.copy()
    df = df.replace("IAS-2", "IAS-1")
    df["gwtc1_pastro"] = df[["pycbc_gwtc1_pastro", "gstlal_gwtc1_pastro"]].max(axis=1)
    cats = ["IAS-1", "GWTC-1"]
    pastros = ['ias_pastro', "gwtc1_pastro"]
    for c, p in zip(cats, pastros):
        d = df[df['Catalogue'] == c]
        plot_significance_comparision(d, fname=f"images/{c}-sig.png", bcr_key="pastro_bcr", ext_key=p)
        hifav = ", ".join(list(d[d['pastro_bcr'] > 0.8].Event))
        fav = ", ".join(list(d[d['pastro_bcr'] > 0.8].Event))
        dis = ", ".join(list(d[d['pastro_bcr'] < 0.5].Event))
        print(f"FAVOURED {c} {fav}")
        print(f"DISFAVOURED {c} {dis}")


def plot_significance_comparision(data, fname, bcr_key, ext_key):
    plt.rcParams["font.size"] = 30
    plt.rcParams["font.family"] = 'sans-serif'
    plt.rcParams["font.sans-serif"] = ["Computer Modern Sans"]
    plt.rcParams["text.usetex"] = False
    plt.rcParams['axes.labelsize'] = 30
    plt.rcParams['axes.titlesize'] = 30
    plt.rcParams['axes.labelpad'] = 25

    data = data.copy()

    data['BCR Ps'] = data[bcr_key]
    data['P-astro'] = data[ext_key]
    data = data.drop_duplicates('Event', keep='last')
    data['diff'] = -np.abs(data['BCR Ps'] - data['P-astro'])
    data = data.sort_values(by=["diff"])
    data = data[[
        'Event',
        'P-astro',
        'BCR Ps'
    ]]
    data.index = data['Event']
    ax = data.plot.barh(
        sort_columns=False,
        figsize=(10, 1 * len(data)),
        # figsize=(12, 8),
        alpha=0.5,
        color=["tab:blue", "tab:orange"]
    )
    ax.set_xlabel('Significance', fontsize='x-large')
    ax.set_ylabel('')
    ax.grid()
    ax.set_xlim(0, 1)
    ax.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc=3,
              ncol=2, mode="expand", borderaxespad=0, frameon=False, fontsize='medium')
    plt.tight_layout()
    plt.savefig(fname, transparent=True)


def main():
    data = load_data()
    create_main_table(data, "data/results_table.tex")
    generate_tuned_vs_untuned_bcr_pastro_comparison(data, "data/tuning_results_table.tex")
    make_summary(data)


if __name__ == '__main__':
    main()
