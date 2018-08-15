#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import git
import os
import pip
import ConfigParser


print(str(sys.argv).upper())

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

    packages = ['', '', '']
    for package in packages:
        pip.main(['install', '--upgrade', package])

    try:
        _ = git.Repo("/home/pythonapp/ws2812server/test").git_dir
        repo = git.Repo.init("/home/pythonapp/ws2812server/test")
        result = repo.git.pull()
        print(result)
    except git.exc.InvalidGitRepositoryError:
        print("Downloading Files")
        repo = git.Repo.clone_from("https://github.com/Acer90/PI-WS2812-Server.git", "/home/pythonapp/ws2812server/test")

elif "UPDATE" == mode:
    cwd = os.getcwd()

    repo = git.Repo.init("/home/pythonapp/ws2812server/test")
    for item in repo.index.diff(None):
        print item.a_path

    result = repo.git.pull()
    print(result)

elif "DEL" == mode:
    cwd = os.getcwd()



