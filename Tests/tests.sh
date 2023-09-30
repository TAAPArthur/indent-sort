#!/bin/sh -e

../indent-sort.py -h >/dev/null
../indent-sort.py --help >/dev/null
../indent-sort.py -v >/dev/null
../indent-sort.py --version >/dev/null
for file in *correct; do
    base=$(basename "$file" .correct)
    original="$base.orig"
    cmd="$(head -n1 "$original")"
    if [ "${cmd#\#\! }" != "$cmd" ]; then
        param="${cmd#\#\!}"
    else
        param="${base#test-partial-sort}"
        [ "$param" = "$base" ] && param=0-
    fi
    if ! ../indent-sort.py $param  < "$original" | diff -u - "$file"; then
        echo "Test $base failed; param: '$param'"
    fi
done
