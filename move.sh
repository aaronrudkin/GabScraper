#!/bin/bash

cd /home/aaron/gab/posts
for i in 0 1 2 3 4 5 6 7 8 9
do 
	cd /home/aaron/gab/posts/$i
	for j in 0 1 2 3 4 5 6 7 8 9
	do
		mkdir $j$i
		mv *$j$i.json $j$i/
		cd /home/aaron/gab/posts/$i/$j$i
		for k in 0 1 2 3 4 5 6 7 8 9
		do
			pwd
			echo $k$j$i
			mkdir $k$j$i
			mv *$k$j$i.json $k$j$i/
		done
		cd ..
	done
done
