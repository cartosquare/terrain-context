#!/bin/bash

../caffe/build/tools/caffe train -solver vgg_tuning/solver.prototxt -weights ./vgg_tuning/VGG_ILSVRC_16_layers.caffemodel -gpu 0
