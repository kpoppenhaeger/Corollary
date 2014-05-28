

source sasvariables.csh

# source coords.csh

# make regions with ds9 and save them before running this.

setenv source `grep circle source.reg`
setenv bg `grep circle bg.reg`

setenv bin 1000

# Create lightcurves (all data/full region; select energy range, region, timebins etc. !!!)

setenv e1 200
setenv e2 3000
setenv e3 800

evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lca.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e1}:${e2}]) && ((X,Y) IN $source )"
evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lcabg.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e1}:${e2}]) && ((X,Y) IN $bg )" 

evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lca_s.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e1}:${e3}]) && ((X,Y) IN $source )"
evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lcabg_s.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e1}:${e3}]) && ((X,Y) IN $bg )" 

evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lca_h.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e3}:${e2}]) && ((X,Y) IN $source )"
evselect table=pn_barycenter.fits withrateset=yes rateset=pn_bary_lcabg_h.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=${bin} expression="(FLAG==0) && (PATTERN<=4) && (PI in [${e3}:${e2}]) && ((X,Y) IN $bg )" 





