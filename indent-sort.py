#!/bin/python3
import sys
import re

comma=True

regex = re.compile(r"^\s*[\[\]\{\},\s;]*")
def getInput():

    for line in sys.stdin:
        yield line
    yield None


def indentSort():
    stack = [(-1, [""])]
    for line in getInput():
        currentLevel, lines = stack[-1]
        if line != None:
            trimmedLine = line.lstrip()

            indentLevel = len(
                line)-len(trimmedLine) if trimmedLine else currentLevel
        else:
            indentLevel = -1
        while currentLevel > indentLevel:
            stack.pop()
            if lines:
                changeComma=False
                if comma and not lines[-1].endswith(",\n") and lines[0].endswith(",\n"):
                    lines[-1]=lines[-1][:-1]+",\n"
                    changeComma=1
                lines.sort()
                if comma and changeComma:
                    lines[-1]=lines[-1][:-2]+"\n"

                stack[-1][1][-1] += "".join(lines)
            currentLevel, lines = stack[-1]


        if line == None:
            return "".join(stack[0][1])
        if trimmedLine != regex.sub("",line):
            stack[-1][1][-1] += line
        else: 
            if currentLevel != indentLevel:
                lines = []
                stack.append((indentLevel, lines))
            lines.append(line)


lines = indentSort()
print(lines,end="")
