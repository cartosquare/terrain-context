#!/bin/bash

../caffe/build/tools/caffe train -solver fine_tuning/solver.prototxt -weights ../caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel -gpu 0
