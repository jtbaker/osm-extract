#!/bin/zsh
files=(osmfiles/*.osm) 

for file in $files 
do
ogr2ogr -append -f PostgreSQL PG:"user=$fwpguser password=$fwpgpass host=$fwpghost dbname=FWGeos" $file lines -nln "osm_ways" -lco "FID=id" -lco "GEOMETRY_NAME=geom" -nlt PROMOTE_TO_MULTI
done