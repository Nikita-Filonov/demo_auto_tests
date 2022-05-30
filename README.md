Core autotests
================

Setup git
---------
**Git config**

1. Open terminal
2. `git config --global user.name "your_gitlab_name"`
3. `git config --global user.email "your_gitlab_email@mail.ru"`

**Add your shh keys to gitlab**

1. `ssh-keygen -t rsa -b 4096 -C "you@computer-name"`

2. Copy your public key and add it to your GitLab profile

`cat ~/.ssh/id_rsa.pub`

Example output

`ssh-rsa AAAAB3NzaC1yc2EAAAADAQEL17Ufacg8cDhlQMS5NhV8z3GHZdhCrZbl4gz you@example.com`

Download autotests
---------
`git clone https://gitlab.alemira.dev/platform/alms/core.git`

either

`git clone git@gitlab.alemira.dev:platform/alms/core.git`

Activating the virtual environment
--------

MacOS
______

``` 
mkdir environments

cd environments

python3 -m venv selenium_env

source selenium_env/bin/activate
``` 

Ubuntu
______

``` 
sudo apt-get update && sudo apt-get upgrade

sudo apt-get install python3.7

python3 -m pip install pip

sudo apt-get install -y python3.7-venv

mkdir environments

cd environments

python3 -m venv selenium_env

source selenium_env/bin/activate
``` 

Windows
______

``` 
mkdir environments

cd environments

python -m venv selenium_env

selenium_env\Scripts\activate.bat
```

Installing dependencies
---------

```
/bin/bash ./infrastructure/setup.sh
``` 

Or

```
cd ./infrastructure
/bin/bash setup.sh
```

It will install public requirements and then install requirements from private nexus

Installing chromedriver
---------
MacOS
______

``` 
brew install wget
```

To install the driver, open the site
https://sites.google.com/a/chromium.org/chromedriver/downloads
and copy the link to that version of ChromeDriver, which matches the version of your browser. To check your browser
version, open a new window in Chrome, in the search bar type: chrome: // version / - and press Enter. In the top line
you will see information about the browser version.

``` 
cd ~/Downloads

wget https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_mac64.zip

unzip chromedriver_mac64.zip

sudo mv chromedriver /usr/local/bin
```

Let's check that the correct version of chromedriver is installed.

``` 
chromedriver --version
```

Warning! If after installing chrome driver you're getting alert like
"The chromedriver application cannot be opened because the developer could not be verified.", then follow steps below

```
where chromedriver 
```

Will output something like `/usr/local/bin/chromedriver`, copy this path and

```
cd /usr/local/bin

xattr -d com.apple.quarantine chromedriver 
```

After that `chromedriver` should work fine

Ubuntu
______
Installing ChromeDriver using commands in the terminal. We will indicate the version of ChromeDriver we need to
download. To get the link, go to the version you need in your browser driver by link to
https://sites.google.com/a/chromium.org/chromedriver/downloads. On the page that opens, click on the file for Linux with
the right button and copy the path to the file. Replace in the example below file path for wget command with your link:

``` 
wget https://chromedriver.storage.googleapis.com/76.0.3809.126/chromedriver_linux64.zip

unzip chromedriver_linux64.zip
```

Move the unzipped file from the ChromeDriver to the desired folder and allow to run chromedriver as executable:

``` 
sudo mv chromedriver /usr/local/bin/chromedriver

sudo chown root:root /usr/local/bin/chromedriver

sudo chmod +x /usr/local/bin/chromedriver
```

Check that chromedriver is available, by running the chromedriver command in the terminal, you should get a message that
the process has started successfully.

Windows
______
To install, open the site
https://sites.google.com/a/chromium.org/chromedriver/downloads and download the version of ChromeDriver that matches the
version your browser. To check your browser version, open a new one window in Chrome, in the search bar type: chrome: //
version / and press Enter. In the top line you will see information about browser version.

Download from the site
https://sites.google.com/a/chromium.org/chromedriver/downloads
driver for your browser version. Unzip the downloaded file. Create a chromedriver folder on the C: drive and put the
unzipped previously the chromedriver.exe file in the C: \ chromedriver folder. Add the C: \ chromedriver folder to the
PATH system variable. How to do it in different Windows versions, oh written
here: https://www.computerhope.com/issues/ch000549.htm.

To check the contents of the path variables, on the command line, run command

``` 
path
```

Run tests locally
---------

First look at ```setting.py``` file and change following settings:

```python
DEBUG = True

DATABASE_LOGGING = True  # if you want to see sql queries

RERUNS = 3  # optionally you can set to 0, if you dont want retries
````

----

Then start autotests with following command (synchronously):

```
pytest
```

(asynchronously)

```
pytest -n auto
```

If you want to run certain scope of autotests then use marks:

```
pytest -m "api" <- will run only "api" autotests

pytest -m "api or learner_ui" <- will run "api" and "learner_ui" autotests

pytest -m "api and not users" <- will run all "api" autotests and exclude "users"
```

All available markers can be viewed in ```pytest.ini``` file

----

To start autotests of specific `class`

```
pytest -k "TestActivitiesApi"
```

Where `TestActivitiesApi` is a class name. Or for few classes

```
pytest -k "TestActivitiesApi or TestDataGridSettingsApi"
```

----
To start specific/single autotest

```
pytest ./tests/api/users/activities/test_activities.py::TestActivitiesApi::test_get_activities
```

Where:

- `./tests/api/users/activities/` - path to python module
- `test_activities.py` - python module
- `TestActivitiesApi` - class we want to select
- `test_get_activities` - specific test we want to select

----

Start autotests of specific module

```
pytest ./tests/api/users/activities/test_activities.py <- path to that module
```

----

Start autotests of specific folder

```
pytest tests/api/users/ <- folder where we want to run our tests
```
