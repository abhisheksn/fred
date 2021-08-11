import os, time, datetime, requests, json, time
import pandas as pd
from scipy import stats
from dotenv import load_dotenv

#Converting numeric value to USD formatted string
#source: Professor Rossetti
def to_usd(my_price):
    my_price = int(my_price)
    return f"${my_price:,}"

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
    #data = FRED_data["observations"]
    try:
        data = FRED_data["observations"]
    except KeyError:
        print("Incorrect input, try again!")
        return None
    df = pd.DataFrame(data)
    df.date=pd.to_datetime(df.date)
    cutoff_dt = df.date.max() - pd.DateOffset(years=yrs)
    df = df[df.date > cutoff_dt]
    return df

def func(state_id):

    #Loading API Key from .env file
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")

    #Since the data on FRED is presented differently, we'll use different timeframes for different reports:
    tfs = [
        None,
        1, # of years for Unemployment by State
        1,   # of years for GDP by State
        2,   # of years for Resident population by State
        1,   # of years for Median Listing Price by State
        2    # of years for Median Household income by State
    ]

    #Here we determine weights for different criteria
    indexes = [
        None,
        -10, # index for Unemployment by State
        5,   # index for GDP by State
        20,   # index for Resident population by State
        None,
        3    # index for Median Household income by State
    ]

    columns = [0, 1]
    slps = list(range(6))

    cur_date = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

    for report_id in range (1,6):

        df = request(hashgen(state_id, report_id), api_key, tfs[report_id])
        if df is None:
            return None
        df.drop(df.columns[columns], axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.value = pd.to_numeric(df.value, errors='coerce', downcast='float')
        slope, intercept, r_value, p_value, std_err = stats.linregress(df.index, df["value"])
        slps[report_id] = slope/df.value.median() #We'll use weighted slopes
        if report_id == 4:
            med_price = float(df.value.tail(1))

    score = (slps[1]+0.05) * indexes[1] + (slps[2]-0.03) * indexes[2] + slps[3] * indexes[3] + (slps[5]-0.08) * indexes[5]
    if score > 0.4:
        prognosis = "Strong positive"
    elif score > 0:
        prognosis = "Positive"
    elif score > -0.4:
        prognosis = "Negative"
    else:
        prognosis = "Strong negative"
    med_price = to_usd(med_price)
    return med_price, prognosis

if __name__ == "__main__":
    #This is the input!!!
    state_id = input("Please enter the State Abbreviation Code:")
    mp, sc = func(state_id)

    print("State:", state_id)
    print("Median price:", mp)
    print("Recommendation:",sc)
