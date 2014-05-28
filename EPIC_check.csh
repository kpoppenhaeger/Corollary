

source sasvariables.csh

# Check for high background

evselect table=mos1.fits withrateset=true rateset=mos1_he_lc.fits makeratecolumn=yes timecolumn=TIME timebinsize=100 maketimecolumn=yes expression="#XMMEA_EM && (PI>10000) && (PATTERN==0)"
evselect table=mos2.fits withrateset=true rateset=mos2_he_lc.fits makeratecolumn=yes timecolumn=TIME timebinsize=100 maketimecolumn=yes expression="#XMMEA_EM && (PI>10000) && (PATTERN==0)"
evselect table=pn.fits withrateset=true rateset=pn_he_lc2.fits makeratecolumn=yes timecolumn=TIME timebinsize=100 maketimecolumn=yes expression="#XMMEA_EP && (PI in [10000:12000]) && (PATTERN==0)"

# Filter eventfile; no gti filtering because we want light curves in the end. But filter out events with bad flags.

evselect table=mos1.fits withfilteredset=true filteredset=mos1_clean.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12))"
evselect table=mos2.fits withfilteredset=true filteredset=mos2_clean.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12))"
evselect table=pn.fits withfilteredset=true filteredset=pn_clean.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EP && (PI in [200:10000]) && (PATTERN<=4))"

# merge clean files:

merge set1=mos1_clean.fits set2=mos2_clean.fits outset=mos_clean.fits
merge set1=mos_clean.fits set2=pn_clean.fits outset=epic_clean.fits


# apply barycentric correction to event files:

cp epic_clean.fits epic_barycenter.fits
barycen table=epic_barycenter.fits:

cp pn_clean.fits pn_barycenter.fits
barycen table=pn_barycenter.fits:

cp mos1_clean.fits mos1_barycenter.fits
barycen table=mos1_barycenter.fits:

cp mos2_clean.fits mos2_barycenter.fits
barycen table=mos2_barycenter.fits:







