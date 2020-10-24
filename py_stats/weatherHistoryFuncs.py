import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

causalCsvDataNaming = {
    'rainfall':     'Rainfall amount (millimetres)',
    'tmax':         'Maximum temperature (Degree C)',
    'tmin':         'Minimum temperature (Degree C)',
    'solarExp':     'Daily global solar exposure (MJ/m*m)',
}

bomDataIDs = {
    'rainfall':     'IDCJAC0009', # Rainfall amount (millimetres)
    'tmax':         'IDCJAC0010', # Maximum temperature (Degree C)
    'tmin':         'IDCJAC0011', # Minimum temperature (Degree C)
    'solarExp':     'IDCJAC0016', # 'Daily global solar exposure (MJ/m*m)'
}

bomIDToCasual = {v: k for k, v in bomDataIDs.items()}

bomDataProductToColumnName = {
    'IDCJAC0009': 'Rainfall amount (millimetres)',
    'IDCJAC0010': 'Maximum temperature (Degree C)',
    'IDCJAC0011': 'Minimum temperature (Degree C)',
    'IDCJAC0016': 'Daily global solar exposure (MJ/m*m)',
}

stationIDs = {
    'avoca': '081000',
    'dubbo': '065030',
    'kyneton': '088123',
    'redesdale': '088051',
    'bendigo': '081123',
    'euroa': '082016',
    'leongatha': '085049',
    'viewbank': '086068',
    'yanYean': '086131',
    'castlemainePrison': '088110',
    'malmsbury_reservoir': '088042',
    'lauriston_reservoir': '088037',
    'newham (cobaw)': '087175',
    'baynton': '088073',
    'lancefield': '087029',
    'eppalockReservoir': '081083',
    'daylesford': '088020',
    'ballarat': '089002',
    'macedonForestry': '087036',
}

stationIDToName = {v: k for k, v in stationIDs.items()}

# p_nccObsCode=136 = t min?
#
# sampleURL = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_display_type=dailyZippedDataFile&p_stn_num=088051&p_c=-1550731119&p_nccObsCode=136&p_startYear=2020

# sampleURL = 'http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_display_type=dailyZippedDataFile&p_stn_num=088051&p_nccObsCode=136&p_startYear=2020


def pullData():
    pass

def getProduct(stationName, productName):
    print()
    print('Trying to fetch:', stationName, productName)

    stationID = stationIDs[stationName]
    productID = bomDataIDs[productName]

    baseFolder = './bomData/'
    dataFolder = '_'.join([productID, stationID, '1800/'])
    productFile = '_'.join([productID, stationID, '1800_Data.csv'])
    # data = pd.read_csv('./temperature/BOM_data/IDCJAC0011_088123_1800_kyneton_Tmin/IDCJAC0011_088123_1800_Data.csv')
    productPath = baseFolder + dataFolder + productFile
    print(productPath)
    rawDf = pd.read_csv(productPath)
    # Strip out and just get the timeseies
    columnName = bomDataProductToColumnName[productID]
    index = pd.to_datetime(rawDf[['Year', 'Month', 'Day']])
    dataDf = np.array(rawDf[columnName])

    humanReadableName = '_'.join([stationIDToName[stationID], bomIDToCasual[productID]])
    outputDf = pd.Series(data=dataDf, name=humanReadableName, index=index)

    return outputDf

def assembleDataframe(stationProductPairs):
    # tell me what products you want put into a dataframe
    # format. list = ((station, product), (station, product))

    series = []
    for (stationName, productName) in stationProductPairs:
        productDf = getProduct(stationName, productName)
        series.append(productDf)
    # It's getting biased if the value is 0.
    dataDf = pd.concat(series, axis=1)  # .iloc[-20*12*30:, :]

    return dataDf

if __name__ == '__main__':
    stationProductPairs = (
        ('redesdale', 'rainfall'),
        ('redesdale', 'tmax'),
        ('redesdale', 'tmin'),
        ('redesdale', 'solarExp'),

        ('lakeEildon', 'rainfall'),
        # ('lakeEildon', 'tmax'),
        # ('lakeEildon', 'tmin'),
        # ('lakeEildon', 'solarExp'),

        ('castlemainePrison', 'tmax'),
    )

    dataDf = assembleDataframe(stationProductPairs)
    print(dataDf)

    if True:
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
    exit(0)