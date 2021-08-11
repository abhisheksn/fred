from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)
import base64
import plotly.graph_objects as go
import os, time, csv, datetime, requests, json, matplotlib, time
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from dotenv import load_dotenv
from pandas import read_csv

all_states=["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MS", "MO", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

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
#columns_df = ["State","Median Listing Price", "UR", "GDP", "POP", "INC", "Coefficient"]

cur_date = datetime.datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

#state_id = input("Please enter the State Abbreviation Code:")

report = pd.DataFrame()

for s in all_states:
    #print(s)

    #Here we'll store all the slopes from different df's
    slps = list(range(6))
    med_price = None
    prognosis = None

    for report_id in range (1,6):

        df = request(hashgen(s, report_id), api_key, tfs[report_id])
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
    report = report.append({"State": s, "Median Listing Price": med_price, "UR": slps[1], "GDP": slps[2], "POP": slps[3], "INC": slps[5], "Coefficient":score, "Recommendation": prognosis}, ignore_index=True)
    time.sleep(2)

filename = f"data/fred_{cur_date}.csv"
report.to_csv(filename)

#Sending CSV attachment as email

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL")

user_email = input("Please enter your Email address:")

message = Mail(
    from_email=SENDER_EMAIL_ADDRESS,
    to_emails=user_email,
    subject='AGY Consultants Country Report',
    html_content='Please find the AGY Consultants Country Report attached with this email.')
with open(filename, 'rb') as f:
    data = f.read()
    f.close()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_name = FileName('AGY Consultants Country Report.csv')
message.attachment = attachment
try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print("Email Successfully Delivered")
except Exception as e:
    print("OOPS", type(e), e)

#Chloropleth Map
#Source: https://plotly.com/python/choropleth-maps/
df = read_csv(filename)
fig = go.Figure(data=go.Choropleth(
    locations=df['State'],  # Spatial coordinates
    z=df['Coefficient'].astype(float),  # Data to be color-coded
    locationmode='USA-states',  # set of locations match entries in `locations`
    colorscale='Spectral',
    colorbar_title="AGY Coefficient Score",
))

fig.update_layout(
    title_text='AGY Coefficient by State Aug 2021',
    geo_scope='usa',  # limit map scope to USA
)

fig.show()
