#!/bin/bash

../caffe/build/tools/caffe train -solver bvlc_googlenet/solver.prototxt -weights ./bvlc_googlenet/bvlc_googlenet.caffemodel -gpu 0
