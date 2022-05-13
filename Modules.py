#Modules Needed 
import os
import PyQt5
from PyQt5 import QtWidgets, uic,QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot, exporters
import sys
import numpy as np
import math 
import statistics as stats
import matplotlib.pyplot as plotting
import scipy as sp
from scipy import stats
from time import sleep 
import warnings


import rpy2

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector


#### SET HOME DIRECTORY OF FILES IN BETWEEN QUOTATIONS ###
home_file_dir = r""




base = importr('base')
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1)


utils.install_packages("rjags")
jags = rpackages.importr("rjags")

utils.install_packages("HDInterval")
hdi = rpackages.importr("HDInterval")

import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()


project_directory = os.getcwd()

icondir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Icons", "")

icondir=(project_directory+"/Icons/")
os.chdir(project_directory)

