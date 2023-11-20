#!/usr/bin/env python3
'''
resultsPlotter.py

Plots the spectrum and rbm from Stage 6 FITS files.

usage: ./resultsPlotter.py [-options] filepath

'''

import argparse
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from scipy import stats
import os

parser = argparse.ArgumentParser(
    description='Takes Stage 6 files and make plots')
parser.add_argument('-spec','-spectrum', default='', help='path to spectrum fits file')
parser.add_argument('-rbm', default='', help='path to rbm fits file')

try:
    args = parser.parse_args() # grabs sys.argv by default
except:
    sys.exit()

specfile = args.spec
rbmfile = args.rbm

def chi_sq_gof(energy,flux,error,normalization,index):
    x = energy.copy()
    y_o = flux.copy()
    y_e = normalization*x**index
    chi_sq = np.sum(np.divide((y_o-y_e)**2,error**2))
    p_val = 1 - stats.chi2.cdf(chi_sq, len(energy)-2)
    return chi_sq,p_val

def plot_spec(spec_file):
    spec = fits.getdata(spec_file,1,header=True)
    specFit = fits.getdata(spec_file,2,header=True)
    specCov = fits.getdata(spec_file,3,header=True)
    E = spec[0].Energy; F = spec[0].Flux; F_err = spec[0].FluxError
    sig = spec[0].Significance
    norm = specFit[0].Normalization[0]; ind = specFit[0].Index[0]
    chi_sq,p_val=chi_sq_gof(E,F,F_err,norm,ind)
    
    plt.rcParams.update({'font.size': 15})
    fig,ax = plt.subplots(1,2,figsize=(16,7))
    
    ax[0].errorbar(E,F,yerr=F_err,fmt='o',elinewidth=3,markersize=9)
    x = np.linspace(spec[0].EBinLowEdge[0],spec[0].EBinHiEdge[-1],100)
    y = norm*x**ind
    ax[0].plot(x,y,linewidth=3)
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[0].set_xlabel('Energy [TeV]')
    ax[0].set_ylabel(r"dN/dE [Te$V^{-1}$ m$^{-2}$ s$^{-1}$]")
    ax[0].set_title('Flux vs Energy')
    ax0_str = r'$\chi^2$ / dof = {:.4g} / {}'.format(chi_sq,len(spec[0].Energy)-2)
    ax0_str += '\nProb = {:.4g}\n'.format(p_val)
    ax0_str += r'Norm = {:.4g} $\pm$ {:.4g}'.format(norm,specFit[0].Normalization[1])
    ax0_str += '\n'
    ax0_str += r'Index = {:.4g} $\pm$ {:.4g}'.format(ind,specFit[0].Index[1])
    ax[0].annotate(ax0_str,
                   xy=(0.3,0.67),xycoords='axes fraction')
    
    ax[1].scatter(E,sig,s=75)
    ax[1].set_xscale('log')
    ax[1].set_xlabel('Energy [TeV]')
    ax[1].set_ylabel(r'Significance [$\sigma$]')
    ax[1].set_title('Significance vs Energy')
    ax[1].set_xlim(ax[0].get_xlim())
    ax1_str = r'MaxSig / E = {:.4g} / {:.4g}'.format(np.max(sig),E[np.argmax(sig)])
    ax1_str += '\n'
    ax1_str += r'MinSig / E = {:.4g} / {:.4g}'.format(np.min(sig),E[np.argmin(sig)])
    ax[1].annotate(ax1_str,xy=(0.4,0.75),xycoords='axes fraction')
    plt.show()

def plot_rbm(rbm_file):
    with fits.open(rbm_file) as d_sky:
        raw_excess_map = d_sky[1].data
        sig_map = d_sky[2].data
        acceptance_map = d_sky[3].data
        raw_on_map = d_sky[4].data
        alpha_map = d_sky[5].data
        unc_excess_map = d_sky[6].data
        sig_distri = d_sky[7].data
        names = [d_sky[i+1].header['EXTNAME'] for i in range(7)]

    maps = [raw_excess_map,sig_map,acceptance_map,
            raw_on_map,alpha_map,unc_excess_map,sig_distri]
    
    plt.rcParams.update({'font.size': 25})
    fig, axes = plt.subplots(2,3,figsize=(40,21))
    plt.subplots_adjust(wspace=0.4)
    for i in range(2):
        for j in range(3):
            ax = axes[i,j]
            m = maps[3*i+j]
            im = ax.contourf(m,levels=1000)
            ax.set_title(names[3*i+j])
            plt.colorbar(im,fraction=0.046, pad=0.04, ax=ax)
            ax.set_xlabel('x [pixel]'); ax.set_ylabel('y [pixel]')
    plt.show()
    

if __name__ == '__main__':
    if specfile != '':
        print('plotting spectrum...')
        try:
            plot_spec(specfile)
        except FileNotFoundError:
            specfile = input('spec fits file not found!\ninput path to fits file: ')
            try:
                plot_spec(specfile)
            except:
                print('error in plotting spectrum! check spec fits file!')
    if rbmfile != '':
        print('plotting sky maps...')
        try:
            plot_rbm(rbmfile)
        except FileNotFoundError:
            rbmfile = input('rbm fits file not found!\ninput path to fits file: ')
            try:
                plot_rbm(rbmfile)
            except:
                print('error in plotting sky maps! check rbm fits file!')
    if (specfile == '') and (rbmfile == ''):
        print('no input stage 6 fits file!')