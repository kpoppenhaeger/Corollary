# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as fits
#import numpy.ma as ma
from astropy.table import Table
from directories_etc import *


#######################################
# read barycentered pn LCs and pn-bg LCs and plot bg-subtracted LCs as funtion of phase.
#######################################

def make_pn_bgsub_lcs(folders=folders, path=path, pn_lc=pn_lc, pn_lcbg=pn_lcbg):
  # calculates bg-subtracted pn light curves as function of orbital phase.
  # set up lists for the data to be read in:
  phases = []
  rates = []
  errors = []
  for i in np.arange(0, len(folders)):
    # read in data
    hdu = fits.open(path + folders[i] + '/' + pn_lc)
    data = hdu[1].data
    hdu.close()
    hdu = fits.open(path + folders[i] + '/' + pn_lcbg)
    databg = hdu[1].data
    hdu.close()
    # calculate orbital phase:
    phase = np.mod(data['TIME'] - t_transit_xmm, period)/period
    phase[phase<0.5] = 1. + phase[phase<0.5]
    # calculate bg-subtracted count rate:
    rate_net = data['RATE'] - databg['RATE']*bgfactor
    rate_error_net = data['ERROR'] + databg['ERROR']*bgfactor
    # save into a structure:
    phases.append(phase)
    rates.append(rate_net)
    errors.append(rate_error_net)
    
  return (phases, rates, errors)


def plot_pn_bgsub_lcs(phases, rates, errors, folders=folders):
  # plots bg-subtracted pn light curves as function of orbital phase
  # make a multiplot, 5 subplots per plot:
  N = 5
  for j in np.arange(0, len(folders)/N+(np.mod(len(folders),N)>0)):
    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, sharex=True, sharey=True, figsize=(8,12))
    ax1.plot(phases[j*N+0], rates[j*N+0])
    ax2.plot(phases[j*N+1], rates[j*N+1])
    ax3.plot(phases[j*N+2], rates[j*N+2])
    ax4.plot(phases[j*N+3], rates[j*N+3])
    ax5.plot(phases[j*N+4], rates[j*N+4])
    plt.xlabel('orbital phase')
    plt.ylabel('                                                                           net pn count rate')
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)


def plot_pn_bgsub_lcs_3bands(phases, rates, errors, phases_s, rates_s, errors_s, phases_h, rates_h, errors_h,fodlers = folders):
  # plots bg-subtracted pn light curves as function of orbital phase, using full band, soft band, and hard band
  # make a multiplot, 5 subplots per plot:
  N = 5
  for j in np.arange(0, len(folders)/N+(np.mod(len(folders),N)>0)):
    f, axarr = plt.subplots(N, sharex=True, figsize=(8,12))
    for i in np.arange(0,N):
      axarr[i].plot(phases[j*N+i], rates[j*N+i], color='k')
      axarr[i].plot(phases_s[j*N+i], rates_s[j*N+i], color='r')
      axarr[i].plot(phases_h[j*N+i], rates_h[j*N+i], color='b')
      axarr[i].plot([p_start_transit, p_start_transit], [0., 0.03], 'k--')
      axarr[i].plot([p_end_transit, p_end_transit], [0., 0.03], 'k--')
      axarr[i].axis([0.8, 1.2, 0., 0.03])
      axarr[i].set_yticks([0, 0.01, 0.02])
      if i==0:
        axarr[i].legend(['0.2-3 keV', '0.2-0.8 keV', '0.8-3 keV'], fontsize=12)
        axarr[i].set_title('Obs ' + str(folders[j*N+0]) + ' - ' + str(folders[j*N + N-1]) )
    
    plt.xlabel('orbital phase')
    plt.ylabel('                                                                           bg-subtracted pn count rate')
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    plt.savefig(plotdir + 'KP_pn_bgsub_' + str(j+1) + '.pdf')





#######################################
# find start and end times for each source exposure
#######################################

def get_start_end_times(folders=folders, path=path, instrument='pn'):
  # reads the arrival time of the first photon in each source file of each observation for a given instrument
  start_times = np.zeros(len(folders))
  end_times = np.zeros(len(folders))
  if instrument == 'pn': instr_file = pn_src
  if instrument == 'mos1': instr_file = mos1_src
  if instrument == 'mos2': instr_file = mos2_src
  for i in np.arange(0, len(folders)):
    hdu = fits.open(path + folders[i] + '/' + instr_file)
    data = hdu[1].data
    hdu.close()
    start_times[i] = data[0]['TIME']
    end_times[i] = data[-1]['TIME']
  
  return (start_times, end_times)



#######################################
# calculate orbital phases of photon arrival times, write them (with the other event file data) into new fits file for each observation and instrument
#######################################

