#!/bin/bash

ls *.cpt > cpt.list

for nm in `awk -F: '{print $1}' cpt.list`
do
   pref=`echo $nm | cut -c-3`
   if [[ $pref == GMT ]]; then
      name=`echo $nm | cut -c5-`
      cp $nm $name
   fi
   
done
rm -f cpt.list
