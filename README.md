# CSC 450 - Team Project
## Team Members

Max Roen

Scott Gere

Timothy Hamilton

David Williams

Nick Perfetuo

# Setup Instructions!
* Clone the project
* setup a virtual environment so you don't overwrite your global python installs:
  * python -m venv $venv_name
  * Then, on mac or linux:
    * . $venv_name/bin/activate
  * Or on windows:
    * $venv_name\Setup\Activate
* pip install -r requirements.txt  
* Install pgadmin (so you have a local postgres database to work with -- https://www.pgadmin.org/download/)
* flask run
  * If you receive an error about missing packages, restart your terminal, it should fix it. I'm not sure which config file needs to be sourced, I'll update this step later once i figure it out.  
* Configuration currently relies on some environment variables being set, see config.py in the root directory  
  export SSBM_SECRET_KEY -> The password your chose for Postgres during install  
  export SSBM_DB_PORT_NUMBER -> Port your local DB is running on (5433 is the default for Postgres15)  
  export MAIL_SERVER=smtp.supersickbracketmaker.tech  
  export MAIL_PORT=587  
  export MAIL_USE_TLS=1  
  export MAIL_USERNAME=support@supersickbracketmaker.tech  
  export MAIL_PASSWORD=jpk7bfb-ben1HDR-kay

* Selenium Tests Setup
  You will need to have chrome/chromium installed.

  Download and install the ChromeDriver version for your version of Chrome.
  * Linux: sudo apt install chromedriver
  * Windows: https://chromedriver.chromium.org/home
  * Mac: https://chromedriver.chromium.org/home

  Export the following enviroment variable
  export SEL_PATH -> The path to the chrome driver exectuable

  Note: You may need to rerun 'pip install -r requirments.txt' to get the new packages.
