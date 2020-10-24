import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import weatherHistoryFuncs as whf
import os

figureFolder = './figs/temperature/'
figSize = (8, 6)
os.makedirs(figureFolder, exist_ok=True)

stationProductPairs = (
    ('redesdale', 'tmax'),
    ('castlemainePrison', 'tmax'),
    ('ballarat', 'tmax'),
    ('ballarat', 'tmin'),
    ('bendigo', 'tmax'),
    ('bendigo', 'tmin'),
)

tempDf = whf.assembleDataframe(stationProductPairs)
tempDf['dayOfYear'] = tempDf.index.dayofyear
temp_median = tempDf.groupby(by='dayOfYear').median()
temp_mean = tempDf.groupby(by='dayOfYear').mean()
temp_std = tempDf.groupby(by='dayOfYear').std()

if False:
    # Horziontal bar plot of valid data ranges.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax1= ax.twinx()
    # plt.pcolormesh(rainDf.index, rainDf.columns, np.transpose(rainDf.notna()),cmap='Blues')
    availableData = tempDf.notna()
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
    fname = figureFolder + '05_availableData.png'
    fig.savefig(fname=fname, dpi=200)

# compare medians
if False:
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
    fname = figureFolder+'04_medianTmax.png'
    fig.savefig(fname=fname,dpi=200)
    plt.close(fig)

if True: # Diff between daily max and min
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
    fname = figureFolder + '06_medianTdelta.png'
    fig.savefig(fname=fname, dpi=200)
    plt.close(fig)