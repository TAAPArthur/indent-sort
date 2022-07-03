# Indent sort
Sorts input with respect to indentation level

## Install
`make install`

## Examples

```
indent-sort          < file    # sort the entire file
indent-sort 0        < file    # sort only non indented lines
indent-sort 1        < file    # sort only the first level of indented lines
indent-sort -m -k 1  < file    # Sort all methods by name (instead of by modifier)
```
