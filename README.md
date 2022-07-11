# Hyperbolic
Beginner CTF automation with a pretty interface.

*Note: this project crashed and burned*

## How it Works

Hyperbola contains the code that actually does the "hacking". It contains all the code to analyze files, connect to platforms like CTFD.io, and run Linux commands on files. Flask is the web interface to run Hyperbola functions.

## Setup

### Hyperbola

No setup needed thus far.

### Flask

Prerequisites:

- Install Python

Installation:

1. `cd` to the project root directory
2. Create a virtual environment with the command `python -m venv .venv`
3. Activate the virtual environment with the command format `.venv\Scripts\activate` (Windows)
4. Install needed Python packages with the command `pip install -r requirements.txt`
5. Add the following environment variables with the command `$Env:VARIABLE_NAME = 'Value'`
   - `SQL_URI` - set to `'sqlite:///site.db'` to use a SQLite database
   - `EMAIL_USER`
   - `EMAIL_PASSWORD`
   - `SECRET_KEY` - generate in Python shell with the following commands
      1. `python` - open Python shell
      2. `import secrets`
      3. `secrets.token_urlsafe(24)` - generate token
      4. Use output as secret key
6. Run the Flask server from the project root with the command command `python run.py`
