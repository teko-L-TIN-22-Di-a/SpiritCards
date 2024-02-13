@echo off

echo starting build...

py -m nuitka --lto=yes --follow-imports --standalone run.py

echo finished building! copying assets folder ...

cp -r assets run.dist

echo successfully copied assets!

@echo on