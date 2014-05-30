# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from astropy.table import Table

# the actual analysis functions are imported through this:

import analysis as ana

# names of a variety of files and directories are imported through this:

from directories_etc import *

# when not using all observations:
folders_nonflare = np.array([
'0720173001',
'0720173101',
'0720173201',
'0720173301',
'0720173401',
#'0720173501',
'0720173601',
'0720173701',
'0720173801',
'0720173901',
'0720174001',
'0720174101',
'0720174201',
#'0720174301',
'0720174401',
])


#########################
# ANALYSIS STARTS HERE
#########################

# calculate the bg-subtracted light curves for pn in full/soft/hard band:
phases, rates, errors = ana.make_pn_bgsub_lcs(folders=folders, path=path, pn_lc=pn_lc, pn_lcbg=pn_lcbg)
phases_s, rates_s, errors_s = ana.make_pn_bgsub_lcs(folders=folders, path=path, pn_lc=pn_lc_s, pn_lcbg=pn_lcbg_s )
phases_h, rates_h, errors_h = ana.make_pn_bgsub_lcs(folders=folders, path=path, pn_lc=pn_lc_h, pn_lcbg=pn_lcbg_h )

# plot the pn full band light curves nicely:
ana.plot_pn_bgsub_lcs(phases, rates, errors)

# plot the pn three band light curves nicely:
ana.plot_pn_bgsub_lcs_3bands(phases, rates, errors, phases_s, rates_s, errors_s, phases_h, rates_h, errors_h)


# create new event files for source and bg region where the arrival times of the phtoons are expressed in orbital phase:
ana.make_new_fits_with_phase(folders=folders, instrument='pn')
ana.make_new_fits_with_phase(folders=folders, instrument='mos1')
ana.make_new_fits_with_phase(folders=folders, instrument='mos2')


# calculate the added-up count rate in and out of transit:

#result = make_count_rate_comparison(folders=folders, energy_low=200, energy_high=2000)
result = ana.make_count_rate_comparison(folders=folders_nonflare, energy_low=500, energy_high=5000)

phaserate_out = (result['counts_out_tr_src'].sum() - result['counts_out_tr_bg'].sum()*bgfactor) / result['phase_out_tr'].sum()
phaserate_in = (result['counts_in_tr_src'].sum() - result['counts_in_tr_bg'].sum()*bgfactor) / result['phase_in_tr'].sum()

rate_out = phaserate_out/period
rate_in = phaserate_in/period

print rate_out, rate_in
print rate_in/rate_out


# calculate normalization factors for each observation to make out-of transit count rate unity:
# rate * norm_factors = normalized rate

norm_factors = ana.calc_norm_factors(folders=folders, instrument='pn', energy_low=200, energy_high=2000)


# now make the co-added light curve.

phase_grid = np.arange(0.70, 1.3, 0.005)

(counts_src, counts_bg, fullness) = ana.make_total_lc(phase_grid, norm_factors, folders=folders_nonflare, instrument='pn', energy_low=200, energy_high=2000)

norms = np.ones([len(folders_nonflare), len(phase_grid) - 1])
for i in np.arange(0, len(folders_nonflare)):
  norms[i,:] = norm_factors[i]

y = ((counts_src-bgfactor*counts_bg)*norms).sum(axis=0)/fullness.sum(axis=0)
x = (phase_grid[0:-1] + phase_grid[1:])/2.

good = fullness.sum(axis=0) > 9.

plt.figrue()
plt.plot(x[good], y[good])


# this still needs error bars etc.






