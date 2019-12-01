#!/bin/bash
set -e

../indent-sort.py -h >/dev/null
../indent-sort.py --help >/dev/null
../indent-sort.py -v >/dev/null
../indent-sort.py --version >/dev/null
while read file; do
    base=$(basename $file .correct)
    original=$base.orig
    echo "Test: $base"
    param=$(echo $base | grep -Po "partial-sort\K.*" || true)
    if ! diff --strip-trailing-cr -q --label "computed" <(cat $original | ../indent-sort.py $param) $file; then
        echo "Param: '$param'"
        cat $original | ../indent-sort.py $param> $base.wrong
        diff --strip-trailing-cr --suppress-common-lines -y <(cat $original | ../indent-sort.py $param) $file
    fi
done < <(ls *correct)
