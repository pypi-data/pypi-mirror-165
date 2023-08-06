#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:16:32 2022

@author: benjamin
"""

import numpy as np
from shapely.geometry import LineString

class Contour:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=pointless-string-statement

    contours = None
    lips = None
    length = None
    tract_variables = {"tongue body" : {"degree" : None, "location" : None},
                       "tongue tip" : {"degree" : None, "location" : None},
                       "lip" : {"aperture" : None, "protrusion" : None},
                       "length": None}

    # Constructor method
    def __init__(self, *args):
        nargin = len(args)
        for k in range(0, nargin, 2):
            key, value = args[k:k+2]
            setattr(self, key, value)
            
    def compute_lip_variables(self):
        
        self.tract_variables["lip"]["aperture"] = get_lip_aperture(self)
        self.tract_variables["lip"]["protrusion"] = get_lip_protrusion(self)
            
    def compute_tongue_variables(self, origin=(10,10)):
        
        distance, thetas = self.get_distance(origin)
        for key_1, tr in zip(["tongue tip", "tongue body"],
                           [(110, 140), (0, 105)]):
            tr_var = extract_degloc(distance, thetas, tr)
            for key_2, value in zip(["degree", "location"], tr_var): 
                self.tract_variables[key_1][key_2] = value 
                
    def compute_tract_variables(self, c, origin=(10,10)):
        
        self.compute_lip_variables()
        self.compute_tongue_variables(origin)
        self.tract_variables["length"] = get_length(self, c)
                
    def get_distance(self, origin):
        
        thetas, xvecs = make_vecs(origin)
        lines = self.make_lines()
        distance_vec = []
        
        for n, theta in enumerate(thetas):
            second_line = make_angle_line(theta, xvecs, origin)
            intersections = [second_line.intersection(l) for l in lines]
            if all([ints.geom_type == "Point" for ints in intersections]):
                inner_point, outer_point = [get_points(ints) for ints in intersections]                       
                distance_vec.append(np.sqrt(np.sum((inner_point-outer_point)**2)))

        return distance_vec, thetas
    
    def interpolation(self, factor=1000):
        
        inner_x, inner_y, outer_x, outer_y = self.contours
        new_inner = interpol_contour(inner_x, inner_y, factor)
        new_outer = interpol_contour(outer_x, outer_y, factor)
        self.contours = (new_inner[0], new_inner[1], new_outer[0], new_outer[1])
        
    def make_lines(self):
        
        inner_x, inner_y, outer_x, outer_y = self.contours
        return (LineString(np.column_stack((inner_x, inner_y))),
                LineString(np.column_stack((outer_x, outer_y))))
    
def extract_degloc(distance, thetas, theta_range):
    
    th_deg = thetas * 180 / np.pi
    idx = [x for x in range(len(thetas)) if th_deg[x] >= theta_range[0] and 
              th_deg[x] <= theta_range[1]]

    distance_tract = [distance[i] for i in idx]
    constriction_degree = np.min(distance_tract)
    constriction_location = (180 - th_deg[idx[np.argmin(distance_tract)]])
    
    return constriction_degree, constriction_location

def extract_task_variables(contour, c, origin=(10,10)):
    
    try:
        contour.compute_tract_variables(c, origin)
        tracts = contour.tract_variables
        
        return [tracts["lip"]["aperture"], 
                  tracts["lip"]["protrusion"],
                  tracts["tongue tip"]["degree"], 
                  tracts["tongue tip"]["location"],
                  tracts["tongue body"]["degree"], 
                  tracts["tongue body"]["location"],
                  tracts["length"]]
    except:
        return [np.nan]*7

def get_length(contour, c):
    
    inner_x, inner_y, outer_x, outer_y = contour.contours
    x1 = -(np.diff(inner_x)+np.diff(outer_x))/100
    y1 = -(np.diff(inner_y)+np.diff(outer_y))/100
    d = 0.5*np.sqrt(x1**2 + y1**2)
    return np.sum(c*d)
    

def get_lip_aperture(contour):
    inner_x, inner_y, outer_x, outer_y = contour.contours
    y_upper_lip = outer_y[np.argmin(outer_x)]
    y_lower_lip = inner_y[np.argmin(inner_x)]
    return np.abs(y_upper_lip - y_lower_lip)

def get_lip_protrusion(contour):
    inner_x, inner_y, outer_x, outer_y = contour.contours
    x = np.sort(inner_x)
    return x[1] - x[0]

def get_points(intersection):
    return np.array([intersection.xy[k][0] for k in [0,1]])

def interpol_contour(x_coor, y_coor, D=1000):
    new_x = []
    new_y = []

    for n in range(len(x_coor)-1):
        x1, x2 = x_coor[n:n+2]
        y1, y2 = y_coor[n:n+2]
        
        x_vec = np.linspace(x1, x2, D)
        y_vec = np.linspace(y1, y2, D)
        if n == 0:
            s = 0
        else:
            s = 1
        
        for x, y in zip(x_vec[s:], y_vec[s:]):
            new_x.append(x)
            new_y.append(y)
            
    return new_x, new_y

def make_angle_line(theta, xvecs, origin):    
    a = np.sign(np.cos(theta)) * np.sqrt(1/np.cos(theta)**2 - 1)
    b = origin[1] - a * origin[0]
    xvec = xvecs[1-(a>=0)]            
    line = a * xvec + b
    return LineString(np.column_stack((xvec, line)))

def make_vecs(origin):
    return (np.linspace(0, 140, 1401) * np.pi/180, 
            (np.linspace(origin[0], 20, 5), 
            np.linspace(0, origin[0], 5)))


    
        