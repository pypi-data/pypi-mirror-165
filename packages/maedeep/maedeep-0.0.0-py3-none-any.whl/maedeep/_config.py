#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:01:43 2022

@author: benjamin
"""

import sys
import os


def get_maedeep_path():
    return [x for x in sys.path if x.endswith("maedeep") if 
            os.path.isdir(os.path.join(x, "parametric_models"))][0]

def get_maedeep_model():
    return os.path.join(get_maedeep_path(), "parametric_models", 
                        "model_spec.json")
