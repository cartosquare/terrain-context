#!/bin/bash

out='train/images'

# beijing
bjMinx=12940836.94
bjMaxx=12968345.889999999
bjMiny=4835676.160526317
bjMaxy=4867303.409473684

for ((i=17; i<=17; ++i))
do
    echo "process level $i"
    python download_tiles.py ${out} $i $bjMinx $bjMiny $bjMaxx $bjMaxy
done
