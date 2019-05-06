#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on November 9 2018
@author: Juliette MILLET
Extract posteriors from Jason Chang's library DPGMM model.
The models are treated as GMM not as DPGMM, following Chen et al.
(we consider that what was learnt is the MAP mixture instead of a whole
distribution over mixtures) Code adapted form Thomas Schatz's one
Input:
    folder with csv numpy array containing features inside of the format DxN with D dimension of features, N time
    GMM from Jason Chang's library in .mat format
Output:
    csv numpy array files with posteriorgrams of the format NxD with D the number of clusters and N time
"""

import os.path as path
import scipy
import scipy.io as io
import numpy as np
import os

#######################
# Auxiliary functions #
#######################
"""
Taken from Elina's megamix code for GMM E-step
Could use directly Elina's library when it is ready
"""


def _compute_precisions_chol(cov):
    n_components, n_features, _ = cov.shape
    precisions_chol = np.empty((n_components, n_features, n_features))
    for k, covariance in enumerate(cov):
        try:
            cov_chol = scipy.linalg.cholesky(covariance, lower=True)
        except scipy.linalg.LinAlgError:
            raise ValueError(str(k) + \
                             "-th covariance matrix non positive definite")
        precisions_chol[k] = scipy.linalg.solve_triangular(cov_chol,
                                                           np.eye(n_features),
                                                           lower=True).T
    return precisions_chol


def _log_normal_matrix(points, means, cov):
    """
    This method computes the log of the density of probability of a normal
    law centered. Each line
    corresponds to a point from points.

    @param points: an array of points (n_points,dim)
    @param means: an array of k points which are the means of the clusters
                  (n_components,dim)
    @param cov: an array of k arrays which are the covariance matrices
                (n_components,dim,dim)
    @return: an array containing the log of density of probability of a normal
             law centered (n_points,n_components)
    """
    n_points, dim = points.shape
    n_components, _ = means.shape
    precisions_chol = _compute_precisions_chol(cov)
    log_det_chol = np.log(np.linalg.det(precisions_chol))
    log_prob = np.empty((n_points, n_components))
    for k, (mu, prec_chol) in enumerate(zip(means, precisions_chol)):
        y = np.dot(points, prec_chol) - np.dot(mu, prec_chol)
        log_prob[:, k] = np.sum(np.square(y), axis=1)
    return -.5 * (dim * np.log(2 * np.pi) + log_prob) + log_det_chol


#######
# API #
#######

def load_model(filename):
    """
    Load GMM model saved in .mat from Jason Chang's library
    Output:
        Dictionary with entries:
            cov : array of floats (n_components,dim,dim)
                Contains the computed covariance matrices of the mixture.

            means : array of floats (n_components,dim)
                Contains the computed means of the mixture.

            log_weights : array of floats (n_components,)
    """
    # file format is not consistent between Chang's init and update steps...
    data = io.loadmat(filename)
    sh = data['clusters'].shape
    if sh[0] == 1:
        K = sh[1]
        # dt = data['clusters'].dtype.descr
        # keys = [dt[i][0] for i in range(len(dt))]  # names of various descriptors for clusters
        model = {}
        logpi = [data['clusters'][0, i]['logpi'] for i in range(K)]
        model['log_weights'] = np.concatenate(logpi).reshape((K,))  # (K,)
        mu = [data['clusters'][0, i]['mu'] for i in range(K)]
        model['means'] = np.column_stack(mu).T  # (K,d)
        d = model['means'].shape[1]
        Sigma = [data['clusters'][0, i]['Sigma'].reshape((1, d, d)) for i in range(K)]
        model['cov'] = np.concatenate(Sigma, axis=0)  # (K,d,d)
    else:
        K = sh[0]
        model = {}
        logpi = [data['clusters'][i, 0]['logpi'] for i in range(K)]
        model['log_weights'] = np.concatenate(logpi).reshape((K,))  # (K,)
        mu = [data['clusters'][i, 0]['mu'] for i in range(K)]
        model['means'] = np.column_stack(mu).T  # (K,d)
        d = model['means'].shape[1]
        Sigma = [data['clusters'][i, 0]['Sigma'].reshape((1, d, d)) for i in range(K)]
        model['cov'] = np.concatenate(Sigma, axis=0)  # (K,d,d)
    return model


def compute_log_posteriors(points, model):
    """
    Returns responsibilities for each
    point in each cluster

    Parameters
    ----------
    points : an array (n_points,dim)
    model : GMM model, formatted like the output from load_model

    Returns
    -------
    log_resp: an array (n_points,n_components)
        an array containing the logarithm of the responsibilities.
    """
    log_normal_matrix = _log_normal_matrix(points,
                                           model['means'],
                                           model['cov'])
    log_product = log_normal_matrix + model['log_weights'][:, np.newaxis].T
    log_prob_norm = scipy.special.logsumexp(log_product, axis=1)
    log_resp = log_product - log_prob_norm[:, np.newaxis]
    return log_resp


def extract_posteriors(features_folder, model_file, output_folder):
    """ Extract posteriorgramm for each np csv feature file and save it as csv files """
    print('Loading model')
    model = load_model(model_file)
    print('Model with {} clusters loaded'.format(len(model['log_weights'])))
    print('Loading input features')
    for root, dirs, files in os.walk(features_folder):
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
            if feat_array.shape[0] == 39:
                feat_array = feat_array.swapaxes(0,1)
            #feat_array = np.swapaxes(feat_array, 0, 1) # Change that if error of axes size
            post_data =  np.exp(compute_log_posteriors(feat_array, model))
            np.savetxt( output_folder + '/' + filename[:len(filename) - 3] + 'csv', post_data, delimiter=',')





if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract posteriors from features file and a chosen model')
    parser.add_argument('features_folder', metavar='feat', type=str,
                        help='folder where the csv numpy files are (mfccs or other)')
    parser.add_argument('model_file', metavar='model_mat', type=str,
                        help='mat file of the model you want to use')
    parser.add_argument('output_folder', metavar='out', type=str,
                        help='output folder where to put the posteriors')


    args = parser.parse_args()

    extract_posteriors(args.features_folder, args.model_file, args.output_folder)
