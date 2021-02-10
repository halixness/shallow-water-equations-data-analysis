#!/usr/bin/python

# Diego Calanzone
# 17-01-2021
# SWE - Task 00

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

# -----------
parser = OptionParser()

parser.add_option("-o", "--output-dir", dest="out_dir",
                  help="Directory file decodificati", metavar="FILE")

parser.add_option("-n", "--bccs", dest="bccs",
                  help="Numero di simulazioni (BCCs forniti)", metavar="FILE")

parser.add_option("-p", "--prefix", dest="prefix", default="toce_ris_V17_50",
                  help="Prefisso simulazione (es: toce_ris_V17_50)", metavar="FILE")

parser.add_option("-y", "--numpy", dest="exp_numpy", default="0",
                  help="Opzione esporta in formato numpy", metavar="FILE")

(options, args) = parser.parse_args()

if options.out_dir is None or options.bccs is None:
    print("Usage: -o outputdir -n numero_simulazioni")
    exit()

# -----------

def txt_to_numpy(filename, line_skip = 5):
    f = open (filename, 'r')
    data = f.readlines()[line_skip:]

    return np.asarray(
        [l.replace("\n", "").split() for l in data]
    ).astype(np.float32)

def numpy_to_txt(filename, data):
    file = open(filename, "w+")
    for row in data:
        row.resize(1,row.shape[0])
        np.savetxt(file, row, fmt="%i", newline='\n', delimiter=' ')

    file.close()

# -----------

out_dir =  options.out_dir
n_bcc = int(options.bccs)
prefix = options.prefix
exp_numpy = (int(options.exp_numpy) == 1)

prefix_dir = "output/{}/decoded_".format(out_dir)
btm_file = "{}-decoded-last.BTM".format(prefix)
maxwse_file = "{}-decoded-last.MAXWSE".format(prefix)

plots_dir = "output/{}/plots".format(out_dir)
targets_dir = "output/{}/targets".format(out_dir)

# -----------

# Check & creating dirs
if not os.path.isdir(plots_dir): os.mkdir(plots_dir)
if not os.path.isdir(targets_dir):
    os.mkdir(targets_dir)
    os.mkdir("{}/5mm/".format(targets_dir))

# option numpy
if exp_numpy:
    targets_5mm = []

# Get & plot BTM
btm = txt_to_numpy("{}000/{}".format(prefix_dir, btm_file))
btm[btm > 1e10] = 0
plt.imsave("{}/btm.png".format(plots_dir), btm)

for bcc in range(n_bcc):

    source = "{}{:03d}".format(prefix_dir, bcc)

    maxwse = txt_to_numpy("{}/{}".format(source, maxwse_file))

    # Rimozione valori soglia
    maxwse[maxwse > 1e10] = 0

    # Generazione matrici target
    result = maxwse - btm
    result[result < 0] = 0

    binary_5mm = (result >= 5e-3)

    # -> numpy
    if exp_numpy:
        targets_5mm.append(binary_5mm)

    # -> files
    numpy_to_txt("{}/5mm/binary_{}.txt".format(targets_dir, bcc), binary_5mm)

    # Plotting
    plt.imsave("{}/maxwse_{}.png".format(plots_dir, bcc), maxwse)
    plt.imsave("{}/binary_5mm_{}.png".format(plots_dir, bcc), binary_5mm)

    print("Processed bcc: {}".format(bcc))

# -> file
if exp_numpy:
    targets_5mm = np.asarray(targets_5mm)
    np.save("{}/targets_5mm.npy".format(targets_dir), targets_5mm)
