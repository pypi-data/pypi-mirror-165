#!/usr/bin/env python
# coding: utf-8
# Copyright (C) 2020 Miriam Cabero
# Edited by Man Leong Chan 2022

# import necessary libraries

from ligo.skymap import io
import numpy, tensorflow, os
from astropy.io import fits
from reproject import reproject_from_healpix
from scipy import interpolate


# Target header for reproject_from_healpix
# This will be used for reprojecting the skymaps from FITS file to a more manageable size
target_header = fits.Header.fromstring("""
NAXIS   =                    2
NAXIS1  =                  360
NAXIS2  =                  180
CTYPE1  = 'RA---CAR'
CRPIX1  =                180.5
CRVAL1  =                180.0
CDELT1  =                   -1
CUNIT1  = 'deg     '
CTYPE2  = 'DEC--CAR'
CRPIX2  =                 90.5
CRVAL2  =                  0.0
CDELT2  =                    1
CUNIT2  = 'deg     '
COORDSYS= 'icrs    '
""", sep='\n')


# these set the default model name and path to fetch the relevant model files

# added links for models and weights (15th Aug 2022)
# GWSkyNet_v1            : model in the original paper

# GWSkyNet_v2 performance: https://ldas-jobs.ligo.caltech.edu/~manleong.chan/test_output/2022-05-24-11-29-11/
# GWSkyNet_v2 model      : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-05-24-11-29-11/model.json
# GWSkyNet_v2 weight     : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-05-24-11-29-11/logs/best_weights.h5

# GWSkyNet_v3 performance: https://ldas-jobs.ligo.caltech.edu/~manleong.chan/test_output/raw_data/2022-07-04-08-19-30/Epoch_10-VL_0.1632-VA_0.9513-TL_0.1542-TA_0.9545/
# GWSkyNet_v3 model      : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-07-04-08-19-30/model.json
# GWSkyNet_v3 weight     : https://ldas-jobs.ligo.caltech.edu/~manleong.chan/GWSkyNet-retraining/raw_data/2022-07-04-08-19-30/weights/Epoch_10-VL_0.1632-VA_0.9513-TL_0.1542-TA_0.9545.h5

model_names = ['GWSkyNet_v1', 'GWSkyNet_v2', 'GWSkyNet_v3'] # added GWSkyNet_v3 on 15th Aug 2022
model_path  = os.path.join(os.path.dirname(__file__), 'GWSkyNet_data', 'models')
rate_path   = os.path.join(os.path.dirname(__file__), 'GWSkyNet_data', 'rates')

model_name  = 'GWSkyNet_v3'  # the model that is actually used.

# when training the GWSkyNet model, a few normalization factors are derived from the corresponding training data set by
# taking the absolute maximum values of the corresponding values of the training samples.
# for example, the training norm "distance" is the maximum value of the posterior mean distances (Mpc) for all samples,
# and "skymap" is the maximum value from the sky location posteriors for all training samples.
# These factors will also be applied to testing data or real data to be consistent.

# These factors are saved in model/training_norms.txt

tnf                     = open(os.path.join(model_path, 'training_norms.txt'), 'r')
tnf_content             = tnf.readlines()
training_norms_keywords = tnf_content[0].split()
training_norms_values   = tnf_content[1:]
tnf.close()

model_index             = [i for i, s in enumerate(training_norms_values) if model_name in s][0]
training_norms          = training_norms_values[model_index].split()

# select the training norms based on the model selected because the training normalization factors are derived from
# different training sets.
training_norms          = {training_norms_keywords[i] : float(training_norms[i]) for i in range(1, len(training_norms))}

if not model_name in model_names:
    raise Exception('Requested GWSkyNet model does not exist: %s.'%(model_name))

def nan_invalid(data, invalid_value):
    """Turn invalid values into numpy.nan"""
    invalid_indices = numpy.where(data==invalid_value)
    for idx in invalid_indices:
        data[idx] = numpy.nan
    return data


# added a function to normalize values to a given range (added on 15th Aug 2022)
def normalized(value, norm_min, norm_max, data_min, data_max):
    
    """
    Function to normalize value to a given range.
   
    Input :
    
    value    : value to be normalized.
    norm_min : the minimal value of the range to which the value will be normalized.
    norm_max : the maximal value of the range to which the value with be normalized.
               i.e., the value will be normalized to [norm_min, norm_max]

    data_min : the minimal value of the data set to which value belongs.
    data_max : the maximal value of the data set to which value belongs.
   
    Output :
    
    norm     : the normalized value
    """
  
    norm = (norm_max - norm_min) * (value - data_min) / (data_max - data_min) + norm_min
    
    return norm

