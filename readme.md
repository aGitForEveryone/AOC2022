# Advent of code 2022
This repository contains my solution attempts for advent of code 2022. Advent of
code is a yearly programming puzzle event happening in December. Every day, 
starting from December 1st and ending on December 25th, a puzzle is released.
It is free to participate, so if you want to try out yourself, 
visit [adventofcode.com](adventofcode.com), login with your favorite platform, 
and get started. 

# Install
Install this repositories dependencies with
```commandline
pip install -r requirements.txt
```

# Repository structure
The code for each puzzle is contained within it's own directory named `dayXX`.
The repository contains a setup script for quickly setting up the code for each
puzzle. You can call the code via the command line:
```commandline
python setup_new_day.py [day]
```
replace `[day]` by the day number for which the code should be initialized. 
Leave the day value empty to generate code for today's puzzle.

# Python package advent-of-code-data
My code uses the Python package 
[Advent of code data](https://pypi.org/project/advent-of-code-data/) for 
automatically downloading the user's input and submitting the calculated answer.
Please visit the library page on pypi.org for instructions on how to set it up 
for your system.