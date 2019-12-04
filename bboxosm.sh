array_of_lines=("${(@f)$(cat bboxes.txt)}")

for line in $array_of_lines
do
wget -O "/osmfiles/$line.osm" "https://lz4.overpass-api.de/api/interpreter?data=way[\"highway\"~\"motorway|primary|trunk|motorway_link|trunk_link\"]($line);(._;>;);out geom;"
done