def prepare_data(fits_file):
    """Pre-processing data from FITS file for GWSkyNet"""
    
    # read FITS file. GWSkyNet only works with FITS file generated using Bayestar
    # as GWSkyNet uses the distance information so "distsances" is set to be true.
    
    skymap, metadata = io.read_sky_map(fits_file, distances=True, nest=None)
    
    #verify the skymap is generated using ligo.skymap
    if not metadata['creator'] == 'BAYESTAR':
        raise Exception ('The input skymap is not generated using ligo.skymap. GWSkyNet is only able to work FITS file generated using ligo.skymap.')
    
    
    # Distance must be normalized by maximum in the training set
    distance = metadata['distmean'] / training_norms['distance']
    
    network = metadata['instruments']
    
    # Convert detector network to multi-hot format
    # 1 means a detector contributed to the identification of an alert,
    # 0 means a detector did not contribute.
    dets = []
    for ifo in ['H1', 'L1', 'V1']:
        dets.append(1) if ifo in network else dets.append(0)
        
    # Read data columns from FITS file
    # invalid_values = {'Distmu':numpy.inf, 'Distsigma':1., 'Distnorm':0.}
    # (convention described in Table 1 of https://arxiv.org/pdf/1605.04242.pdf)
    fits_cols = {'skymap':skymap[0],
                 'distmu':nan_invalid(skymap[1], numpy.inf),
                 'distsigma':nan_invalid(skymap[2], 1.),
                 'distnorm':nan_invalid(skymap[3], 0.)}
    
    # Reproject and downsample each column
    img_data, norms = dict(), dict()
    for column in fits_cols:
        with numpy.errstate(invalid='ignore'):
            img, mask = reproject_from_healpix((fits_cols[column], 'ICRS'),
                                       target_header, nested=metadata['nest'], hdu_in=None,
                                       order='bilinear', field=0)
        
        # Replace NaN with zero and normalize img data
        img = numpy.nan_to_num(img)
        norms[column] = numpy.max(abs(img))
        img = img / norms[column]
        
        # Normalize norms by maximum in the training set
        norms[column] /= training_norms[column]
        
        # Downsample img data using maxpooling
        # the reshape is done to accommodate the format of an input to a tensorflow CNN model
        # [batch_no, image height, image width, channel]
        x = numpy.reshape(img, (1, len(img), len(img[0]), 1))
        
        # convert the numpy array to a tensor and downsample using maxpool
        x = tensorflow.cast(x, tensorflow.float32)
        maxpool = tensorflow.keras.layers.MaxPooling2D(pool_size=(2, 2))
        img_data[column] = maxpool(x)
        
    # added on 15th Aug 2022
    log_bci = normalized(metadata['log_bci'], -1, 1, training_norms['logbci_min'], training_norms['logbci_max'])
    log_bsn = numpy.log10(normalized(metadata['log_bsn'], 0.1, 10, training_norms['logbsn_min'], training_norms['logbsn_max']))
    
    # Stack volume images
    dist_columns = ['distmu', 'distsigma', 'distnorm']
    stacked_volume = numpy.stack([numpy.reshape(img_data[column], (1, 90, 180)) for column in dist_columns], axis=-1)

    return [stacked_volume, img_data['skymap'], numpy.reshape(dets, (1,3)), numpy.reshape(distance, (1,1)),
            numpy.reshape(norms['skymap'], (1,1)), numpy.reshape(norms['distmu'], (1,1)),
            numpy.reshape(norms['distsigma'], (1,1)), numpy.reshape(norms['distnorm'], (1,1)),
            numpy.reshape(log_bci, (1, 1)),             numpy.reshape(log_bsn, (1, 1))]


# In[5]:


def predict(loaded_model, data):
    """Use loaded model to predict result
    
    Keyword arguments:
    loaded_model: machine-learning model to use for prediction
    data: pre-processed data from FITS file
    threshold: real-noise threshold to predict real events (typically 0.5)
    """
    # apply the model to data
    prediction = tensorflow.squeeze(loaded_model(data), [-1]).numpy()

    return prediction

# edited on 15th Aug 2022 to make v3 as the default
def get_rates(class_score, model = model_name):
    
    # check if model is one of the models for which FAR and FNR can be estimated.
    if not 'v3' in model_name:
        
        raise Exception('Sorry, estimates of false positive rate and false negative rate currently works only with v3, while the requested model is %s.'%(model_name))
            
    else:
    # if yes, then read the corresponding rates
       temp       = numpy.genfromtxt(os.path.join(rate_path, '%s_rates.txt'%(model)), delimiter = '\t', comments = '#')
       thresholds = temp[:, 0]
       FARs       = temp[:, 1]
       FNRs       = temp[:, 2]
    
       # interpolate FAR and FNR for a given class score
       # if the class_score is less than the smallest value (threshold) in the rate txt file, just return the rates corresponding to
       # the smallest value (threshold) in the data because interpolation would then actually be exterpolation
       
       FAR_fun    = interpolate.interp1d(thresholds, FARs, bounds_error=False, fill_value=(FARs[0], FARs[-1]))
       FNR_fun    = interpolate.interp1d(thresholds, FNRs, bounds_error=False, fill_value=(FNRs[0], FNRs[-1]))
       
       far        = FAR_fun(class_score)
       fnr        = FNR_fun(class_score)
       
       return far, fnr
        
# In[25]:


def load_GWSkyNet_model(model_path = model_path, model_name = model_name):
    """Function to load the trained GWSkyNet model"""
    
    # check if the input model name has been defined earlier.
    if not model_name in model_names:
        raise ValueError('\n *** The input model name is not one of the available model names for the GWSkyNet classifier.')
    
    # the model file (architecture file and weight should use the same names).
    model_archi   = os.path.join(model_path, model_name + '.json')
    model_weights = os.path.join(model_path, model_name + '.h5') 
    
    # raises if the relevant files are not found
    if not os.path.exists(model_archi):
        raise FileNotFoundError('\n *** The model architecture file %s does not exist. ' %(model_archi))
    
    if not os.path.exists(model_weights):
        raise FileNotFoundError('\n *** The model weight file %s does not exist. ' %(model_weights))
        
    # if the files are found, load the model and the weights
    with open(model_archi, 'r') as f:
        json_model = f.read()
        
    model = tensorflow.keras.models.model_from_json(json_model)
    model.load_weights(model_weights)
    
    return model
