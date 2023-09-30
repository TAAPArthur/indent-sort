#!/usr/bin/python3
import argparse
import re
import sys

debug = False
# debug = True

endingBlockRegex = re.compile(r"^\s*([\[\]\{\},;]|</|-->|\*/)+\s*")
startingBlockRegex = re.compile(r'^\s*(\n|#|/\*|//|/\*|<!--|@|template).*')

modifiersRegex = re.compile(r"(public|static|abstract|private|final|const)\s*")
continuationRegex = re.compile(r"((,| \\)\n)$")


class SortSettings:
    start_key = 0
    ignore_modifiers = False
    ignore_case = False
    sort_min_level = -1
    sort_max_level = float("inf")

    def __init__(self, key=0, ignore_modifiers=False, ignore_case=False, sort_range=""):
        self.start_key = key if isinstance(key, int) else int(key.split(",")[0])
        self.ignore_modifiers = ignore_modifiers
        self.ignore_case = ignore_case

        if sort_range:
            parts = sort_range.split("-")
            if parts:
                if len(parts) == 1:
                    self.sort_min_level = self.sort_max_level = int(parts[0])
                else:
                    if parts[0]:
                        self.sort_min_level = int(parts[0])
                    if parts[1]:
                        self.sort_max_level = int(parts[1])


def getSortKey(key, settings):
    if settings.ignore_modifiers:
        key = modifiersRegex.sub("", key)
    key = key.split()[settings.start_key:]
    if settings.ignore_case:
        key = key.lower()
    return key


class Block:

    def __init__(self, codeBlock, indentLevel, nestedLevel, settings, header=""):
        self.codeBlock = codeBlock
        self.settings = settings
        self.sortKey = getSortKey(codeBlock, settings)
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

    def getEnd(self):
        return self.footer if self.footer else self.codeBlock

    def modifyLastEntry(self, replacement):
        if self.footer:
            self.footer = replacement(self.footer)
        else:
            self.codeBlock = replacement(self.codeBlock)

    def finalize(self):
        if self.done:
            return
        self.done = True
        if not self.children or self.isHeader:
            return
        for kid in self.children:
            kid.finalize()
        if self.settings.sort_min_level <= self.nestedLevel + 1 <= self.settings.sort_max_level:
            assert self.children[-1]
            continuationChar = False
            match = continuationRegex.search(self.children[0].getEnd())
            if not continuationRegex.search(self.children[-1].getEnd()) and match:
                self.children[-1].modifyLastEntry(lambda x: x.replace("\n", match.group(1)))
                continuationChar = 1
            self.children.sort()
            if continuationChar:
                self.children[-1].modifyLastEntry(lambda x: continuationRegex.sub("\n", x))
            assert self.children[-1]

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
                assert self.children[-1]
            if not self.children or self.children[-1].process(line, indentLevel):
                if self.children and self.children[-1].indentLevel == indentLevel:
                    if endingBlockRegex.match(line):
                        self.children[-1].footer += line
                        return False
                if self.children:
                    if self.children[-1].isHeader:
                        header = str(self.children.pop())
                        self.children.append(Block(line, indentLevel, self.nestedLevel + 1, settings=self.settings, header=header))
                        return False
                self.children.append(Block(line, indentLevel, self.nestedLevel + 1, settings=self.settings))
                assert self.children[-1]
        return False


def getInput():
    for line in sys.stdin:
        yield line
    yield None


def indentSort(settings):
    root = Block("", -1, -1, settings=settings)
    lastLevel = -1
    for i, line in enumerate(getInput()):
        if i == 0 and line and line.startswith("#!"):
            root = Block(line, -1, -1, settings)
            continue
        if line != None:
            trimmedLine = line.lstrip()
            indentLevel = len(line) - len(trimmedLine) if trimmedLine else lastLevel
            if not trimmedLine:
                indentLevel = lastLevel + 1
            else:
                lastLevel = indentLevel
        else:
            indentLevel = -1
        root.process(line, indentLevel)
    return root


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version="1.1")
    parser.add_argument("-m", "--ignore-modifiers", default=False, action="store_const", const=True)
    parser.add_argument("-k", "--key", default=0, help="Skip the first N words when sorting")
    parser.add_argument("-i", "--ignore-case", default=False, action="store_const", const=True)
    parser.add_argument("sort_range", default=None, nargs="?")
    namespace = parser.parse_args()
    settings = SortSettings(key=namespace.key, ignore_case=namespace.ignore_case, ignore_modifiers=namespace.ignore_modifiers, sort_range=namespace.sort_range)

    root = indentSort(settings)
    print(root, end="")
