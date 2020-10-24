import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#bom product codes
dailyMinTemp = 'IDCJAC0011'
dailyMaxTemp = 'IDCJAC0010'
dailySolarExposure = 'IDCJAC0016'

kynetonDf_tMin = pd.read_csv('./temperature/BOM_data/IDCJAC0011_088123_1800_kyneton_Tmin/IDCJAC0011_088123_1800_Data.csv')
kynetonDf_tMax = pd.read_csv('./temperature/BOM_data/IDCJAC0010_088123_1800_kyneton_Tmax/IDCJAC0010_088123_1800_Data.csv')
kynetonDf_solar = pd.read_csv('./temperature/BOM_data/IDCJAC0016_088123_1800_kyneton_solarExp/IDCJAC0016_088123_1800_Data.csv')

redesdaleDf_tMin = pd.read_csv('./temperature/BOM_data/IDCJAC0011_088051_1800_redesdale_Tmin/IDCJAC0011_088051_1800_Data.csv')
redesdaleDf_tMax = pd.read_csv('./temperature/BOM_data/IDCJAC0010_088051_1800_redesdale_Tmax/IDCJAC0010_088051_1800_Data.csv')
redesdaleDf_solar = pd.read_csv('./temperature/BOM_data/IDCJAC0016_088051_1800_redesdale_solarExp/IDCJAC0016_088051_1800_Data.csv')

ballaratDf_tMin = pd.read_csv('./temperature/BOM_data/IDCJAC0011_089002_1800_ballarat_Tmin/IDCJAC0011_089002_1800_Data.csv')
ballaratDf_tMax = pd.read_csv('./temperature/BOM_data/IDCJAC0010_089002_1800_ballarat_Tmax/IDCJAC0010_089002_1800_Data.csv')
castlemainePrision_tMax = pd.read_csv('./temperature/BOM_data/IDCJAC0010_088110_1800_castlemainePrison_Tmax/IDCJAC0010_088110_1800_Data.csv')
castlemainePrision_tMin = pd.read_csv('./temperature/BOM_data/IDCJAC0011_088110_1800_castlemainePrison_Tmin/IDCJAC0011_088110_1800_Data.csv')


kynetonNames = [
    'redesdaleTmin',
    'redesdaleTmax',
    'redesdaleSolarExp',
]

kynetonDfs = [
    redesdaleDf_tMin,
    redesdaleDf_tMax,
    redesdaleDf_solar,
]

temp_locations = [
    'KynetonMin',
    'KynetonMax',
    'RedesdaleMax',
    'RedesdaleMin',
    'ballaratMin',
    'ballaratMax',
    'castlemaineMax',
    'castlemaineMin',
]

tempDfs = [
    kynetonDf_tMin,
    kynetonDf_tMax,
    redesdaleDf_tMin,
    redesdaleDf_tMax,
    ballaratDf_tMin,
    ballaratDf_tMax,
    castlemainePrision_tMax,
    castlemainePrision_tMin,
              ]
# For the temperature dataframes.
series = []
for df, location in zip(tempDfs, temp_locations):
    index = pd.to_datetime(df[['Year', 'Month', 'Day']])
    try: rain = np.array(df['Maximum temperature (Degree C)'])
    except: rain = np.array(df['Minimum temperature (Degree C)'])
    series.append(pd.Series(data=rain, name=location, index=index))

# It's getting biased if the value is 0.
dataDf = pd.concat(series, axis=1) #.iloc[-20*12*30:, :]

# For the Kyneton correlation
series = []
for df, location in zip(kynetonDfs, kynetonNames):
    index = pd.to_datetime(df[['Year', 'Month', 'Day']])
    print(df.columns)
    if 'Maximum temperature (Degree C)' in df.columns:
        rain = np.array(df['Maximum temperature (Degree C)'])
    elif 'Minimum temperature (Degree C)' in df.columns:
        rain = np.array(df['Minimum temperature (Degree C)'])
    elif 'Daily global solar exposure (MJ/m*m)' in df.columns:
        rain = np.array(df['Daily global solar exposure (MJ/m*m)'])
    series.append(pd.Series(data=rain, name=location, index=index))
redesdale_dataDf = pd.concat(series, axis=1) #.iloc[-20*12*30:, :]


if False:

    integrationWindow = 365  # days
    # dataDf_rolling = dataDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum() / integrationWindow
    dataDf_rolling = dataDf.rolling(window=integrationWindow, min_periods=int(integrationWindow/3)).median()
    # print(dataDf_rolling)
    # exit(0)

    # Compute the rolling sum to get interpolated rain value.
    # dataDf_rolling['dayOfYear'] = dataDf_rolling.index.dayofyear
    # Compute the yearly median by comparing each day of year over the years.
    # rain_median = dataDf_rolling.groupby(by='dayOfYear').median()

    # yearlyTotal = dataDf.resample('Y').mean().rolling(window=5, min_periods=1).mean()
    print(dataDf_rolling.head())

    for column, data in dataDf_rolling.iteritems(): #yearlyTotal.iteritems():
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1950-1-1')
    plt.xlim(left=fromDate)
    plt.legend()
    plt.show()
    exit(0)

# plot all the data for Redesdale
if False:
    integrationWindow = 365  # days
    # dataDf_rolling = dataDf.rolling(window=integrationWindow, min_periods=integrationWindow).sum() / integrationWindow
    dataDf_rolling = redesdale_dataDf.rolling(window=integrationWindow, min_periods=int(integrationWindow / 3)).median()
    # print(dataDf_rolling)
    # exit(0)

    # Compute the rolling sum to get interpolated rain value.
    # dataDf_rolling['dayOfYear'] = dataDf_rolling.index.dayofyear
    # Compute the yearly median by comparing each day of year over the years.
    # rain_median = dataDf_rolling.groupby(by='dayOfYear').median()

    # yearlyTotal = dataDf.resample('Y').mean().rolling(window=5, min_periods=1).mean()
    print(dataDf_rolling.head())

    for column, data in dataDf_rolling.iteritems():  # yearlyTotal.iteritems():
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1950-1-1')
    plt.xlim(left=fromDate)
    plt.legend()
    plt.show()
    exit(0)

# Plot the redesdale correlational data
if True:
    # plt.plot(redesdale_dataDf['redesdaleTmax'], redesdale_dataDf['redesdaleSolarExp'],
    #          ls='None', marker='.')
    redesdale_dataDf.dropna(inplace=True)
    plt.scatter(x=redesdale_dataDf['redesdaleTmax'],
                y=redesdale_dataDf['redesdaleTmin'],
                c=redesdale_dataDf['redesdaleSolarExp'],
                s=3,
                )
    plt.xlabel('Tmax')
    plt.ylabel('Tmin')
    # plt.ylabel('Solarexp')
    plt.show()
    exit(0)
    for column, data in redesdale_dataDf.iteritems():  # yearlyTotal.iteritems():
        plt.plot(data, label=column)
    fromDate = pd.to_datetime('1950-1-1')
    plt.xlim(left=fromDate)
    plt.legend()
    plt.show()
    exit(0)
