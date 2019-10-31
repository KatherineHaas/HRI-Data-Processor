# HRI-Data-Processor
A program that takes raw data and returns useful metrics

This program takes in a large quantity of raw data and produces several useful metrics(mean, median, mode, range, etc.). It also produces a 3D graph and a 2D graph based off of the XYZ and XY components respectively. The densest portion of the 2D graph is highlighted for your convenience.

The program asks the user whether they would like to analyze everything or if they would like to analyze a single metric from some data file(s). The latter portion of the program requires the name of the folder the data is in, what the file is called, and which metric should be analyzed. Keywords are included in the program for special functions. Using the default setting, the program only requires the folder that the data is in.

Notes: This program is case sensitive. This program runs with the following modules: csv, pandas, glob, os, math, statistics, mpl_toolkits(mplot3d), numpy, matplotlib.pyplot, and matplotlib.patches(Rectangle).

