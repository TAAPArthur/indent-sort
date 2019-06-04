#!/bin/python3
import sys
import re

comma=True

regex = re.compile(r"^\s*[\[\]\{\},\s;]*")
def getInput():

    for line in sys.stdin:
        yield line
    yield None

sortMinLevel=-1
sortMaxLevel=float("inf")
if len(sys.argv) > 1 :
    parts=sys.argv[1].split("-")
    if parts:
        if len(parts)==1:
            sortMinLevel=sortMaxLevel=int(parts[0])
        else:
            if parts[0]:
                sortMinLevel=int(parts[0])
            if parts[1]:
                sortMaxLevel=int(parts[1])

def indentSort():
    stack = [(-1,-1, [""])]
    for line in getInput():
        currentLevel,currentNestLevel, lines = stack[-1]
        if line != None:
            trimmedLine = line.lstrip()

            indentLevel = len(
                line)-len(trimmedLine) if trimmedLine else currentLevel
        else:
            indentLevel = -1
        while currentLevel > indentLevel:
            currentNestLevel= stack.pop()[1]
            if lines:
                if sortMinLevel <= currentNestLevel <= sortMaxLevel:
                    changeComma=False
                    if comma and not lines[-1].endswith(",\n") and lines[0].endswith(",\n"):
                        lines[-1]=lines[-1][:-1]+",\n"
                        changeComma=1
                    lines.sort()
                    if comma and changeComma:
                        lines[-1]=lines[-1][:-2]+"\n"

                stack[-1][-1][-1] += "".join(lines)
            currentLevel,currentNestLevel, lines = stack[-1]


        if line == None:
            return "".join(stack[0][-1])
        if trimmedLine != regex.sub("",line):
            stack[-1][-1][-1] += line
        else: 
            if currentLevel != indentLevel:
                lines = []
                stack.append((indentLevel,currentNestLevel +1, lines))
            lines.append(line)


lines = indentSort()
print(lines,end="")
