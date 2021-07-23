import itertools
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14})

def plot_months(df):
    colnames = df.columns.tolist()
    df['Day'] = df.index.map(lambda x: x.strftime("%d"))
    df['Month'] = df.index.map(lambda x: x.strftime("%m"))
    df['Year'] = df.index.map(lambda x: x.strftime("%Y"))

    # df_diurnal = df.reset_index()
    df_diurnal = df.pivot_table(colnames, ['Year', 'Month', 'Day'], aggfunc='mean').reset_index()
    # months = list(df_diurnal["Month"].unique())
    # months.sort(key=float)
    months = [12] + list(np.arange(11) + 1)
    months = [str(m).zfill(2) for m in months]


    fig, axs = plt.subplots(figsize=(16, 12), 
                            nrows = 4, ncols = 3,
                            sharex = True,
                            sharey = True
                           )

    for mt, ax in zip(months, axs.flatten()):
        ax.tick_params(which = "both", direction = "in")
        mt_label = datetime.strptime(mt, "%m").strftime("%B")
        dft = df_diurnal.query("Month == @mt")
        # years = dft["Year"].unique()
        dft = dft.drop("Month", axis = 1)
        dft = dft.set_index("Day")
        dft = dft.sort_index()
        # print(dft)
        # # method 2: plot lines and legend manually
        years = [2019, 2020, 2021]
        # colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        # colors = ["darkred", "navy", "indianred", "royalblue", "mistyrose", "lightsteelblue"]
        colors = ["tomato", "mediumpurple", "red", "blue", "darkred", "navy"]
        legends = [f"{cn}({yr})" for (yr, cn) in itertools.product(years, colnames)]
        markers = ["-", "--", ":"]
        for count, ((yr, cn), c) in enumerate(zip(itertools.product(years, colnames), colors)):
            if dft[dft["Year"] == str(yr)].empty: continue
            dfp = dft.loc[dft["Year"] == str(yr), cn]
            dfp = dfp.sort_index()
            # ax.plot(dfp.index, dfp, color = c)
            dfp.plot(color = c, ax = ax, legend = None, title=mt_label, style = markers[count//2], lw = 3)
            # lgds.append(str(yr))
        # ax.legend(lgds)
        # legend_labels = [item.get_text() for item in ax.get_xticklabels()]
        ax.set_ylabel("$\mu g / m^{3}$")
        ax.set_xlabel("Day", fontsize = 14)

    # =========================================================================================================
    # extract common legends
    lines = []
    labels = []

    ax_colors = []
    for ax in fig.axes:
        axLine, axLabel = ax.get_legend_handles_labels()
        for line2D in axLine:
            if line2D.get_color() in ax_colors:
                continue
            else:
                ax_colors.append(line2D.get_color())
                line2D.set_label(
                    dict(zip(colors, legends))[line2D.get_color()]
                )
                lines.append(line2D)
    # lines = sorted(lines, key=lambda x: int(x.get_label()), reverse=False)
    # plt.locator_params(axis = 'x', nbins = 8)
    axs.flatten()[-2].legend(handles = lines, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=len(lines))
    # =========================================================================================================
    return fig

df = pd.concat(dfs)
df = df.rename(
    columns = {
        "truth": "$CNEMC$",
        "pred": "$DF21$"
    }
)
# fig = plot_months(df)

# plt.savefig(f"diurnal_new.png", bbox_inches = "tight", dpi = 300)

# plt.close(fig)