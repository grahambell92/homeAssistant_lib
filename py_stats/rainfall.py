import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# kynetonDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0001_088123_kyneton/IDCJAC0001_088123_Data12.csv')
redesdaleRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088051_1800_redesdale/IDCJAC0009_088051_1800_Data.csv')
lakeEildonRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088023_1800_lakeEildon/IDCJAC0009_088023_1800_Data.csv')
bendigoRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_081123_1800_bendigo/IDCJAC0009_081123_1800_Data.csv')
viewbankRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_086068_1800_viewbank/IDCJAC0009_086068_1800_Data.csv')
euroaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_082016_1800_euroa/IDCJAC0009_082016_1800_Data.csv')
leongathaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_085049_1800_leongatha/IDCJAC0009_085049_1800_Data.csv')
castlemaneRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088110_1800_castlemane/IDCJAC0009_088110_1800_Data.csv')


locations = ['Redesdale',
             'lakeEildon',
             'Bendigo',
             'Viewbank',
             'Euroa',
             'Leongatha',
             'Castlemane']
dataFrames = [redesdaleRawDf,
              lakeEildonRawDf,
              bendigoRawDf,
              viewbankRawDf,
              euroaRawDf,
              leongathaRawDf,
              castlemaneRawDf]


series = []
for df, location in zip(dataFrames, locations):
    index = pd.to_datetime(df[['Year', 'Month', 'Day']])
    rain = np.array(df['Rainfall amount (millimetres)'])
    series.append(pd.Series(data=rain, name=location, index=index))

rainDf = pd.concat(series, axis=1)

if False:
    groups = monthlyTotals.groupby(pd.Grouper(freq='M'))
    for label, group in groups:
        print(group)
        # print(group)
    exit(0)

if False:
    print('Last 30 days historical summary')

    # d = pd.to_datetime('2019-5-4')
    firstYear = rainDf.index[0].year + 50
    zeroDate = pd.to_datetime(str(firstYear)+'-1-1')

    histBins = np.linspace(start=-20, stop=20, num=10)
    dateOffsets = np.arange(start=0, stop=365, step=3)
    histContour = np.zeros(shape=(histBins.size, dateOffsets.size))

    medians = np.zeros(shape=(dateOffsets.size, len(dataFrames)))
    stds = np.zeros(shape=(dateOffsets.size, len(dataFrames)))

    for index, dateOffset in enumerate(dateOffsets):

        zeroYear_maxDate = zeroDate + pd.Timedelta(dateOffset, unit='d')
        # print(zeroYear_maxDate)
        rainWindowDf = rainDf.copy()
        for year in np.arange(start=firstYear, stop=2020):
            maxDate = zeroYear_maxDate.replace(year=year)
            # print(maxDate)
            minDate = maxDate - pd.Timedelta(30, unit='d')
            rainWindowDf.loc[minDate: maxDate, 'Year'] = int(year)

        rainWindow_sum = rainWindowDf.groupby(by='Year').sum()
        rainWindow_sum = rainWindow_sum.replace(to_replace=0.0, value=np.nan)
        rainWindow_median = rainWindow_sum.median()
        rainWindow_std = rainWindow_sum.std()

        medians[index, :] = rainWindow_median#['Redesdale']
        stds[index, :] = rainWindow_std#['Redesdale']
        # print(rainWindow_median)
        # rainWindow_anom = rainWindow_sum - rainWindow_median
        # plt.plot(rainWindow_sum['Redesdale'])
        # plt.show()


    # Rain fall historical moving average
    if False:
        plotYear = 2019
        plotYears = np.arange(2019, 2021)
        import os
        avgRainPath = './rollingAvgRain/'
        os.makedirs(avgRainPath, exist_ok=True)
        for plotYear in plotYears:
            print('Plotting: ', plotYear)
            nrow = medians.shape[1]
            ncol = 1;
            figScale = 2.0
            figsize = (8 * figScale, nrow * figScale)
            fig, axs = plt.subplots(nrows=nrow, ncols=ncol, figsize=figsize)

            for median, std, label, ax in zip(medians.T, stds.T, rainDf.columns, axs.reshape(-1)):
                # plt.plot(dateOffsets, median, label=label)
                # plt.errorbar(x=dateOffsets, y=median, yerr=std, marker='.', ls='None')
                dummyYear = pd.date_range(start='1/1/'+str(plotYear), end='1/1/'+str(plotYear+1), periods=len(dateOffsets))
                ax.plot(dummyYear, median, ls='-', label=label+' median')
                rainDf = rainDf.replace(to_replace=0.0, value=np.nan)

                recentRain = rainDf.rolling(window=30, min_periods=1).sum()
                # ax.plot(recentRain['Redesdale'])
                ax.plot(recentRain[label], label = label + ': {0}'.format(plotYear))

                ax.set_xlim(dummyYear[0], dummyYear[-1])
                # plt.show()
                ax.fill_between(dummyYear, median - 1.96*std, median + 1.96*std, alpha=0.3, label='95% CI')
                # break
                ax.set_ylim(top=150.0, bottom=0.0)
                ax.legend()
            plt.savefig('{0}rainfall_rollingAvg_{1}.png'.format(avgRainPath, plotYear), dpi=250)
            plt.close(fig)
        exit(0)

    exit(0)


if True:
    # print('Monthly average rainfall')
    # print(monthlyTotals.groupby('Month').mean())
    # print()
    # print('Yearly total')
    yearlyTotal = rainDf.resample('Y').sum().rolling(window=5, min_periods=1).mean()
    years = yearlyTotal.index.year
    years -= np.max(years)+1

    for column, data in yearlyTotal.iteritems():
        # plt.semilogx(np.abs(years[::-1]), data[::-1], label=column)
        # print(years)
        # print(np.array(data))
        # exit(0)
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1900-1-1')
    # plt.xlim(left=fromDate)
    plt.ylim(bottom=1.0)

    plt.legend()
    plt.show()
    exit(0)
    exit(0)

if True:
    groups = monthlyTotals.groupby('Month')
    for label, groupDf in groups:
        print(label)
        monthTrace = np.array(groupDf)
        plt.plot(monthTrace)
        plt.show()
    exit(0)


if False:
    plt.plot(np.array(monthlyTotals))
    plt.show()
    exit(0)

if False:
    ax = monthlyTotals.plot.hist(bins=20, alpha=0.1, density=1)
    plt.show()

if True:
    for column, label in zip(np.array(monthlyTotals).T, monthlyTotals.columns):
        column = column[~np.isnan(column)]
        y, binEdges = np.histogram(column, bins=15, density=1)
        bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
        plt.plot(bincenters, y, '-', label=label)
    plt.legend()
    plt.show()
