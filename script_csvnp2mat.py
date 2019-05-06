#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on November 9 2018
@author: Juliette MILLET
script to conver numpy array in .csv files (of the form time x dimension) into a big .mat file, all array concatenated to have DxN matrix
with D the dimension of the features, and N the number of points part of the training set, and a .csv numpy file (N2xD) for the validation set
Code adapted from Thomas Schatz's one
"""

import numpy as np
import scipy.io as sio
import os
import io

def csvnp2mat(csvnp_feat_folder, mat_file, vad_file = '', percent_valid = 0):
    """
    Create .mat file for train from numpy csv files and .csv file for validation
    :param csvnp_feat_folder: folder where the numpy arrays are
    :param mat_file: where to save train data (.mat)
    :param vad_file: where to save valid data (.csv)
    :param percent_valid: percentage wanted for validation
    :return: None
    """
    data = []
    for root, dirs, files in os.walk(csvnp_feat_folder):
        len_total = len(files)
        count = 0
        for filename in files:
            # print filename
            count += 1
            if count % 100 == 0:
                print(count, "files done on", len_total)
            if not filename.endswith('.csv'):
                continue
            full_name = os.path.join(root.lstrip('./'), filename)
            feat_array = np.loadtxt(full_name, delimiter=',')
            feat_array = np.swapaxes(feat_array, 0, 1) # to have the .mat file DxN if not in th right order
            data.append(feat_array)

    data = np.concatenate(data, 1)
    data = np.swapaxes(data, 0,1)
    np.random.shuffle(data)  # drop order
    data = np.swapaxes(data, 0, 1)
    if vad_file is '':
        sio.savemat(mat_file, {'data': data})
    else:
        nb_samples = data.shape[1]
        print('total number of samples', nb_samples)
        percent_v = int(percent_valid*nb_samples/100.)
        print('number of validation samples', percent_v)
        np.savetxt(vad_file, np.swapaxes(data[:,:percent_v ], 0, 1), delimiter=',')
        sio.savemat(mat_file, {'data': data[:,percent_v:]})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='transform csv files to mat file and csv file for validation')
    parser.add_argument('csvnp_feat_folder', metavar='feat', type=str,
                        help='folder where the csv numpy files are')
    parser.add_argument('mat_train_file', metavar='mat_train', type=str,
                        help='mat file for train created')
    parser.add_argument('csv_valid_file', metavar='csv_valid', type=str,
                        help='csv file for validation if wanted, if not put \'\'')
    parser.add_argument('percentage_valid', metavar='perc_valid', type=int,
                        help='percentage used for validation (sequences shuffled) if not wanted put 0, usually put 10')

    args = parser.parse_args()

    csvnp2mat(args.csvnp_feat_folder, args.mat_train_file, args.csv_valid_file, args.percentage_valid)