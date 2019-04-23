#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on November 13 2018
@author: Juliette MILLET
script to compute ABX results from .csv feature files -> create three files; one _results of the form A, B, X, real, result_model
one _distances same as _results but with AX and BX distances at the end
the last one _final of the same form that the file you give it : just add distances results
"""

import dtw
import numpy as np

def extract_list_files_compare(file_abx):
    """
    Extract from file_abx, a csv file, a list of triplet A (OTH) B (TGT -> good answer)  and X to compare
    :param file_abx: text file with list of filename A B X in order
    :return: dico of triplet name :[ A, B ,X ,trueX namefiles]
    """
    list_trip_A_B_X_trueX = {}
    f = open(file_abx, 'r')
    ind = f.readline()
    ind = ind.replace('\n', '').split(',')
    for line in f:
        new_line = line.split(',')
        #print(new_line)
        if len(new_line) > 0:
            list_trip_A_B_X_trueX[new_line[ind.index('tripletid')]] = [ new_line[ind.index('file_OTH')] ,
                                                                        new_line[ind.index('file_TGT')],
                                                                        new_line[ind.index('file_X')],
                                                                        new_line[ind.index('file_TGT')]]
    f.close()
    return list_trip_A_B_X_trueX




def compute_ABX_results(file_abx, folder_files, dist_for_cdist):
    """
    Compute results of ABX test on a set for a set of triplets
    :param file_abx: text file with list of filename A B X in order
    :param folder_files: path to feature files .csv to use
    :param dist_for_cdist: distance used by cdist, can be 'braycurtis', 'canberra',
    'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
    'jaccard', 'kulsinski', 'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto',
    'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'wminkowski', 'yule'.
    if 'kl', then instead of dtw with a distance, we use kl divergence
    :return: results list of [A, B, X, truueX, result] and distances list of [A, B, X, trueX, AX, BX]
    """
    dico_A_B_X_trueX = extract_list_files_compare(file_abx)
    results = [] # A, B, X then result between A and B
    distances = [] # A, B, X then AX and BX
    for trip in dico_A_B_X_trueX:
        triplet = dico_A_B_X_trueX[trip]
        A = np.loadtxt(folder_files + '/' + triplet[0] + '.csv', delimiter = ',')
        B = np.loadtxt(folder_files + '/' + triplet[1] + '.csv', delimiter = ',')
        X = np.loadtxt(folder_files + '/' + triplet[2] + '.csv', delimiter = ',')
        #print(triplet[0], triplet[1], triplet[2])
        #print(A.shape, B.shape, X.shape)
        if A.shape[1] != X.shape[1] or B.shape[1] != X.shape[1]:
            #print("in")
            A = np.swapaxes(A, 0, 1)
            B = np.swapaxes(B, 0, 1)
            X = np.swapaxes(X, 0, 1)
        else:
            pass
            #print("out")
        if dist_for_cdist == "kl":
            AX = dtw.accelerated_dtw(A, X, dist = dtw.kl_divergence)[0]
            BX = dtw.accelerated_dtw(B, X, dist = dtw.kl_divergence)[0]
        else:
            AX = dtw.accelerated_dtw(A, X, dist = dist_for_cdist)[0]
            BX = dtw.accelerated_dtw(B, X, dist = dist_for_cdist)[0]
        result = 'A' if AX < BX else 'B'
        results.append(triplet + [result])
        distances.append(triplet + [AX, BX])
        dico_A_B_X_trueX[trip].append(AX)
        dico_A_B_X_trueX[trip].append(BX)
    return results, distances, dico_A_B_X_trueX

def keep_results(results, distances, dico_final, output_file_results, output_file_distances, file_abx, output_final_distances):
    f = open(output_file_distances, 'w')
    g = open(output_file_results, 'w')
    h = open(output_final_distances, 'w')
    orig = open(file_abx, 'r')

    g.write('A,B,X,corr_result,model_result\n')
    for res in results:
        string_to_write = str(res[0])
        for j in range(1, len(res)):
            string_to_write += ',' + str(res[j])
        g.write(string_to_write + '\n')
    g.close()

    f.write('A,B,X,corr_result,AX,BX\n')
    for res in distances:
        string_to_write = str(res[0])
        for j in range(1, len(res)):
            string_to_write += ',' + str(res[j])
        f.write(string_to_write + '\n')
    f.close()

    line_index = orig.readline()
    ind = line_index.split(',')
    h.write(line_index)
    for line in orig:
        new_line = line.replace('\n', '')
        h.write(new_line)
        triplet_name = new_line.split(',')[ind.index('tripletid')]
        h.write(',' + str(dico_final[triplet_name][4]) + ',' + str(dico_final[triplet_name][5]) + '\n')
    h.close()



if __name__ == '__main__':
    import argparse
    fil_abx = sys.argv[1]
    fold_files = sys.argv[2]
    distance = sys.argv[3]
    output_file = sys.argv[4]
    print('Computing ABX results...')
    resul, dis, dico = compute_ABX_results(fil_abx, fold_files, dist_for_cdist=distance)
    print('Saving files...')
    keep_results(resul, dis, dico, output_file_results=output_file + '_results.csv',
                 output_file_distances=output_file + '_distances.csv', file_abx=fil_abx, output_final_distances=output_file + '_final.csv')
    print('Done')
