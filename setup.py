#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import git
import os
import pip
import ConfigParser

Config = ConfigParser.ConfigParser()
packages = ['gitpython']
repo_path = "https://github.com/Acer90/PI-WS2812-Server.git"
mode = ""

def GetValue(text, type = "string", default = ""):
    while 1:
        if(type == "bool"):
            text = text + "[" + str(default) + "](True/False): "
        elif(default != ""):
            text = text + "[" + str(default) + "]: "
        else:
            text = text + ": "

        input_val = raw_input(text)

        if(input_val == ""):
            return default

        if(type == "string"):
            return input_val
        if (type == "bool"):
            try:
                convert_val = bool(input_val)
                return convert_val
            except:
                print("Value is not a Bool variable!")
        if (type == "int"):
            try:
                convert_val = int(input_val)
                return convert_val
            except:
                print("Value is not a integer variable!")
        if (type == "float"):
            try:
                convert_val = float(input_val)
                return convert_val
            except:
                print("Value is not a Float variable!")




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

    for package in packages:
        pip.main(['install', '--upgrade', package])

    try:
        _ = git.Repo(cwd).git_dir
        repo = git.Repo.init(cwd)
        result = repo.git.pull()
        print(result)
    except:
        print("Downloading Files")
        repo = git.Repo.clone_from(repo_path, cwd)

    file_exist = False
    if(os.path.isfile(cwd+"/setup.ini")):
        file_exist = True
        Config.read(cwd+"/setup.ini")
    else:
        setupfile = open(cwd + "/Setup.ini", 'w')

    if (not Config.has_section("Server")): Config.add_section("Server")
    if (not Config.has_section("Strip")): Config.add_section("Strip")
    if (not Config.has_section("Relais")): Config.add_section("Relais")

    ini_server_port = 1234

    ini_Strip_led_count = 60
    ini_Strip_led_pin = 18
    ini_Strip_led_freq_hz = 800000
    ini_Strip_led_dma = 5
    ini_Strip_led_brightness = 255
    ini_Strip_led_invert = False

    ini_Relais_gpio = 0

    if (Config.has_option("Server", "Port")): ini_server_port = Config.getint("Server", "Port")

    if (Config.has_option("Strip", "LED_COUNT")): ini_Strip_led_count = Config.getint("Strip", "LED_COUNT")
    if (Config.has_option("Strip", "LED_PIN")): ini_Strip_led_pin = Config.getint("Strip", "LED_PIN")
    if (Config.has_option("Strip", "LED_FREQ_HZ")): ini_Strip_led_freq_hz = Config.getint("Strip", "LED_FREQ_HZ")
    if (Config.has_option("Strip", "LED_DMA")): ini_Strip_led_dma = Config.getint("Strip", "LED_DMA")
    if (Config.has_option("Strip", "LED_BRIGHTNESS")): ini_Strip_led_brightness = Config.getint("Strip", "LED_BRIGHTNESS")
    if (Config.has_option("Strip", "LED_INVERT")): ini_Strip_led_invert = Config.getboolean("Strip", "LED_INVERT")

    if (Config.has_option("Relais", "GPIO")): ini_Relais_gpio = Config.getint("Relais", "GPIO")


    ini_server_port = GetValue("Serverport", "int", ini_server_port)

    ini_Strip_led_count = GetValue("Strip LED-Count", "int", ini_Strip_led_count)
    ini_Strip_led_pin = GetValue("Pin LED Stripe", "int", ini_Strip_led_pin)
    ini_Strip_led_freq_hz = (GetValue("LED-Stripe Frequency (400/800)", "int", (ini_Strip_led_freq_hz/1000))*1000)
    ini_Strip_led_dma = GetValue("DMA", "int", ini_Strip_led_dma)
    ini_Strip_led_brightness = GetValue("Max Brightness", "int", ini_Strip_led_brightness)
    ini_Strip_led_invert = GetValue("Invert LED-Strip", "bool", ini_Strip_led_invert)

    ini_Relais_gpio = GetValue("GPIO Pin for Relai (0 = off)", "int", ini_Relais_gpio)

    Config.set('Server', 'Port', ini_server_port)

    Config.set('Strip', 'LED_COUNT', ini_Strip_led_count)
    Config.set('Strip', 'LED_PIN', ini_Strip_led_pin)
    Config.set('Strip', 'LED_FREQ_HZ', ini_Strip_led_freq_hz)
    Config.set('Strip', 'LED_DMA', ini_Strip_led_dma)
    Config.set('Strip', 'LED_BRIGHTNESS', ini_Strip_led_brightness)
    Config.set('Strip', 'LED_INVERT', ini_Strip_led_invert)

    Config.set('Relais', 'GPIO', ini_Relais_gpio)

    with open(cwd+"/Setup.ini", 'wb') as configfile:
        Config.write(configfile)


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



