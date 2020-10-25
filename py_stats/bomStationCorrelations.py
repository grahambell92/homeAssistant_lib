import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import weatherHistoryFuncs as whf
import os

stationProductPairs = (
    ('redesdale', 'rainfall'),
    ('redesdale', 'tmax'),
    ('redesdale', 'tmin'),
    ('redesdale', 'solarExp'),

    ('malmsbury_reservoir', 'solarExp'),
    ('malmsbury_reservoir', 'rainfall'),

    ('lauriston_reservoir', 'rainfall'),

    ('castlemainePrison', 'tmax'),
)

dataDf = whf.assembleDataframe(stationProductPairs)
print(dataDf)

figureFolder = './figs/correlations/'
os.makedirs(figureFolder, exist_ok=True)


if False:
    stationProductPairs = (
        ('redesdale', 'rainfall'),
        ('castlemainePrison', 'rainfall'),
        ('leongatha', 'rainfall'),
    )
    dataDf = whf.assembleDataframe(stationProductPairs)
    # dataDf['dayOfYear'] = dataDf.index.dayofyear
    if False:
        hist = dataDf.hist(bins=50)
        # plt.plot(dataDf['redesdale_tmin'], dataDf['castlemainePrision_tmin'], ls='None', marker='.')
        plt.show()

    if True:
        # amount vs how many days it rained
        stationProductPairs = (
            ('redesdale', 'rainfall'),
            ('kyneton', 'rainfall'),
            # ('castlemainePrison', 'rainfall'),
            # ('leongatha', 'rainfall'),
            # ('bendigo', 'rainfall'),
        )

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for (station, product) in stationProductPairs:

            #getProduct returns a pandas Series, not a df.
            dataDf = whf.getProduct(station, product).to_frame()
            # print(dataDf)
            # exit(0)
            didItRain = dataDf> 0.05

            integrationWindow = 30
            # in integration window, how many days did it rain? Then normalise by size of window to get % of time it was raining.
            didItRain_rolling = didItRain.rolling(window=integrationWindow, min_periods=5).sum()/integrationWindow

            didItRain_rolling['dayOfYear'] = didItRain_rolling.index.dayofyear
            # print(didItRain_rolling)
            # exit(0)
            rain_median = didItRain_rolling.groupby(by='dayOfYear').median()
            # exit(0)
            # rain_std = didItRain_rolling.groupby(by='dayOfYear').std()

            name = station+'_'+product
            ax.plot(rain_median[name], label=name)
            # print(rain_median)

        xticks = pd.date_range(start='1/1/2018', periods=12, freq='MS')
        ax.set_xticks(xticks.dayofyear, )
        ax.set_xticklabels(xticks.month_name(), rotation=45)
        ax.legend()
        plt.show()
        exit(0)
        # print(dataDf.iloc[100:200, :]>0.1)
    exit(0)


if False:
    # columns with rainfall in them
    filterWord = 'tmax'
    goodCols = [string for string in dataDf.columns if filterWord in string]
    dataDf = dataDf[goodCols]
    integrationWindow = 365  # days
    # dataDf_rolling = dataDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum() / integrationWindow
    dataDf_rolling = dataDf.rolling(window=integrationWindow,
                                    min_periods=int(integrationWindow / 3)).median()
    for column, data in dataDf_rolling.iteritems():  # yearlyTotal.iteritems():
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1950-1-1')
    plt.xlim(left=fromDate)
    plt.legend()
    plt.show()
    exit(0)

if True:
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dataDf['redesdale_solarExp'], dataDf['malmsbury_reservoir_solarExp'], ls='None', marker='.',
            markeredgecolor='None', alpha=0.3)
    ax.plot([0, 35], [0, 35], color='k')
    ax.set_xlabel('Redesdale Solar Exposure (MJ/day)')
    ax.set_ylabel('Malmsbury Reservoir Solar Exposure (MJ/day)')
    ax.set_aspect('equal')

    fig.savefig(figureFolder + '00_redesdaleSolar-malmsburyReservoirSolar.png', dpi=200)
    plt.close(fig)




    integrationWindow = 30  # days
    redesdaleRolling = dataDf['redesdale_rainfall'].rolling(window=integrationWindow,
                                            min_periods=integrationWindow).sum()
    malmsburyRolling = dataDf['malmsbury_reservoir_rainfall'].rolling(window=integrationWindow,
                                                            min_periods=integrationWindow).sum()

    lauristonRolling = dataDf['lauriston_reservoir_rainfall'].rolling(window=integrationWindow,
                                                            min_periods=integrationWindow).sum()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(redesdaleRolling, malmsburyRolling, ls='None', marker='.', alpha=0.1, markeredgecolor='None',)
    ax.plot([0, 250], [0, 250], color='k')
    ax.set_xlabel('Redesdale 30 cum. rainfall (mm)')
    ax.set_ylabel('Malmsbury Reservoir 30 cum. rainfall (mm)')

    ax.set_aspect('equal')

    fig.savefig(figureFolder + '00_redesdaleRainfall-malmsburyReservoirRainfall.png', dpi=200)

    plt.close(fig)



    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(lauristonRolling, malmsburyRolling, ls='None', marker='.', alpha=0.1, markeredgecolor='None',)
    ax.plot([0, 250], [0, 250], color='k')
    ax.set_xlabel('Lauriston Reservoir 30 cum. rainfall (mm)')
    ax.set_ylabel('Malmsbury Reservoir 30 cum. rainfall (mm)')

    ax.set_aspect('equal')

    fig.savefig(figureFolder + '00_LauristonReservoirRainfall-malmsburyReservoirRainfall.png', dpi=200)

    plt.close(fig)


    exit(0)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dataDf['redesdale_solarExp'], dataDf['malmsbury_reservoir_solarExp'], ls='None', marker='.')

    ax.set_xlabel('redesdale solarexp')
    ax.set_ylabel('malmsbury solarexp')
    fig.savefig(figureFolder + '00_redesdaleSolar-malmsburyReservoirSolar.png', dpi=200)

    plt.show()
    exit(0)

if True:
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # ax.plot(dataDf['redesdale_rainfall'], dataDf['redesdale_tmax']-dataDf['redesdale_tmin'], ls='None', marker='.')
    ax.plot(dataDf['redesdale_rainfall'], dataDf['redesdale_solarExp'], ls='None', marker='.')

    ax.set_xlabel('Rainfall mm')
    ax.set_ylabel('Temp delta')

    plt.show()
    exit(0)