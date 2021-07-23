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

def tsplot(df, colname1, colname2, xlabel = "x", ylabel = "y"):
    res_mean = df.resample("7D").mean()
    # res_mean.index = res_mean.index.map(
    #     lambda x: x.replace(day = 15)
    # )
    # slope, intercept, rvalue, pvalue, stderr = stats.linregress(df.dropna()["$O_3$"], df.dropna()["$GPP_{EC(NT)}$"])
    err_band = df.resample("7D").std()
    # err_band.index = err_band.index.map(
    #     lambda x: x.replace(day = 15)
    # )
    # df = df[df["$Season$"] == 2]
    fig, ax = plt.subplots()

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
    ax.plot(res_mean.index, res_mean[colname1], label = colname1, color = "darkorange")
    ax.plot(res_mean.index, res_mean[colname2], label = colname2, color = "royalblue")
    ax.fill_between(res_mean.index, res_mean[colname1] - err_band[colname1], res_mean[colname1] + err_band[colname1], color = "orange", alpha = 0.5)
    ax.fill_between(res_mean.index, res_mean[colname2] - err_band[colname2], res_mean[colname2] + err_band[colname2], color = "cornflowerblue", alpha = 0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
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
    ax.legend(by_label.values(), by_label.keys(), loc = "upper center", framealpha = 0.1, frameon = True , bbox_to_anchor=(0.5, 1.1), ncol = 4)
    ax.tick_params(direction = "in")
    ax.tick_params(axis='x', labelrotation=45)
    return fig