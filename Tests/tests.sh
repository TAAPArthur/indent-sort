set -e
#diff --strip-trailing-cr -q -y <(cat tests1 | ../indent-sort.py) tests1-correct
#diff --strip-trailing-cr -q -y <(cat tests2 | ../indent-sort.py) tests2-correct
diff --strip-trailing-cr -q <(cat test-partial-sort1 | ../indent-sort.py 1) test-partial-sort1-correct
diff --strip-trailing-cr -q <(cat test-partial-sort2 | ../indent-sort.py 2) test-partial-sort2-correct
diff --strip-trailing-cr -q <(cat test-partial-sort3 | ../indent-sort.py 1-2) test-partial-sort3-correct
