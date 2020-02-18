import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# kynetonDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0001_088123_kyneton/IDCJAC0001_088123_Data12.csv')
kynetonDf_tMax = pd.read_csv('./temperature/BOM_data/IDCJAC0010_089002_1800_ballarat_Tmax/IDCJAC0010_089002_1800_Data.csv')
kynetonDf_tMin = pd.read_csv('./temperature/BOM_data/IDCJAC0011_089002_1800_ballarat_Tmin/IDCJAC0011_089002_1800_Data.csv')
# bendigoRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_081123_1800_bendigo/IDCJAC0009_081123_1800_Data.csv')
# viewbankRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_086068_1800_viewbank/IDCJAC0009_086068_1800_Data.csv')
# euroaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_082016_1800_euroa/IDCJAC0009_082016_1800_Data.csv')
# leongathaRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_085049_1800_leongatha/IDCJAC0009_085049_1800_Data.csv')
# castlemaneRawDf = pd.read_csv('./rainfall/BOMdata/IDCJAC0009_088110_1800_castlemane/IDCJAC0009_088110_1800_Data.csv')


locations = ['KynetonMin',
             'KynetonMax',]
dataFrames = [
    kynetonDf_tMin,
    kynetonDf_tMax,
              ]


series = []
for df, location in zip(dataFrames, locations):
    index = pd.to_datetime(df[['Year', 'Month', 'Day']])
    try: rain = np.array(df['Maximum temperature (Degree C)'])
    except: rain = np.array(df['Minimum temperature (Degree C)'])
    series.append(pd.Series(data=rain, name=location, index=index))

# It's getting biased if the value is 0.
rainDf = pd.concat(series, axis=1)#.iloc[-20*12*30:, :]

if True:
    # print('Monthly average rainfall')
    # print(monthlyTotals.groupby('Month').mean())
    # print()
    # print('Yearly total')
    yearlyTotal = rainDf.resample('Y').mean().rolling(window=5, min_periods=1).mean()
    for column, data in yearlyTotal.iteritems():
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1900-1-1')
    plt.xlim(left=fromDate)
    plt.legend()
    plt.show()
    exit(0)
    exit(0)