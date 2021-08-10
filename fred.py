import os, time, csv, datetime, requests, json, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from dotenv import load_dotenv

#This function generates the right series_id depending on the scenario
def hashgen(state_id, dt_code):
    series_id = list(range(6))
    series_id[1] = (state_id) + "UR"  #Unemployment by State: STD, Monthly data, June 21
    series_id[2] = (state_id) + "RQGSP" #GDP by State: STD, Qtrly data, Jan 21
    series_id[3] = (state_id) + "POP" #Resident population by State: STD, Annual data, Jan 20
    series_id[4] = "MEDLISPRI" + (state_id) #Median Listing Price by State: STD, Monthly data, June 21
    series_id[5] = "MEHOINUS" + (state_id) + "A646N" #Median Household income by State: STD, Annual data, Jan 19
    return series_id[dt_code]

#This function pulls a nicely framed DF for certain state and scenario
def request(series_id, api_key, yrs):
    FRED_URL = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
    FRED_request = requests.get(FRED_URL)
    FRED_data = json.loads(FRED_request.text)
    data = FRED_data["observations"]
    df = pd.DataFrame(data)
    df.date=pd.to_datetime(df.date)
    cutoff_dt = df.date.max() - pd.DateOffset(years=yrs)
    df = df[df.date > cutoff_dt]
    return df

#Loading API Key from .env file
load_dotenv()
api_key = os.getenv("FRED_API_KEY")


#web_app_updates
state_id = input("Please enter the State Abbreviation Code:")
#series_id = (state_id) + "UR"  #Unemployment by State
#series_id = (state_id) + "RQGSP" #GDP by State
#series_id = (state_id) + "POP" #Resident population by State
series_id = "MEDLISPRI" + (state_id) #Median Listing Price by State
#series_id = "MEHOINUS" + (state_id) + "A646N"

#Request from FRED URL
FRED_URL = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
FRED_request = requests.get(FRED_URL)
FRED_data = json.loads(FRED_request.text)
data = FRED_data["observations"]
df = DataFrame(data)
print(df)
fig = px.line(df, x='date', y='value', title=f'{series_id} over time')
fig.show()
=======
#Since the data on FRED is presented differently, we'll use different timeframes for different reports:
tfs = [
    None,
    1, # of years for Unemployment by State
    1,   # of years for GDP by State
    2,   # of years for Resident population by State
    1,   # of years for Median Listing Price by State
    2    # of years for Median Household income by State
]

columns = [0, 1]

cur_date = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

state_id = "CT"

for report_id in range (1,6):
    filename = f"data/fred_{hashgen(state_id, report_id)}-{cur_date}.csv"
    df = request(hashgen(state_id, report_id), api_key, tfs[report_id])
    df.to_csv(filename)

#state_id = input("Please enter the State Abbreviation Code:")

#df.drop(df.columns[columns], axis=1, inplace=True)
#df.reset_index(drop=True, inplace=True)
#df.value = pd.to_numeric(df.value, errors='coerce', downcast='float')
#df["dt_ord"] = pd.to_datetime(df["date"]).map(datetime.datetime.toordinal)
#slope, intercept, r_value, p_value, std_err = stats.linregress(df.index, df["value"])
#print(df.dtypes)
#print(slope)
#dts = df.value
#print(dts)
#dts.plot(label = "Unemployment Rate")
#plt.legend()
#plt.show()
#print(df)
#>>>>>>> main
