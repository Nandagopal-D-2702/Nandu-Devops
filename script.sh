#!/bin/bash

for i in linux git jenkins docker kubernetes terraform
do
	mkdir $i
	touch $i/Notes.md
done

