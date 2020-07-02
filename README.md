# basic Django App with Login and Registration

## Local
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