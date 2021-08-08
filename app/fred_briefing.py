import os
from dotenv import load_dotenv
from datetime import date

from app import APP_ENV
from app.weather_service import set_geography
from app.email_service import send_email

load_dotenv()

USER_NAME = os.getenv("USER_NAME", default="Player 1")


if __name__ == "__main__":

    #print(f"RUNNING THE FRED BRIEFING APP IN {APP_ENV.upper()} MODE...")

    # CAPTURE INPUTS

    user_state = set_geography()
    print("STATE:", user_state)
    


    # FETCH DATA



    # DISPLAY OUTPUTS

    todays_date = date.today().strftime('%A, %B %d, %Y')

    html = ""
    html += f"<h3>Good Morning, {USER_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{todays_date}</p>"

    html += f"<h4>Housing Information for {user_state}</h4>"
    html += "<ul>"
    
    html += "</ul>"

    send_email(subject="[FRED Briefing] My Housing Report", html=html)