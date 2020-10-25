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

figureFolder = './figs/temperature/'
figSize = (8, 6)
os.makedirs(figureFolder, exist_ok=True)

stationProductPairs = (
    ('redesdale', 'tmax'),
    ('redesdale', 'tmin'),
    ('castlemainePrison', 'tmax'),
    ('ballarat', 'tmax'),
    ('ballarat', 'tmin'),
    ('bendigo', 'tmax'),
    ('bendigo', 'tmin'),
    ('melbourneAirport', 'tmax'),
    ('lavertonRAAF', 'tmax')
)

tempDf = whf.assembleDataframe(stationProductPairs)
tempDf['dayOfYear'] = tempDf.index.dayofyear
temp_median = tempDf.groupby(by='dayOfYear').median()
temp_mean = tempDf.groupby(by='dayOfYear').mean()
temp_std = tempDf.groupby(by='dayOfYear').std()

if True:
    # Horziontal bar plot of valid data ranges.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax1= ax.twinx()

    availableData = tempDf.loc[:, tempDf.columns != 'dayOfYear'].notna()
    sortByMostData = availableData.sum().sort_values()
    sortedCols = list(sortByMostData.index)
    # re sort the raindf
    rainDf = tempDf[sortedCols]
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

    dayYearLabels = ['{0} days/\n{1:.1f} years'.format(days, days/365) for place, days in numOfValidDays.iteritems()]

    ax1.set_ylim(ax.get_ylim())
    ax1.set_yticks(yTicks)
    ax1.set_yticklabels(dayYearLabels)
    ax1.set_ylabel('Amount of data')

    ax.set_xlabel('Year')
    ax.set_ylabel('Location')
        # yTicks = np.arange(len(rainDf.columns))
    # plt.yticks(yTicks[:-1] + 0.5)
    fig.tight_layout()
    fname = figureFolder + '00_availableData.png'
    fig.savefig(fname=fname, dpi=200)

# compare medians
if True:
    for tempType in ['tmax', 'tmin']:
        fig = plt.figure(figsize=figSize)
        ax = fig.add_subplot(1, 1, 1)

        for column in temp_median.columns:
            ax.plot(temp_median[column], label='{0}'.format(column))
        ax.set_ylabel('tmax')

        xticks = pd.date_range(start='1/1/2018', periods=12, freq='MS')
        ax.set_xticks(xticks.dayofyear, )
        ax.set_xticklabels(xticks.month_name(), rotation=45)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.yaxis.grid()
        ax.legend()
        fig.tight_layout()
        fname = figureFolder+'01_median_{0}.png'.format(tempType)
        fig.savefig(fname=fname,dpi=200)
        plt.close(fig)

if False: # Diff between daily max and min
    tempDf['bendigo_tdelta'] = tempDf['bendigo_tmax'] - tempDf['bendigo_tmin']
    tempDf['ballarat_tdelta'] = tempDf['ballarat_tmax'] - tempDf['ballarat_tmin']

    temp_median = tempDf.groupby(by='dayOfYear').median()

    fig = plt.figure(figsize=figSize)
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(temp_median['bendigo_tdelta'], label='bendigo')
    ax.plot(temp_median['ballarat_tdelta'], label='ballarat')

    ax.set_ylabel('temp delta daily')

    xticks = pd.date_range(start='1/1/2018', periods=12, freq='MS')
    ax.set_xticks(xticks.dayofyear, )
    ax.set_xticklabels(xticks.month_name(), rotation=45)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.yaxis.grid()
    ax.legend()
    fig.tight_layout()
    fname = figureFolder + '02_medianTdelta.png'
    fig.savefig(fname=fname, dpi=200)
    plt.close(fig)

if True:
    locations = [
        'redesdale_tmax',
        'redesdale_tmin',
        'castlemainePrison_tmax',
        'ballarat_tmax',
        'ballarat_tmin',
        'bendigo_tmax',
        'bendigo_tmin',
        'melbourneAirport_tmax',
        'lavertonRAAF_tmax'
    ]
    for location in locations:
        # Plot history trace over median
        plotFolder = figureFolder + location + '/'
        os.makedirs(plotFolder, exist_ok=True)
        figScale = 4.0
        figsize = (2.0 * figScale, figScale)

        minDate = tempDf.index[0]
        maxDate = pd.Timestamp.today()
        plotDateRange = pd.date_range(start=minDate, end=maxDate, freq='D').normalize()
        plotDayOfYear = plotDateRange.dayofyear

        anomaly = tempDf.reindex(plotDateRange)[location] - np.array(temp_median.loc[plotDayOfYear, location])

        anomalyPercent = (anomaly / np.array(temp_median.loc[plotDayOfYear, location])) * 100.0

        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)

        ax.plot(anomaly.rolling(window=3 * 365, min_periods=365).median())
        ax.set_title(location + ' daily temperature anomaly')
        # ax.set_ylabel('Rainfall anomaly (mm) \n (3y rolling median filter)')
        ax.set_ylabel('Temperature anomaly (deg C) \n (3y rolling median filter applied)')
        ax.set_ylim(-1.5, 1.5)

        # ax.set_ylim(bottom=-50, top=50)
        ax.hlines(0.0, xmin=minDate, xmax=maxDate)
        plotSeasonBands(minDate=minDate, maxDate=maxDate, ax=ax)
        fname = '{0}05_tempAnomalyTrace_{1}.png'.format(figureFolder, location)
        fig.savefig(fname=fname)
        plt.close(fig)
        # copyTowwwFolder(currentImagePath=fname)

if False:
    corrPairs = [
        ('redesdale_tmax', 'castlemainePrison_tmax'),
        ('redesdale_tmax', 'bendigo_tmax'),
        ('bendigo_tmax', 'bendigo_tmin'),
    ]
    for place1, place2 in corrPairs:
        plt.plot(tempDf[place1], tempDf[place2], ls='None',
                 marker='.', alpha=0.2)
        plt.title(place1 + ':' + place2)
        plt.show()
    exit(0)
