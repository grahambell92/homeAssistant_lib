import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import weatherHistoryFuncs as whf
import os

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

stationProductPairs = (
    ('redesdale', 'rainfall'),
    ('malmsbury_reservoir', 'rainfall'),
    ('lauriston_reservoir', 'rainfall'),
    ('kyneton', 'rainfall'),
    # ('castlemainePrison', 'rainfall'),
    # ('leongatha', 'rainfall'),
    ('bendigo', 'rainfall'),
    ('newham (cobaw)', 'rainfall'),
    ('baynton', 'rainfall'),
    ('lancefield', 'rainfall'),
    ('eppalockReservoir', 'rainfall'),
    ('daylesford', 'rainfall'),
)

rainDf = whf.assembleDataframe(stationProductPairs)



figureFolder = './figs/rainfall/'
figSize = (8, 6)
os.makedirs(figureFolder, exist_ok=True)
integrationWindow = 50 # days
rainDf_rolling_density = rainDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum() / integrationWindow

# Compute the rolling sum to get interpolated rain value.
rainDf_rolling_density['dayOfYear'] = rainDf_rolling_density.index.dayofyear
# Compute the yearly median by comparing each day of year over the years.
rain_median = rainDf_rolling_density.groupby(by='dayOfYear').median()
rain_mean = rainDf_rolling_density.groupby(by='dayOfYear').mean()
rain_std = rainDf_rolling_density.groupby(by='dayOfYear').std()

if True:
    # Horziontal bar plot of valid data ranges.
    fig = plt.figure(figsize=figSize)
    ax = fig.add_subplot(1, 1, 1)
    ax1= ax.twinx()
    # plt.pcolormesh(rainDf.index, rainDf.columns, np.transpose(rainDf.notna()),cmap='Blues')
    availableData = rainDf.notna()
    sortByMostData = availableData.sum().sort_values()
    sortedCols = list(sortByMostData.index)
    # re sort the raindf
    rainDf = rainDf[sortedCols]
    numOfValidDays = rainDf[sortedCols].notna().sum()
    ax.imshow(np.transpose(rainDf[sortedCols].notna()), aspect='auto', cmap='Blues')

    # plt.xticks(rainDf.index)
    xTickLabels = pd.date_range(start=rainDf.index[0], end=rainDf.index[-1], periods=8)
    xTicks = np.linspace(start=0, stop=len(rainDf), num=8)
    ax.set_xticks(xTicks)
    ax.set_xticklabels(xTickLabels.year)


    yTicks = np.arange(len(rainDf.columns))
    ax.set_yticks(yTicks)
    ax.set_yticklabels(rainDf.columns)

    ax1.set_ylim(ax.get_ylim())
    ax1.set_yticks(yTicks)
    dayYearLabels = [r'{0} days/\n{1:.1f} years'.format(days, days/365) for place, days in numOfValidDays.iteritems()]
    # print(dayYearLabels)
    # exit(0)
    ax1.set_yticklabels(numOfValidDays)
    ax1.set_ylabel('Valid days/years')
    plt.show()
        # yTicks = np.arange(len(rainDf.columns))
    # plt.yticks(yTicks[:-1] + 0.5)
    fig.tight_layout()
    fname = figureFolder + '05_availableData.png'
    fig.savefig(fname=fname, dpi=200)
    exit(0)



# compare medians
if True:
    fig = plt.figure(figsize=figSize)
    ax = fig.add_subplot(1, 1, 1)
    for column in rain_median.columns:
        ax.plot(30.0*rain_median[column], label='{0}'.format(column))
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
exit(0)
# Look at median and variance
if False:
    fig = plt.figure(figsize=figSize)
    ax = fig.add_subplot(1, 1, 1)
    ax2 = ax.twinx()
    integrationWindow = 50  # days
    for column in ['redesdale_rainfall']: #rainDf.columns:
        # ax.plot(rain_median_long[column], label='{0} median'.format(column))
        smoothMedian = rain_median[column].rolling(window=30, min_periods=5).mean()
        smoothStd = rain_std[column].rolling(window=30, min_periods=5).mean()
        ax.plot(smoothMedian, color='b', label='{0} Median'.format(column))
        ax2.plot(smoothStd, color='r', label='{0} Std'.format(column))

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

# Bar plot of total rainfall per year
if False:
    fig = plt.figure(figsize=figSize)
    ax = fig.add_subplot(1, 1, 1)
    rain_median_annual = rain_median.sum().sort_values()
    for index, row in enumerate(rain_median_annual.iteritems()):
        columns, value = row
        ax.bar(index, value)
        ax.text(index, value + 5.0, '{:0.0f}'.format(value),
                color='blue', fontweight='bold', ha='center',)

    ax.set_xticks(np.arange(len(np.array(rain_median.columns))))
    ax.set_xticklabels(np.array(rain_median.columns), rotation=45)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_ylabel('Annual rainfall (mm)')
    fig.tight_layout()
    fname = figureFolder + '05_annualRainfall_bar.png'
    fig.savefig(fname=fname, dpi=200)
    plt.close(fig)

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
if False:
    historyLengths = np.array([24, 36, 60, 120, 240])*30.0

    figScale = 4.0
    figsize = (2.0 * figScale, figScale)
    for column in ['redesdale_rainfall']: #rain_median.columns:
        for length in historyLengths:
            minDate = pd.Timestamp.today() - pd.Timedelta(length, unit='D')
            maxDate = pd.Timestamp.today()
            plotDateRange = pd.date_range(start=minDate, end=maxDate, freq='D').normalize()
            plotDayOfYear = plotDateRange.dayofyear

            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(1, 1, 1)

            ax.plot(plotDateRange, np.array(rain_median.loc[plotDayOfYear, column])*30.0, label='{0} median'.format(column))

            # ax.plot(rainDf_rolling.loc[plotDateRange, column]*30.0, label='{0} recent'.format(column))
            ax.plot(rainDf_rolling_density.reindex(plotDateRange)[column]*30.0, label='{0} recent'.format(column))

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

# Plot the rain anomaly away from median.
if True:
    figScale = 3.0
    figsize = (2.0* figScale, figScale)

    for column in ['redesdale_rainfall']: #rainDf.columns:
        minDate = rainDf_rolling_density.index[0]
        maxDate = pd.Timestamp.today()
        plotDateRange = pd.date_range(start=minDate, end=maxDate, freq='D').normalize()
        plotDayOfYear = plotDateRange.dayofyear

        # anomaly = rainDf_rolling.loc[plotDateRange, column] - np.array(rain_median.loc[plotDayOfYear, column])
        anomaly = rainDf_rolling_density.reindex(plotDateRange)[column] - np.array(rain_median.loc[plotDayOfYear, column])

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
            # copyTowwwFolder(currentImagePath=fname)


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
            # copyTowwwFolder(currentImagePath=fname)