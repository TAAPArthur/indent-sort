#!/bin/bash
set -e
diff --strip-trailing-cr -q <(cat test-partial-sort1.orig | ../indent-sort.py 1) test-partial-sort1.correct
diff --strip-trailing-cr -q <(cat test-partial-sort2.orig | ../indent-sort.py 2) test-partial-sort2.correct
diff --strip-trailing-cr -q <(cat test-partial-sort3.orig | ../indent-sort.py 1-2) test-partial-sort3.correct

while read file; do
    original=$(basename $file .correct).orig
    if ! diff --strip-trailing-cr -q --label "computed" <(cat $original | ../indent-sort.py) $file; then
        diff --strip-trailing-cr -y <(cat $original | ../indent-sort.py) $file
    fi
done < <(ls *correct |grep -v partial)
