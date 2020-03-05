import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

def plotSeasonBands(minDate, maxDate, ax):
    # plot the seasons
    minYear = minDate.year
    maxYear = maxDate.year
    for year in range(minYear, maxYear + 1):
        # Bloody americans...
        summerStartDate = pd.to_datetime('12/01/' + str(year))
        summerEndDate = pd.to_datetime('02/28/' + str(year + 1))
        ax.axvspan(summerStartDate, summerEndDate, facecolor='red', ls='None', alpha=0.2)

        winterStartDate = pd.to_datetime('06/01/' + str(year))
        winterEndDate = pd.to_datetime('08/31/' + str(year))
        ax.axvspan(winterStartDate, winterEndDate, facecolor='blue', ls='None', alpha=0.2)
    # return ax

def pullBOMWeatherTrace():
    pass


def copyTowwwFolder(currentImagePath):
    # Copy to the www folder for the HomeAssistant Server
    wwwFolder = '/home/homeassistant/.homeassistant/www/' + 'rainfallFigs/'
    os.makedirs(wwwFolder, exist_ok=True)
    shutil.copy(currentImagePath, wwwFolder)
    print('Copied to HA local folder:{}'.format(wwwFolder))

# kynetonDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0001_088123_kyneton/IDCJAC0001_088123_Data12.csv')
redesdaleRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088051_1800_redesdale/IDCJAC0009_088051_1800_Data.csv')
lakeEildonRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088023_1800_lakeEildon/IDCJAC0009_088023_1800_Data.csv')
bendigoRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_081123_1800_bendigo/IDCJAC0009_081123_1800_Data.csv')
viewbankRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_086068_1800_viewbank/IDCJAC0009_086068_1800_Data.csv')
euroaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_082016_1800_euroa/IDCJAC0009_082016_1800_Data.csv')
leongathaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_085049_1800_leongatha/IDCJAC0009_085049_1800_Data.csv')
castlemaneRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088110_1800_castlemane/IDCJAC0009_088110_1800_Data.csv')
# dubboRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_065030_1800_dubbo/IDCJAC0009_065030_1800_Data.csv')

locations = ['Redesdale',
             'lakeEildon',
             'Bendigo',
             'Viewbank',
             'Euroa',
             'Leongatha',
             'Castlemaine',
             # 'Dubbo'
             ]
dataFrames = [redesdaleRawDf,
              lakeEildonRawDf,
              bendigoRawDf,
              viewbankRawDf,
              euroaRawDf,
              leongathaRawDf,
              castlemaneRawDf,
              # dubboRawDf
              ]

if False:
    locations = locations[:1]
    dataFrames = dataFrames[:1]

series = []
for df, location in zip(dataFrames, locations):
    index = pd.to_datetime(df[['Year', 'Month', 'Day']])
    rain = np.array(df['Rainfall amount (millimetres)'])
    series.append(pd.Series(data=rain, name=location, index=index))

rainDf = pd.concat(series, axis=1)


if True:

    figureFolder = './figs/'
    figSize = (6, 4)
    os.makedirs(figureFolder, exist_ok=True)
    integrationWindow = 60 # days
    rainDf_rolling = rainDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum()/integrationWindow

    # Compute the rolling sum to get interpolated rain value.
    rainDf_rolling['dayOfYear'] = rainDf_rolling.index.dayofyear
    # Compute the yearly median by comparing each day of year over the years.
    rain_median = rainDf_rolling.groupby(by='dayOfYear').median()
    rain_mean = rainDf_rolling.groupby(by='dayOfYear').mean()

    rain_std = rainDf_rolling.groupby(by='dayOfYear').std()


