# Hyperbolic
Flask implementation of hyperbola

## How it Works

Hyperbola contains the code that actually does the "hacking". It contains all the code to analyze files, connect to platforms like CTFD.io, and run Linux commands on files. Flask acts as an API for Hyperbola. All the commands that can be done in Hyperbola can be requested from Flask which then returns the output as a JSON. Client is a Vue server that acts as the interface between the Flask API and end users. It takes the JSON output and uses it to display pages all as a single-page application (SPA).

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

### Client

Prerequisites:

- Install node.js
- Install NPM

Installation:

1. `cd` to the `client` directory
2. Run `npm install` to install the needed NPM packages
3. Run the Vue server from the client directory with the command `npm run serve`
