# Real Estate Investment Recommendation App

This Python application provides real estate investment recommendations based on five different macroeconomic indicators:

  + Median Household Income
  + Median House Listing Price
  + State GDP
  + State Unemployment Rate
  + Resident Population of the state.

The data is obtained by hitting the API endpoints of the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/).

There are two versions of the engine
  + <b>Free</b>: In this version, the user can enter the State ID to get the latest median house price in a state and also the investment recommendation based on our algorithm. This version can also be accessed through our [web app](https://agy-consultants.herokuapp.com/)

  + <b>Premium</b>: In this version, a report is generated with detailed information on all 50 states. Our recommendation for each state is also available. The report will be emailed to the user as a .csv file, for a small fee. An interactive choropleth map is also generated from the report data.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](https://github.com/abhisheksn/fred) under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```
cd ~/Desktop/fred
```

## Create Environment
Use Anaconda to create and activate a new virtual environment, perhaps called "fred-env":

```
conda create -n fred-env python=3.8 #(first time only)
```
```
conda activate fred-env
```

## Install Packages
After activating the virtual environment, install package dependencies (see the ["requirements.txt"](/requirements.txt) file):

```
pip install -r requirements.txt
```

## Setup
In the root directory of your local repository, create a new file called ".env". Obtain the [API credentials](https://fred.stlouisfed.org/docs/api/api_key.html) to access the FRED database and include it in the contents of the ".env" file. You can also include the SendGrid API credentials in the same ".env" file:

```
#this is the .env file
#FRED API KEY
FRED_API_KEY=______________________ #(this is not a string)
```

```
#this is the .env file
#SENDGRID EMAIL Credentials
SENDGRID_API_KEY= "_________________"
SENDER_EMAIL= "________________"
```

> NOTE: the ".env" file is usually the place for passing configuration options and secret credentials, so as a best practice we don't upload this file to version control (which is accomplished via a corresponding entry in the [".gitignore"](/.gitignore) file). This means each person who uses our code needs to create their own local ".env" file.

> NOTE:Follow these [SendGrid setup instructions](https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/sendgrid.md#setup) to sign up for a SendGrid account, configure your account's email address (i.e. `SENDER_EMAIL`), and obtain an API key (i.e. `SENDGRID_API_KEY`)

## Run Python Script

### Free version
```
python -m  app.fred
```

### Premium version
```
python -m  app.fred_premium
```

> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment

## User input

### Free version
In the free version, the user needs to input a 2 letter state abbreviation code to obtain the median listing price and our investment recommendation for the State.

### Premium version
In the premium version, the user will be asked to input an email address to receive the country report.


## WEB-APP
The web-app can be accessed at [agy-consultants.herokuapp.com](https://agy-consultants.herokuapp.com/).

This app was created by [Yanjka Regan](https://github.com/yr999), [Grigory Patsera](https://github.com/gbacila) and [Abhishek Swaminathan](https://github.com/abhisheksn).
