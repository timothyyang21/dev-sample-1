
# The Maze Challenge Graphics

![alt text](https://github.com/timothyyang21/dev-sample-1/resources/demo_pic.png)

Author: Timothy Yang
Date: October 2019

## Build Instructions

### Build Maze Graphics Program
To build and run the maze_graphics.py program, one needs to first download python 3.6 and the download pygame module

#### Windows
To see which version of Python 3 you have installed, open a command prompt and run

$ python3 --version
One can install python3.6 through Ubuntu

``` $ sudo apt-get update ```
``` $ sudo apt-get install python3.6 ```
If installation can't be done through the above command, go to python.org and install the appropriate version https://www.python.org/downloads/release/python-360/

After installing python, ones need to install the pygame module through pip

First, update the pip installer

``` $ python -m pip install --upgrade pip ```
If one does not have the pip installer installed (when installing python 3.6), one can install pip using the following command:

``` $ sudo apt update ```
``` $ sudo apt install python3-pip ```
Once the installation is complete, verify the installation by checking the pip version:

``` $ pip3 --version ```
Then, install pygame with

``` $ python -m pip install pygame ```
Pygame should be installed and now, import pygame should work.

Make sure that your python environment is using python 3.6 and that your pygame is installed for python 3.6. One easy way to check if pygame is installed for your python 3.6 is through

"Default Preferences" -> "Project Interpreter" 
If for some reason pygame isn't there, you can simply go to the lower left corner's + sign and install pygame package there.

One would also need to install pathlib2 for the maze_graphics.py program.

``` $ python -m pip install pathlib2 ```

#### Mac OS
Install brew , using these instructions in this website:

https://brew.sh/index.html

This is a package manager capable of installing all sorts of programs.

If you need Python 3 installed:

``` $ brew install python3 ```
Link applications to Python3:

``` $ brew linkapps python3 ```
Install pygame Dependencies:

``` $ brew install --with-python3 sdl sdl_image sdl_mixer sdl_ttf portmidi ```
Install pygame:

``` $ pip3 install pygame ```
Install pathlib2:

``` $ pip3 install pathlib2 ```

## Run Instructions

### Run Maze Graphics Program
Run the following command:

``` $ python programs/maze_graphics.py log_file resource_dir fancy_or_not ```
log_file is required and should be a log file produced by client-init program
resource_dir is required and should be a log file that includes all the resource needed to run the maze_graphics.py program
fancy_or_not is required and it's either 0 or 1, 0 means just the normal version, 1 means the fancy version that includes block walls and bread crumbs
For example:

``` $ python maze_graphics.py maze_taiwana_10_2.log resources 0 ```
To run an in-built example, use make graphics.

One might need to type python3 instead of python in the command run if one did not alias python as python3

## Assumptions

The maze_graphics.py assumes one has the log file that's been produced by the maze-solving program, and it assumes one has the right python environment to run the code.

## Limitations

The maze_graphics.py program works best when the maze is relatively small, bigger maze makes the graphics hard to see and takes more time to solve.

