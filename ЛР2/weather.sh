#!/bin/bash
if [[ "$1" != "" ]]; then
    LATIT="$1"
else
    LATIT="58.00675"
fi
if [[ "$2" != "" ]]; then
    LONGIT="$2"
else
    LONGIT="56.22857"
fi
echo $LATIT
echo $LONGIT
OUTPUT_FILE="/var/www/html/index.nginx-debian.html"
echo $1
#echo "wttr.in/$1?format=j1"

# output to index file
#sudo echo $(curl  "wttr.in/$1?format=j1" | jq '.["current_condition"][0] | .localObsDateTime, .temp_C, .humidity') > "<p>$OUTPUT_FILE</p>"

#output to ndex file
sudo curl "https://api.open-meteo.com/v1/forecast?latitude=$LATIT&longitude=$LONGIT&current=temperature_2m,relative_humidity_2m" | jq '. | [.current.time, .current.temperature_2m, .current_units.temperature_2m[1:], .current.relative_humidity_2m, .current_units.relative_humidity_2m] | join(" ")' > "$OUTPUT_FILE"