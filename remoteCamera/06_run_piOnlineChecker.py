import pandas as pd
import time
from datetime import datetime

# Check whether an internet connection exists.
try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


if __name__ == '__main__':

    timeBetweenAlivePosts = 60.0

    timeOfLastAlivePost = time.time() - 2*timeBetweenAlivePosts
    csvFile = 'rpiOnlineRecord.csv'
    emptyDf = pd.DataFrame(columns=['rpiRunning', 'haveInternet'])
    while True:
        timeSinceLastAlivePost = time.time() - timeOfLastAlivePost

        if timeSinceLastAlivePost > timeBetweenAlivePosts:
            timeOfLastAlivePost = time.time()

            try:
                csv = pd.read_csv(csvFile, index_col=0)
                if len(csv) > 60*24*20:
                    csv = emptyDf

            except:
                csv = emptyDf

            rpiRunning = 'True'
            internetExists = have_internet()

            csv.loc[str(datetime.now())] = [rpiRunning, internetExists]

            csv.to_csv(csvFile)

            if True:
                print('-'*20)
                print(csv)
            time.sleep(0.5)