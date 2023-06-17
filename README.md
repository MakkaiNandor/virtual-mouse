# Hand Gesture Controlled Virtual Mouse Application

## Requirements

The application requires `Python 3.8+` and `pip 19.3+`.

You can download the right Python version from [here](https://www.python.org/). Python version above 3.4 includes the `pip` as well.

You can check the Python and pip version by the following command:

  - Windows: `pip -V`
  - MacOS: `pip3 -V`

Make sure that your `pip` version is up-to-date. If don't, use the following command to update: `python -m pip install --upgrade pip`

The application also requires many other Python packages, which are listed in the `requirements.txt` file.

The application was tested on Windonws 10 and MacOS Ventura operating systems.

## How to use

### Step 1: Create a virtual environment

For virtual environment you can use the [`virtualenv`](https://pypi.org/project/virtualenv/) Python package. Install the package with this command:

  - Windows: `pip install virtualenv`
  - MacOS: `pip3 install virtualenv`

Create the virtual environment with the command `virtualenv <path-to-directory>` and enter in the directory.

Activate the virtual environment:

  - Windows: `Scripts/activate.bat`
  - MacOS: `source bin/activate`

### Step 2: Clone the git repository

Clone the repository with this command `git clone https://github.com/MakkaiNandor/virtual-mouse.git <path-to-directory>` and enter in the directory.

### Step 3: Install dependencies

The `requirements.txt` contains the Python packages which are required for the application to run. You can install all of these packages whit this command:

  - Windows: `pip install -r requirements.txt`
  - MacOS: `pip3 install -r requirements.txt`

Now you can run the application:

  - Windows: `python app.py`
  - MacOS: `python3 app.py`