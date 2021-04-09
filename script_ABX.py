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
    list_trip_OTH_TGT_X_trueX = {}
    f = open(file_abx, 'r')
    ind = f.readline()
    ind = ind.replace('\n', '').split(',')
    for line in f:
        new_line = line.split(',')
        #print(new_line)
        if len(new_line) > 0:
            list_trip_OTH_TGT_X_trueX[new_line[ind.index('tripletid')]] = [ new_line[ind.index('file_OTH')] ,
                                                                        new_line[ind.index('file_TGT')],
                                                                        new_line[ind.index('file_X')],
                                                                        new_line[ind.index('file_TGT')]]
    f.close()
    return list_trip_OTH_TGT_X_trueX




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
    list_trip_OTH_TGT_X_trueX = extract_list_files_compare(file_abx)
    results = [] # A, B, X then result between A and B
    distances = [] # A, B, X then AX and BX
    for trip in list_trip_OTH_TGT_X_trueX:
        triplet = list_trip_OTH_TGT_X_trueX[trip]
        OTH = np.loadtxt(folder_files + '/' + triplet[0] + '.csv', delimiter = ',')
        TGT = np.loadtxt(folder_files + '/' + triplet[1] + '.csv', delimiter = ',')
        X = np.loadtxt(folder_files + '/' + triplet[2] + '.csv', delimiter = ',')
        #print(triplet[0], triplet[1], triplet[2])
        #print(A.shape, B.shape, X.shape)
        if OTH.shape[1] != X.shape[1] or TGT.shape[1] != X.shape[1]:
            #print("in")
            OTH = np.swapaxes(OTH, 0, 1)
            TGT = np.swapaxes(TGT, 0, 1)
            X = np.swapaxes(X, 0, 1)
        else:
            pass
            #print("out")
        if dist_for_cdist == "kl":
            OTHX = dtw.accelerated_dtw(OTH, X, dist = dtw.kl_divergence)[0]
            TGTX = dtw.accelerated_dtw(TGT, X, dist = dtw.kl_divergence)[0]
        else:
            OTHX = dtw.accelerated_dtw(OTH, X, dist = dist_for_cdist)[0]
            TGTX = dtw.accelerated_dtw(TGT, X, dist = dist_for_cdist)[0]
        result = 'OTH' if OTHX < TGTX else 'TGT'
        results.append(triplet + [result])
        distances.append(triplet + [OTHX, TGTX])
        list_trip_OTH_TGT_X_trueX[trip].append(OTHX)
        list_trip_OTH_TGT_X_trueX[trip].append(TGTX)
    return results, distances, list_trip_OTH_TGT_X_trueX

def keep_results(results, distances, dico_final, output_file_results, output_file_distances, file_abx, output_final_distances):
    f = open(output_file_distances, 'w')
    g = open(output_file_results, 'w')
    h = open(output_final_distances, 'w')
    orig = open(file_abx, 'r')

    g.write('OTH,TGT,X,corr_result,model_result\n')
    for res in results:
        string_to_write = str(res[0])
        for j in range(1, len(res)):
            string_to_write += ',' + str(res[j])
        g.write(string_to_write + '\n')
    g.close()

    f.write('OTH,TGT,X,corr_result,OTHX,TGTX\n')
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

    parser = argparse.ArgumentParser(description='Output the abx scores from list of abx triplet and .csv files of the representation of each triphone')
    parser.add_argument('file_abx', metavar='abx', type=str,
                        help='file with the list of ABX triplet you want to compare, the file needs to have at least three columns, one file_OTH, file_TGT and file_X')
    parser.add_argument('fold_files', metavar='fold', type=str,
                        help='the folder where the features files are')
    parser.add_argument('distance', metavar='d', type=str,
                        help='distance used for the dtw computation: distance used by cdist, can be \'braycurtis\', '
                             '\'canberra\',\'chebyshev\', \'cityblock\', \'correlation\', \'cosine\', \'dice\', \'euclidean\', '
                             '\'hamming\', \'jaccard\', \'kulsinski\', \'mahalanobis\', \'matching\', \'minkowski\', \'rogerstanimoto\', '
                             '\'russellrao\', \'seuclidean\', \'sokalmichener\', \'sokalsneath\', \'sqeuclidean\', \'wminkowski\', '
                             '\'yule\'. if \'kl\', then instead of dtw with a distance, we use kl divergence')
    parser.add_argument('output_file', metavar='out', type=str,
                        help='output file beginning: three file are produced : one _results of the form OTH, TGT, X, real, '
                             'result_model one _distances same as _results but with OTHX and TGTX distances at the end the '
                             'last one _final of the same form that the file you give it : just add distances results')


    args = parser.parse_args()

    print('Computing ABX results...')
    resul, dis, dico = compute_ABX_results(args.file_abx, args.fold_files, dist_for_cdist=args.distance)
    print('Saving files...')
    keep_results(resul, dis, dico, output_file_results=args.output_file + '_results.csv',
                 output_file_distances=args.output_file + '_distances.csv', file_abx=args.file_abx, output_final_distances=args.output_file + '_final.csv')
    print('Done')
