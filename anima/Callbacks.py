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
    metrics     = None
    
    def __init__(self,model,each_epoch):
        self._helper    = Helper()
        self._config    = Configuration()
        self._serial    = self._helper.getSerialNow()
        
        self._file_json = config.output_folder+self._serial+"_menesis_metrics.json"
        self._model     = model
        self._each_epoch= each_epoch
        self._batch     = 0
        self.metrics    = {'loss':[], 'acc':[]}
        
    def on_epoch_begin(self, epoch, logs):
        try:
            with open(self._file_json, 'r') as f:   
                self.metrics = json.load(f)
        except:
            with open(self._file_json, 'w') as f:
                self.metrics = {'loss':[], 'acc':[]}
                json.dump(self.metrics, f)
 			
    def on_epoch_end(self, epoch, logs):
        self.metrics['loss'].append(logs.get('loss'))
        self.metrics['acc'].append(logs.get('acc'))
        with open(self._file_json, 'w') as f:
            data = json.dump(self.metrics, f)
    
    def on_batch_end(self, batch, logs={}):
        if self._batch % self._each_epoch == 0:
            print 'Salving weights'
            file_name = config.output_folder+self._serial+'_weights%08d.h5' % self.batch
            self._model.save_weights(file_name)
        self._batch += 1