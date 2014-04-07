#!/bin/bash

ls *.cpt > cpt.list

for nm in `awk -F: '{print $1}' cpt.list`
do
   oname=$nm #`echo $nm | cut -c4-`
   name=h5_$oname
   echo $name
   cp $nm /Users/brentminchew/Documents/Python/PySAR/pysar/plot/cpt/$name
done
rm -f cpt.list 
