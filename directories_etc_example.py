# -*- coding: utf-8 -*-

import numpy as np

# path to where the XMM data is located.
# this is supposed to be the parent folder, with the individual observations folders (/072xxxyyyy/) inside that folder.

path = '/your/path/to/the/XMM/data/' # don't forget the "/" at the end

# define folders of individual observations:
folders = np.array([
'0720173001',
'0720173101',
'0720173201',
'0720173301',
'0720173401',
'0720173501',
'0720173601',
'0720173701',
'0720173801',
'0720173901',
'0720174001',
'0720174101',
'0720174201',
'0720174301',
'0720174401',
])

# plotting directory:

plotdir = '/your/path/to/where/you/want/your/plots/to/be/saved/' # don't forget the "/" at the end

#define file names for the event files and pre-extracted light curves
mos1_src = 'mos1_barycenter_src.fits'
mos2_src = 'mos2_barycenter_src.fits'
pn_src = 'pn_barycenter_src.fits'

mos1_bg = 'mos1_barycenter_bg.fits'
mos2_bg = 'mos2_barycenter_bg.fits'
pn_bg = 'pn_barycenter_bg.fits'

pn_lc = 'pn_bary_lca.fits'
pn_lcbg = 'pn_bary_lcabg.fits'

pn_lc_s = 'pn_bary_lca_s.fits'
pn_lcbg_s = 'pn_bary_lcabg_s.fits'
pn_lc_h = 'pn_bary_lca_h.fits'
pn_lcbg_h = 'pn_bary_lcabg_h.fits'


# define scaling factor from bg to source; i.e. bgfactor * bg_area = source_area
bgfactor = 20.**2/60.**2

# define expected transit times and period
# from http://exoplanets.org
t_transit_jd = 2454237.53556 # in JD
t_transit_xmm = 295750337.568 # in seconds since TT 1998.0
period = 1.7429935 * 86400
T_dur = 135*60 # transit duration in seconds

# start and end phase of transit:
p_start_transit = (period - 0.5*135*60)/period
p_end_transit = (period + 0.5*135*60)/period




