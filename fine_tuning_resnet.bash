#!/bin/bash

../caffe/build/tools/caffe train -solver resnet/solver.prototxt -weights ./resnet/ResNet-152-model.caffemodel -gpu 0
