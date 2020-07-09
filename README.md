
# Testing

Validation, manual unit, cross browser/cross device, travis, coverage, we roughed in a bit of testing.

# Validation Testing 
Various IDE's Pycharm VSCode and GitPod help do basic linter testing.

CSS Validator Note, any error associated with root: color variables were ignored.
HTML Validator - validation of HTML with Django is pretty useless as all {{}} bracketed values raise errors. I ran only a few files through the validator and instead relied heavily upon pycharm's IDE to identify mismatched tags and closing Django directives.
django-extensions - used for validating templates from the command line python manage.py validate_templates
JavaScript Validator Note any errors for let, variables set in other .js files, and constants were ignored. I also used a more ES6 friendly checker and there were no errors for main.js
Pycharm IDE - PyCharm has inline validation for many file types. Python, CSS, HTML, DJANGO files were continuously tested for validity when using this IDE.

## Unit Testing

As core functionality and features were delivered we manually executed test cases to ensure profiles were updated, families were udpated and status could be changed and posts could be created. Console logs were checked and only favicon 404 errors were checked in.

## Cross Browser/Cross Device Verification
Spot checking of our application was done across the following devices operating systems and screen sizes is as follows:

| DEVICE   | BROWSER | OS      | SCREEN WIDTH    |
|----------|---------|---------|-----------------|
| macbook  | firefox | Mojave  | HD 125-1240     |
| macbook  | safari  | Mojave  | HD 125-1240     |
| macbook  | chrome  | Mojave  | HD 125-1240     |
| motog6   | chrome  | android | XS 360px & less |
| iphoneSE | chrome  | iOs     | XS 360px & less |


## Python Testing
Tests were written for a couple of the accounts forms and views. 

Basic test framework has been installed using django-nose driver. To run tests execute the following command from the terminal window:
 
``` python manage.py test --noinput --settings ci_hackathon_july_2020.settings_test```

[django-nose](https://pypi.org/project/django-nose/) was used to help configure and run the python tests with coverage output.

To run these tests go to the command terminal and:

python manage.py test --noinput --settings ms4_challenger.settings_test
Generate a report coverage report
Generate the HTML coverage html
Open the newly created test_coverage directory in the root of your project folder.
Open the index.html file inside it.
Run the file in the browser to see the output.


## Travis 
Travis continuous integration testing with coverage was set up for this project to run the python tests mentioned above.

[![Build Status](https://travis-ci.org/maliahavlicek/ci_hackathon_july_2020.svg?branch=master)](https://travis-ci.org/maliahavlicek/ci_hackathon_july_2020)






## Changing CSS or JS files
Files stored in /static folders are hosted by AWS. if you make a change
you may not see it. 

If you are actively working on CSS or JS, to get your changes loaded to AWS you must run the following command:

```python manage.py collectstatic --settings ci_hackathon_july_2020.settings_collect_static```


so that changes will be collected to AWS. This way the deployment in heroku will then have access to the updates.

## Local Environment
### FIRST TIME LOCAL SETUP
1. Save a copy of the github repository located at https://github.com/maliahavlicek/ci_hackathon_july_2020.git by clicking the 'download.zip' button at the top of the page and extracting the zip file to your chosen folder. If you have Git installed on your system, you can clone the repository with the following command:
   ```bash
   $ git clone https://github.com/maliahavlicek/ci_hackathon_july_2020.git
   ```
1. Open your preferred IDE, then open a terminal session in the unzip folder or cd to the correct location.
1. Set up a virtual environment via this command in the terminal session:
   ```bash 
   python3 manage.py
   ``` 
   > NOTE: The ```python``` prefix of this command and other steps below assumes you are working with a mac and pycharm's IDE. Your command may differ, such as ```python -m .venv venv ...``` or ```py manage.py ...``` or ```.\manage.py ...```
1. Activate the .venv with the command:
   ```bash 
   .venv\Scripts\activate
   ```
   > Again this command may differ depending on your operating system, please check the Python Documentation on [virtual environments](https://docs.python.org/3/library/venv.html) for further instructions.
1. If needed, Upgrade pip locally with:
   ```bash
   pip install --upgrade pip
   ```
1. Install all required modules with the command:
   ```bash
   pip install -r requirements.txt
   ```
1. Create a new file at the base ms4_challenge directory level called env.py:
   ```python
   touch env.py
   ```
1. Copy the following into the env.py file:
    ```python
    import os
    
    os.environ.setdefault('HOSTNAME', '<your value>')
    os.environ.setdefault('SECRET_KEY', '<your value>')
    os.environ.setdefault('EMAIL_USER', '<your value>')
    os.environ.setdefault('EMAIL_PASS', '<your value>')
    ```
1. Replace <your value> with the values from your own accounts
    - HOSTNAME - should be the local address for the site when running within your own IDE.
    - SECRET_KEY -is a django key a long random string of bytes. For example, copy the output of this to your config: 
        ```bash
       python -c 'import os; print(os.urandom(16))'
        ```
1. Set up the databases by running the following management command in your terminal:
    ```bash
    python manage.py migrate
    ```
1. Create the superuser so you can have access to the django admin, follow the steps necessary to set up the username, email and password by running the following management command in your terminal:
    ```bash
    python manage.py createsuperuser
    ```
1. Start your server by running the following management command in your terminal:
    ```bash
    python manage.py runserver
    ```
1. if using gitpod, update settings.py to include 'localhost' in the ALLOWED_HOSTS

### After Initial Setup
1. Pull or fetch data from branch or master
1. ```pip install -r requirements.txt```
1. ```python manage.py makemigrations``` 
1. ```python manage.py migrate```




## Notes

Google recently updated security policies. Now you have to do two things after setting up an app specific email via gmail. First log out of all gmail accounts and log into the one you are going to use for your application then hit these two URLS:
1) [turn off captcha](https://accounts.google.com/displayunlockcaptcha)
2) [less secure settings](https://myaccount.google.com/lesssecureapps?pli=1) 
