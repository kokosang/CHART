#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Collectrtldata
# Generated: Tue Aug 14 16:42:11 2018
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import chart
import osmosdr
import time
import datetime
import numpy as np
import pprint
from ast import literal_eval


class collectrtldata(gr.top_block):

    def __init__(self, c_freq):
        gr.top_block.__init__(self, "Collectrtldata")

        ##################################################
        # Variables
        ##################################################
        self.veclength = veclength = 1024
        self.samp_rate = samp_rate = 2e6
        self.c_freq = c_freq
        self.int_length = 100
        self.data_file = '/home/locorpi3b/data/' + str(datetime.datetime.now()).replace(' ', '_') + '.dat'
        self.data_file = self.data_file.replace(':', '-')
        self.metadata_file = self.data_file[:-3] + 'metadata.npz'
        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(c_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(45, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.fft_vxx_0 = fft.fft_vcc(veclength, True, (window.blackmanharris(1024)), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, 1024)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, veclength)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(self.int_length, veclength)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, veclength*100*100)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*veclength, self.data_file, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(veclength)
        self.chart_meta_trig_py_ff_0 =chart.meta_trig_py_ff(veclength)
        ##################################################
        # Connections
        ##################################################
        self.connect((self.chart_meta_trig_py_ff_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))    
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_integrate_xx_0, 0), (self.chart_meta_trig_py_ff_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        #self.connect((self.blocks_vector_to_stream_0, 0), (self.chart_meta_trig_py_ff_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_head_0, 0))    

        self.start_time = time.time()


    def get_veclength(self):
        return self.veclength

    def set_veclength(self, veclength):
        self.veclength = veclength
        self.blocks_head_0.set_length(self.veclength*100*100)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def parameters(self):
        d={'date': str(datetime.date.today()),
           'start_time': time.time(), 
           'samp_rate': self.samp_rate,
           'frequency': self.c_freq,
           'vector_length': self.get_veclength(),
           'int_length': self.int_length,
           #data file (.dat file it refers to)
           'data_file': self.data_file,
           #print after every integration. 100 d for each c_freq
           'metadata_file': self.metadata_file,
           'times': self.chart_meta_trig_py_ff_0.get_l()
          }
        return d

    def meta_save(self):
        np.savez(self.metadata_file,
           date = str(datetime.date.today()),
           start_time = self.start_time,
           end_time = time.time(), 
           samp_rate = self.samp_rate,
           frequency = self.c_freq,
           vector_length = self.get_veclength(),
           int_length = self.int_length,
           #data file (.dat file it refers to)
           data_file = self.data_file,
           #print after every integration. 100 d for each c_freq
           metadata_file = self.metadata_file,
           times = self.chart_meta_trig_py_ff_0.get_l())

def main(top_block_cls=collectrtldata, options=None):
    #d = dict()
    for c_freq in range(50*10**6, 52*10**6, 2*10**6):
    #if self.c_freq%100==0: 
        tb = top_block_cls(c_freq)
        tb.start()
        #d = tb.parameters()
        tb.wait()
        #d['end_time'] = time.time()
        tb.meta_save()
        del(tb)  
        #print(d)      
        #np.savez(d['metadata_file'], d)

if __name__ == '__main__':
    main()