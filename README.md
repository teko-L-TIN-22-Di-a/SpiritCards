# SpiritCards

A school project authored by Benny Schärer and Celin Villars.

## Project Setup

The initial Project setup is done but it is still missing a lot of parts that may or may not be added in the future. Some Points:
- Add proper makefile support?
- Test and or configure proper pyproject.toml

> ! This setup guide is targeted towards windows.

Install a python version below '3.12' because of Nuitka compatibility issues. (Best use [3.11.8](https://www.python.org/downloads/release/python-3118/))

Setup venv

```
py -m venv
```

Install all dependencies

```
py -m pip install -r requirements.txt
```

## Local development

```
py run.py
```

## Build for distribution

At the moment there is only a batch script that builds the app into the "run.dist" folder using the Nuitka builder.
Nuitka compiles and builds the python project into a ".exe" file.
For the build to be successful the script copies the "assets" folder and all its contents into the "run.dist" folder.

```
start build.cmd
```
