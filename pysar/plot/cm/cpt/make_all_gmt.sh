#!/bin/bash

for nm in `awk -F: '{print $1}' gmt_colors.list`
do
   force=-Fr
   points=256
   if [[ $nm == rainbow || $nm == topo || $nm == sealand ]]; then
      force=-Fh
   fi
   if [[ $nm == globe || $nm == topo || $nm == relief ]]; then
      points=1024
   fi
   echo "makecpt -C$nm.cpt -T0/$points/1 $force > gmt_$nm.cpt"
   makecpt -C$nm.cpt -T0/$points/1 $force > gmt_$nm.cpt
done
