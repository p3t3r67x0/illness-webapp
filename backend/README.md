Illness WebApp README
---------------------

## Installation and Setup

### git clone as always

### Install pipenv globally e.g.

    pip3 install pipenv

###. Install project dependencies. pipenv takes care of creating the virtualenv for you - omit the `--dev` flag for installations in production environments    
    
    pipenv install --dev --python python3.7
    
There is a bug in pipenv (and OSX?). In case the command above fails and complains about: 

    "FileNotFoundError: [Errno 2] No such file or directory: '/usr/local/bin/pythonz': '/usr/local/bin/pythonz'"
    
use this command instead:

    pipenv install --dev --python `which python3.7`
    
### Activate the created virtualenv

    pipenv shell

### Copy illness/.env.example to illness/.env and adjust the settings

    cp illness/.env.example illness/.env

### Init the Database

    ./manage.py migrate
    
### Enable pre-commit git hook
    
    pre-commit install 
