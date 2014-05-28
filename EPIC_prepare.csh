
heainit
startsas

source sasvariables.csh

mkdir odf
mv *.gz odf
cd odf
gunzip *.tar.gz
tar -xvf *.tar
tar -xvf *.TAR
rm *.tar
rm *.TAR
cd ..

cifbuild
odfingest outdir=$SAS_ODF odfdir=$SAS_ODF
emproc;epproc

mv *EMOS1*ImagingEvts.ds mos1.fits
mv *EMOS2*ImagingEvts.ds mos2.fits
mv *EPN*ImagingEvts.ds pn.fits

merge set1=mos1.fits set2=mos2.fits outset=mos.fits
merge set1=mos.fits set2=pn.fits outset=epic.fits