#33
    # compare medians
    if True:
        fig = plt.figure(figsize=figSize)
        ax = fig.add_subplot(1, 1, 1)
        integrationWindow = 50  # days
        rainDf_rolling_long = rainDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum()/integrationWindow
        rainDf_rolling_long['dayOfYear'] = rainDf_rolling_long.index.dayofyear
        rain_median_long = rainDf_rolling_long.groupby(by='dayOfYear').median()
        for column in ['Redesdale', 'Bendigo', 'Leongatha', 'Viewbank']: #rainDf.columns:
            # ax.plot(rain_median_long[column], label='{0} median'.format(column))
            smoothMedian = rain_median[column].rolling(window=30, min_periods=5).mean()
            ax.plot(smoothMedian[:-1]*30, label='{0}'.format(column))
        ax.set_ylabel('Median rainfall, 30 day cumulative (mm)')

        xticks = pd.date_range(start='1/1/2018', periods=12, freq='MS')
        ax.set_xticks(xticks.dayofyear, )
        ax.set_xticklabels(xticks.month_name(), rotation=45)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.grid()
        ax.legend()
        fig.tight_layout()
        fname = figureFolder+'04_medianRainfall.png'
        fig.savefig(fname=fname,dpi=200)
        plt.close(fig)
        copyTowwwFolder(currentImagePath=fname)
        # plt.show()
        # exit(0)

    if True:
        fig = plt.figure(figsize=figSize)
        ax = fig.add_subplot(1, 1, 1)
        ax2 = ax.twinx()
        integrationWindow = 50  # days
        for column in ['Redesdale']: #rainDf.columns:
            # ax.plot(rain_median_long[column], label='{0} median'.format(column))
            smoothMedian = rain_median[column].rolling(window=30, min_periods=5).mean()
            smoothStd = rain_std[column].rolling(window=30, min_periods=5).mean()
            ax.plot(smoothMedian[:-1]*30, color='b', label='{0} Median'.format(column))
            ax2.plot(smoothStd[:-1]*30, color='r', label='{0} Std'.format(column))

        ax.set_ylabel('Median rainfall, 30 day cumulative (mm)', color='b')
        ax2.set_ylabel('Standard Dev. rainfall, 30 day cumulative (mm)', color='r')

        xticks = pd.date_range(start='1/1/2018', periods=12, freq='MS')
        ax.set_xticks(xticks.dayofyear, )
        ax.set_xticklabels(xticks.month_name(), rotation=45)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.grid()
        # ax.legend()
        fig.tight_layout()
        fname = figureFolder+'03_Redesdale_medianStdRainfall.png'
        fig.savefig(fname=fname,dpi=200)
        plt.close(fig)
        copyTowwwFolder(currentImagePath=fname)

        # plt.show()

    # Bar plot of total rainfall per year
    if True:
        fig = plt.figure(figsize=figSize)
        ax = fig.add_subplot(1, 1, 1)
        for index, column in enumerate(rainDf.columns):
            sum = rain_median[column].sum()
            ax.bar(index, sum)
            ax.text(index, sum + 5.0, '{:0.0f}'.format(sum), color='blue', fontweight='bold', ha='center',)

        ax.set_xticks(np.arange(len(np.array(rainDf.columns))))
        ax.set_xticklabels(np.array(rainDf.columns), rotation=45)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_ylabel('Annual rainfall (mm)')
        fig.tight_layout()
        fname = figureFolder + '05_annualRainfall_bar.png'
        fig.savefig(fname=fname, dpi=200)
        plt.close(fig)
        copyTowwwFolder(currentImagePath=fname)

        # exit(0)


    # Intensity of rain
    if False:
        for column, label in zip(np.array(rainDf).T, rainDf.columns):
            column = column[~np.isnan(column)]
            bins = np.linspace(start=0.0, stop=100, num=30)
            y, binEdges = np.histogram(column, bins=bins, density=1)
            bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
            plt.semilogy(bincenters, y, '-', label=label)
        plt.legend()
        plt.show()
        exit(0)

    # Plot history trace over median
    if True:
        historyLengths = np.array([24, 36, 60, 120, 240])*30.0

        figScale = 4.0
        figsize = (2.0 * figScale, figScale)
        for column in rainDf.columns:
            for length in historyLengths:

                minDate = pd.Timestamp.today() - pd.Timedelta(length, unit='D')
                maxDate = pd.Timestamp.today()
                plotDateRange = pd.date_range(start=minDate, end=maxDate, freq='D').normalize()
                plotDayOfYear = plotDateRange.dayofyear

                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(1, 1, 1)

                ax.plot(plotDateRange, np.array(rain_median.loc[plotDayOfYear, column])*30.0, label='{0} median'.format(column))

                # ax.plot(rainDf_rolling.loc[plotDateRange, column]*30.0, label='{0} recent'.format(column))
                ax.plot(rainDf_rolling.reindex(plotDateRange)[column]*30.0, label='{0} recent'.format(column))

                # plot the seasons
                plotSeasonBands(minDate=minDate, maxDate=maxDate, ax=ax)

                # Plot 90% CI
                CImax = 1.64*np.array(rain_std.loc[plotDayOfYear, column]) + np.array(rain_median.loc[plotDayOfYear, column])
                CImin = -1.64*np.array(rain_std.loc[plotDayOfYear, column]) + np.array(rain_median.loc[plotDayOfYear, column])
                ax.fill_between(plotDateRange, CImin*30.0, CImax*30.0, facecolor='0.2', alpha=0.3)
                ax.set_ylim(bottom=0.0)
                # ax.set_ylabel('Daily Rainfall (mm)')
                ax.set_ylabel('Sum of 30 Day Rainfall (mm)')

                ax.legend()
                fname='{0}00_{2}_currentHistory_{1}months.png'.format(figureFolder, length, column)
                fig.savefig(fname=fname, dpi=200)
                plt.close(fig)
                copyTowwwFolder(currentImagePath=fname)

    # Plot the rain anomaly away from median.
    if True:
        figScale = 3.0
        figsize = (2.0* figScale, figScale)

        for column in rainDf.columns:
            minDate = rainDf_rolling.index[0]
            maxDate = pd.Timestamp.today()
            plotDateRange = pd.date_range(start=minDate, end=maxDate, freq='D').normalize()
            plotDayOfYear = plotDateRange.dayofyear

            # anomaly = rainDf_rolling.loc[plotDateRange, column] - np.array(rain_median.loc[plotDayOfYear, column])
            anomaly = rainDf_rolling.reindex(plotDateRange)[column] - np.array(rain_median.loc[plotDayOfYear, column])

            anomalyPercent = (anomaly/np.array(rain_median.loc[plotDayOfYear, column]))*100.0

            if True:
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(1, 1, 1)

                ax.plot(anomaly.rolling(window=3*365, min_periods=365).median())
                ax.set_title(column + ' daily rainfall anomaly')
                # ax.set_ylabel('Rainfall anomaly (mm) \n (3y rolling median filter)')
                ax.set_ylabel('Rainfall anomaly (% from median) \n (3y rolling median filter applied)')

                # ax.set_ylim(bottom=-50, top=50)
                ax.hlines(0.0, xmin=minDate, xmax=maxDate)
                plotSeasonBands(minDate=minDate, maxDate=maxDate, ax=ax)
                fname = '{0}01_rainfallAnomalyTrace_{1}.png'.format(figureFolder, column)
                fig.savefig(fname=fname)
                plt.close(fig)
                copyTowwwFolder(currentImagePath=fname)


            if True:

                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(1, 1, 1)

                window = 8*365
                # excessDeficit = anomaly.rolling(window=window, min_periods=30).sum()/window*30
                excessDeficit = anomaly.rolling(window=window, min_periods=30).sum()/window #*30
                cumulativeMedian = rain_median.loc[plotDayOfYear, column].rolling(window=window, min_periods=30).sum()/window
                excessDeficitPercent = ((excessDeficit/np.array(cumulativeMedian))+1)*100.0
                excessDeficit = excessDeficitPercent.rolling(window=30*12,min_periods=10).median()
                ax.plot(excessDeficit)
                ax.set_title(column + ' rainfall excess/deficit in 30 days')
                ax.hlines(100.0, xmin=minDate, xmax=maxDate)
                # ax.set_ylim(bottom=-50, top=50)
                ax.set_ylabel('Cumulative rainfall (%)')

                plotSeasonBands(minDate=minDate, maxDate=maxDate, ax=ax)

                fname = '{0}02_rainfallDeficitTrace_{1}.png'.format(figureFolder, column)
                fig.savefig(fname=fname)
                plt.close(fig)
                copyTowwwFolder(currentImagePath=fname)




exit(0)

if True:
    yearlyTotal = rainDf.resample('Y').sum().rolling(window=5, min_periods=1).mean()
    years = yearlyTotal.index.year
    years -= np.max(years)+1

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for column, data in yearlyTotal.iteritems():
        # plt.semilogx(np.abs(years[::-1]), data[::-1], label=column)
        # print(years)
        # print(np.array(data))
        # exit(0)
        ax.plot(data, label=column)
    fromDate = pd.to_datetime('1900-1-1')
    # plt.xlim(left=fromDate)
    ax.set_ylim(bottom=1.0)

    ax.legend()
    fig.savefig('totalRainfallHistory.png', dpi=200)
    plt.close(fig)

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

if False:
    for column, label in zip(np.array(monthlyTotals).T, monthlyTotals.columns):
        column = column[~np.isnan(column)]
        y, binEdges = np.histogram(column, bins=15, density=1)
        bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
        plt.plot(bincenters, y, '-', label=label)
    plt.legend()
    plt.show()
