#!/bin/bash

dir="$1"
cd $dir
for z in *.zip;
  do unzip "$z" -d "${z%.*}";
done

rm *.zip