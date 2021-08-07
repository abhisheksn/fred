# fred

This Python application enables investors and home buyers to get updates on medium home prices in different states in the U.S. 

Prerequisites

Anaconda 3.7+
Python 3.7+
Pip
Installation

Fork this remote repository under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

cd ~GitHub/fred
You can also navigate to the directory by clicking "Repository" and "Open in Terminal" from GitHub Desktop upon dowloading the copy of the application.

Use Anaconda to create and activate a new virtual environment, perhaps called "fred-env":

conda create -n fred-env python=3.8
conda activate fred-env
After activating the virtual environment, install package dependencies (see the "requirements.txt" file):

pip install -r requirements.txt
NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial cd step above).
Setup

In the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to specify your desired username (then make sure to SAVE the ".env" file aftwards):

Get your own free API key from https://research.stlouisfed.org/useraccount/apikeys and input it below in .env. 

api_key="Your API key"

NOTE: the ".env" file is usually the place for passing configuration options and secret credentials, so as a best practice we don't upload this file to version control (which is accomplished via a corresponding entry in the ".gitignore" file). This means we need to instruct each person who uses our code needs to create their own local ".env" file. 

The ".gitignore" file generated during the GitHub repo creation process should already do this, otherwise you can create your own ".gitignore" file and place inside the following contents:

#this is the ".gitignore" file

#ignore secret environment variable values in the ".env" file:
.env

Ensure to create .env file before creating .gitignore file.

Usage

Run the Python script:

python fred.py

# alternative module-style invocation (only required if importing from one file to another):
python -m fred.py
NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the pip command above to ensure that package has been installed into the virtual environment.