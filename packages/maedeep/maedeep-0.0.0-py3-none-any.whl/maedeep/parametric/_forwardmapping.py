#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:04:55 2022

@author: benjamin
"""

import numpy as np
from maedeep._areafunction import (AreaFunction)
from maedeep._waveguide import Waveguide
from maedeep._contour import extract_task_variables
from .modeltools import check_model, contour_to_area_function, vector_to_contours

def area_to_formant(area_function):
    wvg = Waveguide("area_function", area_function)
    wvg.computetransferfunction()
    return wvg.computeformants()

def area_to_transfer_function(area_function, df=50):
    wvg = Waveguide("area_function", area_function)
    return wvg.computetransferfunction(df=df)
    
def contour_to_area(contours, model=None):
    
    data = check_model(model)
    
    size_correction = data["semi-polar coordinates"]["size correction"]
    alph, beta = [data["semi-polar coordinates"]["sagittal-area coefficients"][key]
                       for key in ["alpha", "beta"]]
    vp_map = data["semi-polar coordinates"]["map coeff"]
    iniva_tng = int(data["tongue"]["parameters"]["initial point"])
    c = size_correction * vp_map
    
    afs = [contour_to_area_function(contour, c, iniva_tng, alph, beta) 
              for contour in contours]
    
    AF = AreaFunction("area", np.array([x["area"] for x in afs]).T,
                      "length", np.array([x["length"] for x in afs]).T)

    AF.interpolate(40)
    return AF

def articulatory_to_area(articulatory_parameters, model=None):    
    contours = articulatory_to_contour(articulatory_parameters, model)
    area_function = contour_to_area(contours, model)
    return area_function

def articulatory_to_contour(articulatory_parameters, model=None):
    return vector_to_contours(articulatory_parameters, model)

def articulatory_to_formant(articulatory_parameters, model=None):
    return area_to_formant(articulatory_to_area(articulatory_parameters, 
                                                model=model))    

def articulatory_to_task(articulatory_parameters, model=None, verbosity=False):
    data = check_model(model)    
    size_correction = data["semi-polar coordinates"]["size correction"]    
    vp_map = data["semi-polar coordinates"]["map coeff"]
    c = size_correction * vp_map
    return contour_to_task(articulatory_to_contour(articulatory_parameters, model), 
                            c, verbosity=verbosity)

def articulatory_to_transfer_function(articulatory_parameters, model=None, 
                                      df=50):
    return area_to_transfer_function(articulatory_to_area(articulatory_parameters, 
                                                    model), df=df)

def contour_to_formant(contours, model=None):
    return area_to_formant(contour_to_area(contours, model))
    
def contour_to_task(contours, c, verbosity=False):
    if verbosity:
        from tqdm import tqdm
        return np.array([extract_task_variables(ctr, c) for ctr in tqdm(contours)]).T
    else:
        return np.array([extract_task_variables(ctr, c) for ctr in contours]).T

def contour_to_transfer_function(contours, model=None, df=50):
    return area_to_transfer_function(contour_to_area(contours, model), df=df)

def transfer_function_to_formant(transfer_function, freq):
    wvg = Waveguide("transfer_function", transfer_function,
                    "freq", freq)
    return wvg.computeformants()



        
    
    
    

