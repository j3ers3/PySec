#!/bin/bash

for p in 98.13{6..9}.{0..255}.{0..255}; do
wget -t 1 -T 5 http://${ip}/phpinfo\(\); done 


