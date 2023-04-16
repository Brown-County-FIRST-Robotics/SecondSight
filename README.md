# SecondSight

A computer vision project for FRC teams. The intention of this project is to lower the difficulty of AprilTag and object detection using off the shelf cameras and single board computers.

# Getting Started

To get started, set up a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

We use `poetry` to manage our dependencies (as opposed to `pip`), so install that:

```
pip install poetry
```

To start the server, run:

```
poetry install
poetry run second-sight
```

Which will spit out a URL you can visit to verify the system is working.

# Contributing
Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute and configuring your Python environment. SecondSight uses Poetry to manage dependencies and builds, VS Code works well as the editor.
