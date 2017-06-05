#!/bin/bash
s=0
for ((a=0;a<100;a++))
do
	python setting_ships.py ships.txt
	python battleship_final2.py ships.txt no_of_moves.txt
	SUM=0
	for i in `cat no_of_moves.txt`
	do
		SUM=$(($SUM+$i))
	done	
	s=$(($SUM+$s))
done
echo $s/100 | bc -l