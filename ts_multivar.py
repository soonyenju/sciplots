import matplotlib.pyplot as plt

def get_endpoints(seasons, years):
    starts, ends = [], []
    for yr in years:
        # yr = 2009
        yr_season = seasons[seasons.index.year == yr]
        if yr_season.empty: continue
        # print(yr_season)
        # print("------------------")
        start = yr_season.index[0]
        end = yr_season.index[-1]
        if 12 in yr_season.index.month:
            yr_season = yr_season[yr_season.index.month != 12]
        if (yr -1 in seasons.index.year) & (12 in seasons.index.month):
            last_year = seasons[
                ((seasons.index.year == yr - 1) & (seasons.index.month == 12)) #| yr_season.index
            ]
            start = last_year.index[0]
            end = yr_season.index[-1]
        else:
            if yr_season.empty: continue
            start = yr_season.index[0]
            end = yr_season.index[-1]
        starts.append(start)
        ends.append(end)
    return (starts, ends)

def tsplot_(df, colnames, xlabel = "x", ylabel = "y", freq = "7D", season_shade = True, line_colors = ["darkorange", "royalblue"], shade_colors = ["orange", "cornflowerblue"]):
    # ------------------------------------------------------------------------------------------------------------------
    # create mean and std
    res_mean = df.resample(freq).mean()
    # res_mean.index = res_mean.index.map(
    #     lambda x: x.replace(day = 15)
    # )
    # slope, intercept, rvalue, pvalue, stderr = stats.linregress(df.dropna()["$O_3$"], df.dropna()["$GPP_{EC(NT)}$"])
    err_band = df.resample(freq).std()
    # err_band.index = err_band.index.map(
    #     lambda x: x.replace(day = 15)
    # )
    # df = df[df["$Season$"] == 2]
    fig, ax = plt.subplots()
    # ------------------------------------------------------------------------------------------------------------------
    # create season shade
    if season_shade:
        # ax.fill_betweenx(y, x1, x2)
        years = res_mean.index.year.unique()
        # winter
        summers = res_mean.loc[res_mean["$Season$"] == 1, "$Season$"]
        starts, ends = get_endpoints(summers, years)
        for start, end in zip(starts, ends):
            # print(start, end)
            # end_iloc = res_mean.index.tolist().index(end)
            # if end_iloc + 1 < len(res_mean): end =  res_mean.index[end_iloc + 1]
            start = start.replace(day = 1)
            end = end.replace(month = end.month + 1, day = 1)
            ax.axvspan(start, end, alpha=0.15, color='deepskyblue', label = "Winter")
            # ax.axvline(start, color='k', linestyle='--', alpha = 0.5)
            # ax.axvline(end, color='k', linestyle='--', alpha = 0.5)
        # summers
        summers = res_mean.loc[res_mean["$Season$"] == 3, "$Season$"]
        starts, ends = get_endpoints(summers, years)
        for start, end in zip(starts, ends):
            # print(start, end)
            # end_iloc = res_mean.index.tolist().index(end)
            # if end_iloc + 1 < len(res_mean): end =  res_mean.index[end_iloc + 1]
            start = start.replace(day = 1)
            end = end.replace(month = end.month + 1, day = 1)
            ax.axvspan(start, end, alpha=0.15, color='tomato', label = "Summer")
            # ax.axvline(start, color='k', linestyle='--', alpha = 0.5)
            # ax.axvline(end, color='k', linestyle='--', alpha = 0.5)
        # print(res_mean["2005": "2006"].index)
    # ------------------------------------------------------------------------------------------------------------------------------
    # plot and add legend
    for count, colname in enumerate(colnames):
        ax.plot(res_mean.index, res_mean[colname], label = colname, color = line_colors[count])
        # ax.plot(res_mean.index, res_mean[colname2], label = colname2, color = "royalblue")
        ax.fill_between(res_mean.index, res_mean[colname] - err_band[colname], res_mean[colname] + err_band[colname], color = shade_colors[count], alpha = 0.5)
        # ax.fill_between(res_mean.index, res_mean[colname2] - err_band[colname2], res_mean[colname2] + err_band[colname2], color = "cornflowerblue", alpha = 0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # ax.set_ylim([0, 60])
    # Python < 3.7
    """
    from collections import OrderedDict
    import matplotlib.pyplot as plt

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    """
    # Python > 3.7
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc = "upper center", framealpha = 0.1, frameon = True , bbox_to_anchor=(0.5, 1.1), ncol = len(handles))
    ax.tick_params(direction = "in")
    ax.tick_params(axis='x', labelrotation=45)
    return fig, ax

# df = pd.concat(dfs)
# df['$Season$'] = (df.index.month%12 + 3) // 3 # print(seasons)
# df = df.rename(
#     columns = {
#         "truth": "$CNEMC$",
#         "pred": "$DF21$"
#     }
# )
# fig = tsplot(df, "$CNEMC$", "$DF21$", xlabel = "", ylabel = "$\mu g / m^{3}$")
# fig.savefig("fig.png", dpi = 300, bbox_inches = "tight")

def plot_sites(df, site_list, freq = "7D", season_shade = True, line_colors = ["darkorange", "royalblue"], shade_colors = ["orange", "cornflowerblue"]):
    df = df.copy()
    df = df[site_list]
    df['$Season$'] = (df.index.month%12 + 3) // 3 # print(seasons)

    fig, ax = tsplot_(df, site_list, xlabel = "", ylabel = "$\mu g / m^{3}$", freq = freq, season_shade = season_shade, line_colors = line_colors, shade_colors = shade_colors)
    return fig, ax