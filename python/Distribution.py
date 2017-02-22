#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 
#
# Desenvolvido pelo Laboratória de Engenharia e Sistemas de Computação (Lesc)
# Universidade Federal de Viçosa -Campus Florestal - MG 
# Kristtopher Kayo Coelho Graduando em Ciência da Computação


import numpy as np
from gnuradio import gr
import pmt
import math

class Distribution(gr.sync_block):
    """
    docstring for block Dist
    
    shape : float, > 0.
    Shape of the distribution Pareto,
    weibull and zipf is equivalent "a"
    Shape of the distribution poisson shape is equivalent "lam"
    
    pareto(a = Shape, size = 1)
    weibull(a = Shape, size = 1)
    zipf(a = Shape, size = 1)
    poisson(lam = Shape, size = 1)
    
    uniform(low = Min, high = Max, size = 1)

    
    This block is capable of generating random values 
    following models distributions listed above.

    It has selectable output in the types:
    complex, int and float 
    besides having fixed output type message pdu    
    """
    def __init__(self, Min, Max, Model, Shape, Type):
 
        self.minimo = Min
        self.maximo = Max
        self.shape = Shape  
        self.flag = 0

        if Type == int:
            self.type = np.int32
        elif Type == float:
            self.type = np.float32
        elif Type == complex:
            self.type = np.complex64     
        
        if Model == 0:
            self.model = 'Poisson'
        elif Model == 1:
            self.model = 'Pareto'
        elif Model == 2:
            self.model = 'Weibull'
        elif Model == 3:
            self.model = 'Zipf'
        elif Model == 4:
            self.model = 'Uniforme'
        
        gr.sync_block.__init__(self,
            name="Distribution",
            in_sig=None,
            out_sig=[self.type])
        
        self.message_port_register_out(pmt.intern('out_msg')) 


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
        if self.flag == 0:              
            out[:] = self.principal(self.model,self.minimo,self.maximo, self.shape)
            self.flag = 1
        return len(output_items[0])
        
    def poisson(self,lower,upper,shape):
        poisson = np.random.poisson(shape,1)
        return float(poisson)
        
    def weibull(self,lower,upper,shape):
        wei = np.random.weibull(shape, 1)
        return float(wei)
    
    def zipf(self,lower,upper,shape):
        zi = np.random.zipf(shape, 1)
        return float(zi)
          
    def generat(self):
        rand = 0
        rand = np.random.randint(self.minimo,self.maximo)
        return rand
	
    def uniforme(self,lower,upper,shape):
        uni = np.random.uniform(lower,upper, 1)
        return float(uni)
	
    def pareto(self,lower,upper,shape):
	    x = []
	    while len(x) < 1:
		    x = np.random.pareto(shape, 1) + lower
		    x = x[x < upper][:1]
	    return float(x[0])
	
    def principal(self, model, minimo, maximo, shape):
        if model == 'Poisson':
            value = self.poisson(minimo, maximo, shape)
            if value < 1:
                value = math.ceil(value)
            self.message_port_pub(pmt.intern('out_msg'), pmt.to_pmt(value))
        elif model == 'Pareto':
            value = self.pareto(minimo, maximo, shape)
            if value < 1:
                value = math.ceil(value)
            self.message_port_pub(pmt.intern('out_msg'), pmt.to_pmt(value))
        elif model == 'Weibull':
            value = self.weibull(minimo, maximo, shape)
            if value < 1:
                value = math.ceil(value)
            self.message_port_pub(pmt.intern('out_msg'), pmt.to_pmt(value))
        elif model == 'Zipf':
            value = self.zipf(minimo, maximo, shape)
            if value < 1:
                value = math.ceil(value)
            self.message_port_pub(pmt.intern('out_msg'), pmt.to_pmt(value))
        elif model == 'Uniforme':
            value = self.uniforme(minimo, maximo, shape)
            if value < 1:
                value = math.ceil(value)
            self.message_port_pub(pmt.intern('out_msg'), pmt.to_pmt(value))
        return value