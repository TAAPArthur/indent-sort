
# Indent sort
Sorts input with respect to indentation level

## Install
`make install`

## Examples

```
cat file | indent-sort           # sort the entire file
cat file | indent-sort 0         # sort only non indented lines
cat file | indent-sort 1         # sort only the first level of indented lines
cat file | indent-sort -m -k 1   # Sort all methods by name (instead of by modifier)
```

