#!/usr/bin/python3
import sys
import re
import argparse

comma = True
debug = False
# debug = True

endingBlockRegex = re.compile(r"^\s*([\[\]\{\},;]|</|-->|\*/)+\s*")
startingBlockRegex = re.compile(r'^\s*(\n|#|/\*|//|/\*|<!--|@|template).*')

modifiersRegex = re.compile(r"(public|static|abstract|private|final|const)\s*")


def getInput():
    for line in sys.stdin:
        yield line
    yield None


helpStr = """
Usage: indent-sort [[min]-[max]]

Examples
cat file | indent-sort 0        # sort non-indented lines
cat file.xml | indent-sort        # sort entire file
"""

sortMinLevel = -1
sortMaxLevel = float("inf")
IGNORE_MODIFIERS = False
KEY_SPLIT = None

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version="1.1")
parser.add_argument("-m", "--ignore-modifiers", default=False, action="store_const", const=True)
parser.add_argument("-k", "--key", default=None, type=int, help="Skip the first N words when sorting")
parser.add_argument("range", default=None, nargs="?")
namespace = parser.parse_args()
KEY_SPLIT = namespace.key
IGNORE_MODIFIERS = namespace.ignore_modifiers
if namespace.range:
    parts = namespace.range.split("-")
    if parts:
        if len(parts) == 1:
            sortMinLevel = sortMaxLevel = int(parts[0])
        else:
            if parts[0]:
                sortMinLevel = int(parts[0])
            if parts[1]:
                sortMaxLevel = int(parts[1])


def getSortKey(key):
    if IGNORE_MODIFIERS:
        key = modifiersRegex.sub("", key)
    if KEY_SPLIT:
        key = key.split()[KEY_SPLIT:]
    return key


class Block:

    def __init__(self, codeBlock, indentLevel, nestedLevel, header=""):
        self.codeBlock = codeBlock
        self.sortKey = getSortKey(codeBlock)
        self.indentLevel = indentLevel
        self.nestedLevel = nestedLevel
        self.children = []
        self.done = False
        self.header = header
        self.isHeader = startingBlockRegex.match(codeBlock)
        self.footer = ""

    def __lt__(self, other):
        return self.sortKey < other.sortKey

    def __iadd__(self, value):
        self.codeBlock += value
        return self

    def endswith(self, s):
        return self.footer.endswith(s) if self.footer else self.codeBlock.endswith(s)

    def setTrailingComma(self, add):
        if add:
            if self.footer:
                self.footer = self.footer[:-1] + ",\n"
            else:
                self.codeBlock = self.codeBlock[:-1] + ",\n"
        else:
            if self.footer:
                self.footer = self.footer[:-2] + "\n"
            else:
                self.codeBlock = self.codeBlock[:-2] + "\n"

    def finalize(self):
        if self.done:
            return
        self.done = True
        if not self.children or self.isHeader:
            return
        for kid in self.children:
            kid.finalize()
        if sortMinLevel <= self.nestedLevel + 1 <= sortMaxLevel:
            assert(self.children[-1])
            changeComma = False
            if comma and not self.children[-1].endswith(",\n") and self.children[0].endswith(",\n"):
                self.children[-1].setTrailingComma(1)
                changeComma = 1
            self.children.sort()
            if comma and changeComma:
                self.children[-1].setTrailingComma(0)
            assert(self.children[-1])

    def __str__(self):
        s = ""
        if debug:
            s += str(self.nestedLevel)
        s += self.header + self.codeBlock
        for kid in self.children:
            s += str(kid)
        s += self.footer
        return s

    def __iter__(self):
        yield self
        for kid in self.children:
            for k in kid:
                yield k

    def process(self, line, indentLevel):
        if self.done:
            return True
        if self.indentLevel >= indentLevel:
            self.finalize()
            return True
        else:
            if self.children:
                assert(self.children[-1])
            if not self.children or self.children[-1].process(line, indentLevel):
                if self.children and self.children[-1].indentLevel == indentLevel:
                    if endingBlockRegex.match(line):
                        self.children[-1].footer += line
                        return False
                if self.children:
                    if self.children[-1].isHeader:
                        header = str(self.children.pop())
                        self.children.append(
                            Block(line, indentLevel, self.nestedLevel + 1, header=header))
                        return False
                self.children.append(
                    Block(line, indentLevel, self.nestedLevel + 1))
                assert(self.children[-1])
        return False


def indentSort():
    root = Block("", -1, -1)
    lastLevel = -1
    for i, line in enumerate(getInput()):
        if i == 0 and line.startswith("#!"):
            root = Block(line, -1, -1)
            continue
        if line != None:
            trimmedLine = line.lstrip()
            indentLevel = len(line) - len(
                trimmedLine) if trimmedLine else lastLevel
            if not trimmedLine:
                indentLevel = lastLevel + 1
            else:
                lastLevel = indentLevel
        else:
            indentLevel = -1
        root.process(line, indentLevel)
    return root


root = indentSort()
print(root, end="")
