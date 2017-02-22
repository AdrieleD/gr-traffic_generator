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
# Desenvolvido pelo Laboratória de Engenharia e Sistemas de Computação (Lesc)
# Universidade Federal de Viçosa -Campus Florestal - MG 
# Kristtopher Kayo Coelho Graduando em Ciência da Computação

import numpy as np
from gnuradio import gr
import time
import pmt
import math

class Traffic_Generator_Random(gr.sync_block):
    """
    docstring for block Generate
    
    This block generates data to be transmitted artificial combining
    values intervals of time and length of the data.

    Amount of data to be sent selectable in "Num messages" > 0 or infinite for "Num messages" = -1    
    
    The parameters "Length" or "Interval" can take values from distributions blocks
    or internal values
    
    Random messages are generated every transmission
    
    """
    def __init__(self, Interval, Length, Num, Type):
        
        if Type == int:
            self.type = np.int32
        elif Type == float:
            self.type = np.float32
        elif Type == complex:
            self.type = np.complex64 
        self.inter = Interval
        self.len = Length
        self.num = Num
        
        gr.sync_block.__init__(self,
            name="Traffic_Generator_Random",
            in_sig=[self.type, self.type],
            out_sig=None)
            
        self.message_port_register_out(pmt.intern('msg_out'))
        
    def work(self, input_items, output_items):
        
        if np.iscomplexobj(input_items[0]): # converte de numero complexo para real
            inInter = np.real(input_items[0])
            inLen = np.real(input_items[1])
        else:
            inInter = input_items[0]
            inLen = input_items[1]

        if self.inter == 0 and self.len ==0:   #gera uma mensagem aleatoria pra cada envio
            while self.num > 0 or self.num < 0: 
                self.send_msg(int(math.ceil(inLen[0])), float(inInter[0]))
                self.send_EOF(self.num)
                self.num = self.num - 1 
        elif self.inter != 0 and self.len ==0:
            while self.num > 0 or self.num < 0: 
                self.send_msg(int(math.ceil(inLen[0])), self.inter)
                self.send_EOF(self.num)
                self.num = self.num - 1 
        elif self.inter == 0 and self.len !=0:
            while self.num > 0 or self.num < 0: 
                self.send_msg(self.len, float(inInter[0]))
                self.send_EOF(self.num)
                self.num = self.num - 1 
        elif self.inter != 0 and self.len !=0:
            while self.num > 0 or self.num < 0: 
                self.send_msg(self.len, self.inter)
                self.send_EOF(self.num)
                self.num = self.num - 1 
        else:
            while self.num > 0 or self.num < 0: 
                self.message_port_pub(pmt.intern('msg_out'), pmt.to_pmt('missing argument'))
                self.send_EOF(self.num)                
                self.num = self.num - 1 
        return len(input_items[0])
        
    def message_generat(self, length):
        alfabeto='abcdefghijklmnopqrstuvwxyz 0123456789'
        msg=''
        for i in range (0,length):
            msg+=alfabeto [np.random.randint(0,len(alfabeto))]
        msg+='\n'
        return msg
	
    def send_msg(self, length, interval):
        msg = self.message_generat(length)
        self.message_port_pub(pmt.intern('msg_out'), pmt.to_pmt(msg))
        time.sleep(interval/1000)

    def send_EOF(self, num):
        if num == 1:
            self.message_port_pub(pmt.intern('msg_out'), pmt.PMT_EOF)