import os
import requests
import json
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

#Loading API Key from .env file
load_dotenv()
api_key = os.getenv("FRED_API_KEY")


state_id = input("Please enter the State Abbreviation Code:")
series_id = (state_id) + "UR"  #Unemployment by State
#series_id = (state_id) + "RQGSP" #GDP by State
#series_id = (state_id) + "POP" #Resident population by State
#series_id = "MEDLISPRI" + (state_id) #Median Listing Price by State
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