def make_new_fits_with_phase(folders=folders, path=path, instrument='pn', t_transit_xmm=t_transit_xmm, period=period):
  # make new fits event files which contain orbital phase information
  if instrument == 'pn': instr_file_s = pn_src; instr_file_b = pn_bg
  if instrument == 'mos1': instr_file_s = mos1_src; instr_file_b = mos1_bg
  if instrument == 'mos2': instr_file_s = mos2_src; instr_file_b = mos2_bg
  # for all observations:
  for i in np.arange(0, len(folders)):
    # calculate and save phase for source files:
    hdu = fits.open(path + folders[i] + '/' + instr_file_s)
    data = hdu[1].data
    hdu.close()
    # calculate orbital phase:
    phase = np.mod(data['TIME'] - t_transit_xmm, period)/period
    phase[phase<0.5] = 1. + phase[phase<0.5]
    # what information we need for the new file:
    # time, phase, pi (i.e. photon energy to be able to filter later)
    col1 = fits.Column(name='TIME', format='E', array=data['TIME'])
    col2 = fits.Column(name='PHASE', format='E', array=phase)
    col3 = fits.Column(name='PI', format='I', array=data['PI'])
    cols = fits.ColDefs([col1, col2, col3])
    tbhdu = fits.new_table(cols)
    tbhdu.writeto(path + folders[i] + '/' + instr_file_s.replace('.fits', '_phase.fits'), clobber=True)
    # calculate and save phase for bg files:
    hdu = fits.open(path + folders[i] + '/' + instr_file_b)
    data = hdu[1].data
    hdu.close()
    # calculate orbital phase:
    phase = np.mod(data['TIME'] - t_transit_xmm, period)/period
    phase[phase<0.5] = 1. + phase[phase<0.5]
    # what information we need for the new file:
    # time, phase, pi (i.e. photon energy to be able to filter later)
    col1 = fits.Column(name='TIME', format='E', array=data['TIME'])
    col2 = fits.Column(name='PHASE', format='E', array=phase)
    col3 = fits.Column(name='PI', format='I', array=data['PI'])
    cols = fits.ColDefs([col1, col2, col3])
    tbhdu = fits.new_table(cols)
    tbhdu.writeto(path + folders[i] + '/' + instr_file_b.replace('.fits', '_phase.fits'), clobber=True)   




#######################################
# compare count rates in and out of transit, using defined energy band
#######################################


def make_count_rate_comparison(folders=folders, path=path, instrument='pn', p_start_transit=p_start_transit, p_end_transit=p_end_transit, energy_low=200., energy_high=2000.):
  # initialize Table array:
  a = np.zeros(len(folders))
  counts = Table([a, a, a, a, a, a], names=('counts_in_tr_src', 'counts_in_tr_bg', 'counts_out_tr_src', 'counts_out_tr_bg', 'phase_in_tr', 'phase_out_tr'), meta={'name': 'first table'})
  # for all observations:
  for i in np.arange(0, len(folders)):
    # for source and bg:
    hdu = fits.open(path + folders[i] + '/' + 'pn_barycenter_src_phase.fits')
    data_s = hdu[1].data
    hdu.close()
    hdu = fits.open(path + folders[i] + '/' + 'pn_barycenter_bg_phase.fits')
    data_b = hdu[1].data
    hdu.close()
    # filter: before, during, after transit.
    # also filter for photon energies (energy_low, energy_high as defined in function call)
    tr_in_s = (data_s['PHASE'] >= p_start_transit) & (data_s['PHASE'] <= p_end_transit) & (data_s['PI'] >= energy_low) & (data_s['PI'] <= energy_high)
    tr_before_s = (data_s['PHASE'] < p_start_transit) & (data_s['PI'] >= energy_low) & (data_s['PI'] <= energy_high)
    tr_after_s = (data_s['PHASE'] > p_end_transit) & (data_s['PI'] >= energy_low) & (data_s['PI'] <= energy_high)
    tr_in_b = (data_b['PHASE'] >= p_start_transit) & (data_b['PHASE'] <= p_end_transit) & (data_b['PI'] >= energy_low) & (data_b['PI'] <= energy_high)
    tr_before_b = (data_b['PHASE'] < p_start_transit) & (data_b['PI'] >= energy_low) & (data_b['PI'] <= energy_high)
    tr_after_b = (data_b['PHASE'] > p_end_transit) & (data_b['PI'] >= energy_low) & (data_b['PI'] <= energy_high)
    # if observation covers at least part of transit, get number of counts and covered phase interval:
    if np.sum(tr_in_s)>0:
      #source
      counts['counts_in_tr_src'][i] = len(data_s['PHASE'][tr_in_s])
      # background
      counts['counts_in_tr_bg'][i] = len(data_b['PHASE'][tr_in_b])
      # just take phase from source event file, because background region will have same exposure time anyway
      counts['phase_in_tr'][i] = data_s['PHASE'][tr_in_s][-1] - data_s['PHASE'][tr_in_s][0]
    # if observation covers time before and/or after transit, get number of counts and covered phase interval:
    c_before = 0
    c_before_bg = 0
    p_before = 0
    if np.sum(tr_before_s)>0:
      c_before = len(data_s['PHASE'][tr_before_s])
      c_before_bg = len(data_b['PHASE'][tr_before_b])
      p_before = data_s['PHASE'][tr_before_s][-1] - data_s['PHASE'][tr_before_s][0]
    
    c_after = 0
    c_after_bg = 0
    p_after = 0
    if np.sum(tr_after_s)>0:
      c_after = len(data_s['PHASE'][tr_after_s])
      c_after_bg = len(data_b['PHASE'][tr_after_b])
      p_after = data_s['PHASE'][tr_after_s][-1] - data_s['PHASE'][tr_after_s][0]
    
    # sum up before and after transit data to get all count out of transit:
    counts['counts_out_tr_src'][i] = c_before + c_after
    counts['counts_out_tr_bg'][i] = c_before_bg + c_after_bg
    counts['phase_out_tr'][i] = p_before + p_after
  
  return counts




