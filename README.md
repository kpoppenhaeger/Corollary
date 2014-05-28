Corollary
=========

Some analysis scripts for some observations

============
XMM scripts
============

I have made some XMM SAS scripts to produce the initial data files. Those are for cshell; if you work in bash, you will need to make a modified version of those.

List of scripts, and order of steps:

- sasvariables.csh

to be copied into the working directory.

- EPIC_prepare.csh

extracts the data tar file, performs cifbuild, odfingest, em/epproc, and basic event file merging for a first look.

- EPIC_check.csh

checks for hugh background and makes clean event files (i.e. events with bad flags excluded); applies barycenter correction to event files.

- next step: define source and bg regions with ds9. I use 20 arcsec source regions and 60 arcsec bg regions.

- EPIC_pn_lc.csh

extracts pn light curves in a few bands.

- EPIC_extract_regions.csh

extracts source and bg counts from the defined regions, for all 3 EPIC detectors.
