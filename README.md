# Trinity
To install Trinity, first download the repository off of GitHub. Once downloaded, enter the directory of the folder containing it and run the command
"pip install -r requirements.txt" (you may need to replace "pip" with "pip3"
depending on your OS). This will install all the packages needed to run the
GUI. For this to work properly, you will need to have the program R installed
on your computer, as well as the package JAGS.

For users with a Mac opertating system, you will need a gcc compiler installed in order for the RPy2 package to be installed. To download RPy2 utilizing this compiler, insert the command "env CC=/usr/local/Cellar/gcc/X.x.x/bin/gcc-X pip install rpy2" into your command line, replacing X.x.x with the current version of gcc you are using. 

To run Trinity, first enter the directory of the folder containing it. Once you
have entered this directory, run the file called “Spectrum GUI.py”.

More information on using Trinity can be found in the TrinityInformation.pdf file located in the repository.
