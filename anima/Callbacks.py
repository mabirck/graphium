#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import keras.callbacks as callbacks
from system.Helper import Helper
from system.Configuration import Configuration

class JSONMetrics(callbacks.Callback):
    
    _helper     = None
    _serial     = None
    _config     = None
    _model      = None
    _each_epoch = None
    _metrics    = None
    _epoch      = None
    
    def __init__(self,model,each_epoch):
        self._helper    = Helper()
        self._config    = Configuration()
        self._serial    = self._helper.getSerialNow()
        
        self._file_json = self._config.output_folder+self._serial+"_menesis_metrics.json"
        self._model     = model
        self._each_epoch= each_epoch
        self._epoch     = 0
        self._metrics   = {'loss':[], 'acc':[]}
        
    def on_epoch_begin(self, epoch, logs):
        try:
            with open(self._file_json, 'r') as f:   
                self._metrics = json.load(f)
        except:
            with open(self._file_json, 'w') as f:
                self._metrics = {'loss':[], 'acc':[]}
                json.dump(self._metrics, f)
 			
    def on_epoch_end(self, epoch, logs):
        self._metrics['loss'].append(logs.get('loss'))
        self._metrics['acc'].append(logs.get('acc'))
        with open(self._file_json, 'w') as f:
            data = json.dump(self._metrics, f)
            
        if self._epoch % self._each_epoch == 0:
            
            file_name = self._config.output_folder+self._serial+'_weights%08d.h5' % self._epoch
            print 'Salving weights at',file_name
            self._model.save_weights(file_name)
        self._epoch += 1