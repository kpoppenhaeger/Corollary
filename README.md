Corollary
=========

Some analysis scripts for some observations.

What you will need:
- python 2.7.x
- matplotlib
- numpy
- scipy
- astropy
- XMM SAS (some reasonably recent version)

XMM scripts
===========

I have made some XMM SAS scripts to produce the initial data files. Those are for cshell; if you work in bash, you will need to make a modified version of those.

List of scripts, and order of steps:

- sasvariables.csh

to be copied into the working directory.

- EPIC_prepare.csh

extracts the data tar file, performs cifbuild, odfingest, em/epproc, and basic event file merging for a first look.

- EPIC_check.csh

checks for high background and makes clean event files (i.e. events with bad flags excluded); applies barycenter correction to event files.

- next step: define source and bg regions with ds9. I use 20 arcsec source regions and 60 arcsec bg regions.

- EPIC_pn_lc.csh

extracts pn light curves in a few bands.

- EPIC_extract_regions.csh

extracts source and bg counts from the defined regions, for all 3 EPIC detectors individually.


Python scripts
==============

- directories_etc_example.py

This contains some file and folder definitions. Make a copy of this file, put your paths in there, and save it as "directories_etc.py". The filename 'directories_etc.py' is in the .gitignore file, so that you don't accidentally overwrite other people's path settings when pushing/pulling stuff from the repository.

- running_the_analysis.py

This is the main script from which you can copy and paste into your ipython shell. 

- analysis.py

This contains the routines which are called in "running_the_analysis.py".