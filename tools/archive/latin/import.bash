#!/bin/bash

ar=$PWD/tools/archive/latin
glyphnames=$HOME/script/smithplus/etc/glyph_names/glyph_names.csv
import=$HOME/script/latn/font-andika/source/masters/Andika
scale="--scale 0.836"

for ufo in source/masters/*.ufo
do
    psfdeleteglyphs -i $ar/delete-prepare.txt $ufo
    $HOME/script/tools/ufo2glyphdata.py $HOME/script/adobe/agl-aglfn/aglfn.txt source/masters/*-Regular.ufo source/glyph_data.csv
    ./preflight
done

pushd source/masters
for weight in Bold Regular
do
    ufo=Nokyung-${weight}.ufo

    # first 3 glyphs
    $ar/import.py $ufo

    # prepare
    psfrenameglyphs -i $ar/rename-prepare.csv $ufo
    psfsetunicodes -i $ar/encode-prepare.csv $ufo

    # import
    latin=${import}-${weight}.ufo
    glyphs=$ar/import.csv
    psfgetglyphnames -i $ar/import.txt -a $glyphnames $latin $glyphs
    psfcopyglyphs --rename rename --unicode usv $scale -s $latin -i $glyphs -l tmp.log $ufo

    # cleanup
    psfdeleteglyphs -i $ar/delete-cleanup.txt $ufo
    psfrenameglyphs -i $ar/rename-cleanup.csv $ufo
    psfsetunicodes -i $ar/encode-cleanup.csv $ufo
    psfsetmarkcolors -i $ar/import.txt -u -c g_light_gray $ufo
    git restore $ufo/glyphs/four.glif

    # commit
    git add $ufo
    git commit -m "Improve character encoding in $weight"
    sleep 5
done
popd
