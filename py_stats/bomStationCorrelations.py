import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import weatherHistoryFuncs as whf

stationProductPairs = (
    ('redesdale', 'rainfall'),
    ('redesdale', 'tmax'),
    ('redesdale', 'tmin'),
    ('redesdale', 'solarExp'),

    # ('lakeEildon', 'rainfall'),
    # ('lakeEildon', 'tmax'),
    # ('lakeEildon', 'tmin'),
    # ('lakeEildon', 'solarExp'),

    ('castlemainePrison', 'tmax'),
)

dataDf = whf.assembleDataframe(stationProductPairs)
print(dataDf)


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
    # ax.plot(dataDf['redesdale_rainfall'], dataDf['redesdale_tmax']-dataDf['redesdale_tmin'], ls='None', marker='.')
    ax.plot(dataDf['redesdale_rainfall'], dataDf['redesdale_solarExp'], ls='None', marker='.')

    ax.set_xlabel('Rainfall mm')
    ax.set_ylabel('Temp delta')

    plt.show()
    exit(0)