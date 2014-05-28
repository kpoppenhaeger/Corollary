

source sasvariables.csh

# make regions with ds9 and save them before running this.

setenv source `grep circle source.reg`
setenv bg `grep circle bg.reg`

# extract source counts and bg counts from regions

evselect table=mos1_barycenter.fits withfilteredset=true filteredset=mos1_barycenter_src.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12) && ((X,Y) IN $source) )"
evselect table=mos1_barycenter.fits withfilteredset=true filteredset=mos1_barycenter_bg.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12) && ((X,Y) IN $bg) )"

evselect table=mos2_barycenter.fits withfilteredset=true filteredset=mos2_barycenter_src.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12) && ((X,Y) IN $source) )"
evselect table=mos2_barycenter.fits withfilteredset=true filteredset=mos2_barycenter_bg.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EM && (PI in [200:10000]) && (PATTERN<=12) && ((X,Y) IN $bg) )"

evselect table=pn_barycenter.fits withfilteredset=true filteredset=pn_barycenter_src.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EP && (PI in [200:10000]) && (PATTERN<=4) && ((X,Y) IN $source) )"
evselect table=pn_barycenter.fits withfilteredset=true filteredset=pn_barycenter_bg.fits keepfilteroutput=true destruct=yes expression="(#XMMEA_EP && (PI in [200:10000]) && (PATTERN<=4) && ((X,Y) IN $bg) )"







