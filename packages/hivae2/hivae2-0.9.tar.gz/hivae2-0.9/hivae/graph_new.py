#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:49:15 2018

Graph definition for all models

@author: anazabal, olmosUC3M, ivaleraM
@changes: athro
"""

import tensorflow as tf
import numpy as np
from hivae import VAE_functions
import hivae #import hivae as hivae

def HVAE_graph(model_name, types_description, batch_size, learning_rate=1e-3, z_dim=2, y_dim=1, s_dim=2, y_dim_partition=[]):
    
    #We select the model for the VAE
    #print('[*] Importing model: ' + model_name)
    hivae.hivae.vprint_s(2,'[*] Importing model: ' + model_name)
    # how to import a submoule 101
    model = __import__('hivae.{}'.format(model_name),fromlist=[model_name])
    #model = __import__(model_name)
    
    #Load placeholders
    hivae.hivae.vprint_s(2,'[*] Defining placeholders')
    batch_data_list, batch_data_list_observed, miss_list, tau, tau2, types_list = VAE_functions.place_holder_types(types_description, batch_size)
    
    #Batch normalization of the data
    X_list, normalization_params = VAE_functions.batch_normalization(batch_data_list_observed, types_list, miss_list)
    
    #Set dimensionality of Y
    if y_dim_partition:
        y_dim_output = np.sum(y_dim_partition)
    else:
        y_dim_partition = y_dim*np.ones(len(types_list),dtype=int)
        y_dim_output = np.sum(y_dim_partition)
    
    #Encoder definition
    hivae.hivae.vprint_s(2,'[*] Defining Encoder...')
    samples, q_params = model.encoder(X_list, miss_list, batch_size, z_dim, s_dim, tau)
    encoding = samples
    # hivae.hivae.vprint_s(2,'debug ' * 10)
    # hivae.hivae.vprint_s(2,samples)
    # hivae.hivae.vprint_s(2,'- ' * 10)
    # hivae.hivae.vprint_s(2,q_params)
    # hivae.hivae.vprint_s(2,'debug ' * 10)

    
    hivae.hivae.vprint_s(2,'[*] Defining Decoder...')
    theta, samples, p_params, log_p_x, log_p_x_missing = model.decoder(batch_data_list, miss_list, types_list, samples, q_params, normalization_params, batch_size, z_dim, y_dim_output, y_dim_partition, tau2)

    hivae.hivae.vprint_s(2,'[*] Defining Cost function...')
    ELBO, loss_reconstruction, KL_z, KL_s = model.cost_function(log_p_x, p_params, q_params, types_list, z_dim, y_dim_output, s_dim)
    
    optim = tf.compat.v1.train.AdamOptimizer(learning_rate).minimize(-ELBO)
    
    #Generator function for testing purposes
    samples_test, test_params, log_p_x_test, log_p_x_missing_test = model.samples_generator(batch_data_list, X_list, miss_list, types_list, batch_size, z_dim, y_dim_output, y_dim_partition, s_dim, tau, tau2, normalization_params)
    
    #Packing results
    tf_nodes = {'ground_batch' : batch_data_list,
                'ground_batch_observed' : batch_data_list_observed,
                'miss_list': miss_list,
                'tau_GS': tau,
                'tau_var': tau2,
                'samples': samples,
                'log_p_x': log_p_x,
                'log_p_x_missing': log_p_x_missing,
                'loss_re' : loss_reconstruction,
                'loss': -ELBO, 
                'optim': optim,
                'KL_s': KL_s,
                'KL_z': KL_z,
                'p_params': p_params,
                'q_params': q_params,
                'samples_test': samples_test,
                'test_params': test_params,
                'log_p_x_test': log_p_x,
                'log_p_x_missing_test': log_p_x_missing_test,
                'encoding':encoding}

    return tf_nodes
