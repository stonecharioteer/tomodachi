#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont

from epd import epd2in7b as epdlib

import RPi.GPIO as GPIO
from tomodachi import get_hiragana

def get_user_input():
    
    import pdb

def start_quiz():
    """Starts the epaperhat quiz."""
    import random
    hiragana = get_hiragana()
    points = 0
    while True:
        hiragana_to_test = random.choice(hiragana.keys())
        correct_kana = hiragana[hiragana_to_test]
        other_options = [x for x in hiragana.values() if x != correct_kana]
        other_options = random.sample(other_options, 3)
        other_options.append(correct_kana)
        random.shuffle(other_options)
        answer = ask_question(hiragana_to_test, options)
        if answer == correct_kana:
            points+=1
            success=True
        else:
            success=False
        print_result(points, success)
        
if __name__ == "__main__":
    start_quiz()

def get_input():
    GPIO.setmode(GPIO.BCM)                                                                                                
    keys = [
           5, 6, 13, 19
        ]
    for key in keys:
        GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        input_states = dict((key,GPIO.input(gpio_pin)) for key,gpio_pin in enumerate(keys))

