#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import git
import os
import pip
import ConfigParser


print(str(sys.argv).upper())

packages = ['gitpython']
mode = ""

if "INSTALL" in str(sys.argv).upper():
    print "Running Setup"
    mode = "INSTALL"
elif "UPDATE" in str(sys.argv).upper():
    print "Running Update"
    mode = "UPDATE"
elif "REMOVE" in str(sys.argv).upper():
    print "Removing Server"
    mode = "DEL"

if "DIR" in str(sys.argv).upper():
    i = sys.argv.index("bar")

if mode == "":
    while 1:
        input_val = raw_input("Select Mode[INSTALL or 1 | UPDATE or 2 | REMOVE or 3]: ").upper()

        if "INSTALL" == input_val or "1" == input_val:
            print "Running Setup"
            mode = "INSTALL"
            break
        elif "UPDATE" == input_val or "2" == input_val:
            print "Running Update"
            mode = "UPDATE"
            break
        elif "REMOVE" == input_val or "3" == input_val:
            print "Removing Server"
            mode = "DEL"
            break

if "INSTALL" == mode:
    cwd = os.getcwd()
    print("Install/Upgrade Python Packages")

    for package in packages:
        pip.main(['install', '--upgrade', package])

    try:
        _ = git.Repo(cwd).git_dir
        repo = git.Repo.init(cwd)
        result = repo.git.pull()
        print(result)
    except:
        print("Downloading Files")
        repo = git.Repo.clone_from("https://github.com/Acer90/PI-WS2812-Server.git", cwd)

elif "UPDATE" == mode:
    cwd = os.getcwd()

    for package in packages:
        pip.main(['install', '--upgrade', package])

    repo = git.Repo.init(cwd)
    for item in repo.index.diff(None):
        print item.a_path

    result = repo.git.pull()
    print(result)

elif "DEL" == mode:
    cwd = os.getcwd()



