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


import pmt
import numpy as np
import time
from gnuradio import gr

class Traffic_Generator(gr.sync_block):
    """
    docstring for block Message Generator
    
    
    This block generates data to be transmitted artificial combining
    values intervals of time and length of the data.

    Amount of data to be sent selectable in "Num messages" > 0 or infinite for "Num messages" = -1  

    Requires at least one exteno paramentro, "Length" or "Interval"

    "Length" or "Interval"> 0 the block takes the value itself    
    
    """
    def __init__(self, Interval, Length, Num):
        gr.sync_block.__init__(self,
            name="Traffic_Generator",
             in_sig=None,
             out_sig=None)
        self.interval = Interval
        self.length = Length
        self.num = Num  
             
        self.message_port_register_out(pmt.intern('msg_out'))
        self.message_port_register_in(pmt.intern('Interval'))
        self.message_port_register_in(pmt.intern('Length'))
        
        if self.interval == 0 and self.length == 0:
            self.set_msg_handler(pmt.intern("Interval"), self.handle_msg)
        elif self.interval == 0 and self.length != 0:
            self.set_msg_handler(pmt.intern("Interval"), self.handle_interval)
        elif self.interval != 0 and self.length == 0:
            self.set_msg_handler(pmt.intern("Length"), self.handle_length)
        else:
            print "Wrong block use Traffic_Generate_Random"
        
    def handle_msg(self, msg):
        self.interval = int(pmt.to_float(msg))
        self.set_msg_handler(pmt.intern("Length"), self.handle_length)
        
    def handle_interval(self,msg):
        self.interval = int(pmt.to_float(msg))
        self.send_msg(self.length, self.interval, self.num)
    
    def handle_length(self,msg):
        self.length = int(pmt.to_float(msg))
        self.send_msg(self.length, self.interval, self.num)
        
   
    def message_generat(self, length):
        alfabeto='abcdefghijklmnopqrstuvwxyz 0123456789'
        msg=''
        for i in range (0,length):
            msg+=alfabeto [np.random.randint(0,len(alfabeto))]
        msg+='\n'
        return msg
	
    def send_msg(self, length, interval, num): #envia sempre a mesma mensagem aleatoria gerada
        msg = self.message_generat(length)    
        while num > 0 or num < 0 :
            self.message_port_pub(pmt.intern('msg_out'), pmt.to_pmt(msg))
            time.sleep(interval/1000.0)
            num = num - 1    
        self.message_port_pub(pmt.intern('msg_out'), pmt.PMT_EOF)
