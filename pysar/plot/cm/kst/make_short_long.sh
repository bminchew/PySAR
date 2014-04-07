#!/bin/bash

ls *.cpt > cpt.list

for nm in `awk -F: '{print $1}' cpt.list`
do
   pref=`echo $nm | cut -c-2`
   name=`echo $nm | cut -c4-`
   echo $nm $pref.cpt $name
   cp $nm $name
done
rm -f cpt.list
