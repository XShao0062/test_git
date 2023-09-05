#! /Usr/bin/env python 
"""Determine Andromeda location in ra/dec degrees"""

from math import cos, pi
from random import uniform
import numpy as np

NSRC = 1_000_000
# from wikipedia
RA = '00:42:44.1'
DEC = '41:16:00'

def make_positions():
    # convert to decimal degrees
    d, m, s = DEC.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = RA.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)


    # make 1000 stars within 1 degree of Andromeda
    ras = []
    decs = []
    for i in range(NSRC):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))
    return ras, decs

def clip_to_radius(ra, decs, ref_ra, ref_dec, radius):

    mask = np.where(np.hypot((ras-ref_ra), (decs-ref_dec)) <= radius)
    cropped_ras = ras[mask]
    cropped_decs = decs[mask]
    return cropped_ras, cropped_decs

def crop_to_circle(ras, decs, ref_ra, ref_dec, radius):
    ra_out = []
    dec_out = []
    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(ras[i])
    return ra_out, dec_out

def save_positions(ras, decs):
    # now write these to a csv file for use by my other program
    with open('catalog.csv','w', encoding='utf8') as f:
        print("id,ra,dec", file=f)
        for i in range(NSRC):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)

def clip_to_radius():
    return

def main():
    ras, decs = make_positions()
    save_positions(ras, decs)

if __name__ =="__main__":
    main()
