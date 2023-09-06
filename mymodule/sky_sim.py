#! /Usr/bin/env python 
"""Determine Andromeda location in ra/dec degrees"""

from math import cos, pi
from random import uniform
import argparse
import logging


# configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mylogger")

# use the logger
log.info('This is an info message')



NSRC = 1_000_000
# from wikipedia
RA_str = '00:42:44.0'
DEC_str = '41:16:00'


def get_redec():
    """
    Generate the ra/dec coordinates of Andromeda
    in decimal degrees.

    Returns
    -------
    ra : float
        The RA, in degrees, for Andromeda
    dec : float
        The DEC, in degrees for Andromeda
    """
    log.debug("Starting get_radec")
    
    andromeda_ra = '00:42:44.3'
    andromeda_dec = '41:16:09'
    
    d, m, s = andromeda_dec.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = andromeda_ra.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)
    log.debug("Finished get_radec")
    return ra, dec


def make_positions(ra, dec, nsrc=NSRC):
    """
    Generate nsrc stars within 1 degree of the given ra/dec

    Parameters
    ----------
    ra, dec : float
        The ra and dec in degrees for the central location.
    nsrc : int
        The number of star locations to generate.
        Default = mymodule.sky_sim.NSRC
    
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates.
    """
    log.debug(f"Start make_positions with {ra}, {dec}, {nsrc}")
    # make 1000 stars within 1 degree of Andromeda
    ras = []
    decs = []
    for i in range(NSRC):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))
    return ras, decs

    # apply our filter
    ras, decs = crop_to_circle(ras, decs, ra, dec, 1)
    log.debug("Finished make_positions")
    return ras, decs

def clip_to_radius(ra, decs, ref_ra, ref_dec, radius):
    log.debug("Being clipping in clip_to_radius")
    mask = np.where(np.hypot((ras-ref_ra), (decs-ref_dec)) <= radius)
    cropped_ras = ras[mask]
    cropped_decs = decs[mask]
    return cropped_ras, cropped_decs

def crop_to_circle(ras, decs, ref_ra, ref_dec, radius):
    log.debug("Being cropping in crop_to_circle")
    ra_out = []
    dec_out = []
    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(ras[i])
    return ra_out, dec_out


def save_positions(ras, decs, out='catalog.csv'):
    log.debug(f"writing catalogue to {out}")
    # now write these to a csv file for use by my other program
    with open('catalog.csv','w', encoding='utf8') as f:
        print("id,ra,dec", file=f)
        for i in range(NSRC):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)
    log.info(f"Wrote file {out}")


def skysim_parser():
    """
    Configure the argparse for skysim

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for skysim.
    """
    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')
    parser.add_argument('--ra', dest = 'ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest = 'dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
                        help='destination for the output catalog')
    return parser


def main():
    parser = skysim_parser()
    options = parser.parse_args()

     # if ra/dec are not supplied the use a default value
    if None in [options.ra, options.dec]:
        ra, dec = get_radec()
    else:
        ra = options.ra
        dec = options.dec 
        
    ras, decs = make_positions(ra, dec, NSRC)
    save_positions(ras, decs, options.out)


if __name__ =="__main__":
    main()
