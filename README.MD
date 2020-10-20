# **Server Side For Simple Multiplayer Online Games:**
## (This template is for: Tic-Tac-Toe) 
---
## **GETTING STARTED**:
### **1. Pipenv**
This project utilizes [pipenv 2020.8.13](https://pypi.org/project/pipenv/) for managing its packages, so go to pypi.org for more informations or install it using the command:
> pip install pipenv

If you or your team are using virtualenv with 'requirements.txt', after pipenv installation, you can easily update your packages with:
> pipenv install -r ./requirements.txt

The first time you run pipenv, an virtual environment will be created, and you can simply access it using:
>pipenv shell

*This will have the same effect as 'source venv/bin/activate.bat'*

If you want to check where the virtual environment is beeing stored, you can run the command for venv information:
> pipenv --venv

Or, inside pipen shell, use sys.executable to print path:

```shell
$ pipenv shell
Launching subshell in virtual environment…

$ python
Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:43:08) [MSC v.1926 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.executable
'C:\\Users\\Snades\\Envs\\tic-tac-toe-backend-rOhMoS9H\\Scripts\\python.exe'
>>>
```

For returning to your previous environment, type:
>exit

*This will have the same effect as 'deactivate' inside virtualenv*

After that, for update your project for production, it is a good practice to ignore Pipfile at the expense of Pipfile.lock, wich has all the versions and hashes specified. In this case, you won't have any issues with outdated dependencies, and anyone can easily clone your repository and reproduce this template. That said, run the lock command and ignore de Pipfile versions:

> pipenv install --ignore-pipfile

### **2. Env Variables**
In the case of having to use environment variables, let's say, to get an API key or to link to you Local or Remote Database, just create a new file in your root directory named '.env'. In .env, create any variables you'd like, for instance:
```env
DB_USERNAME="User123"
DB_PASSWORD="passwd123456"
``` 
In Python, you have to import 'os' module to acces env variables, calling 'os.environ['ENV_VARIABLE_NAME']

For example:
```shell
$ pipenv run python
Loading .env environment variables…
Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:43:08) [MSC v.1926 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.environ['DB_USERNAME']
'User123'
>>> os.environ['DB_PASSWORD']
'passwd123456'
>>> 
```
*P.S.: Remember to add the .env file to your .gitignore*

### **3) Customizing your games:**

