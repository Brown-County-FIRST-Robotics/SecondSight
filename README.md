TEST

# SecondSight

A computer vision project for FRC teams.

# Getting started
You should create a python virtual environment as we will need some specific dependencies and versions

To create a python virtual environment ensure you have the 'venv' python module installed. For example on Ubuntu you would run `sudo apt-get install -y python3-venv` to install this module.

Then run

```shell
python -m venv secondsight_env
source secondsight_env/bin/activate
```

# Poetry build environment
This project uses Poetry for dependency management and building. To install poetry run `pip install poetry`

# Running the system
To test things out, you can run `poetry run second-sight` which will spit out a URL you can visit to verify the system is working.
