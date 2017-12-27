#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import logging

from PIL import Image, ImageDraw, ImageFont

from epd import epd2in7b as epdlib

import RPi.GPIO as GPIO
from tomodachi import get_hiragana

def get_input(wait=1000):
    """When called, it waits 100s 
    for the first sign of input from the user,
    and returns a number corresponding to that input."""
    import time
    import RPi.GPIO as GPIO
    selected_key = None
    GPIO.setmode(GPIO.BCM)                                                                                               
    keys = [
           5, 6, 13, 19
        ]
    for key in keys:
        GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    counter = 0
    while counter<wait:
        counter+=1
        input_states = dict((key,GPIO.input(gpio_pin)) for key, gpio_pin in enumerate(keys))
        for key in range(4):
            if not input_states[key]:
                selected_key = key+1
                counter = wait
                break
            
        time.sleep(0.1)
    logging.debug("You chose: {}".format(selected_key))
    return selected_key

def test_romaji_hiragana(romaji, options):
    """Prints a question to the screen, asking which of the
    printed hiragana correspond to the given romaji."""
    from epd import epd2in7b as epdlib
    from PIL import Image, ImageDraw, ImageFont
    # TODO: Make a library for this.
    canvas_width, canvas_height = 264, 176
    canvas_black = Image.new(
            "L", 
            (canvas_width, canvas_height), 
            "#ffffff")
    canvas_red = Image.new(
            "L", 
            (canvas_width, canvas_height), 
            "#ffffff")
    font_path = "fonts/rounded-mgenplus-1p-regular.ttf"
    font_en = ImageFont.truetype(font_path, 20)
    font_nh = ImageFont.truetype(font_path, 18)
    draw = ImageDraw.Draw(canvas_black)
    msg_1 = u"What is the hiragana for\n'{}'?".format(romaji)
    logging.debug(msg_1)
    
    draw.text(
            (2, 5),
            msg_1,
            fill = "#000000",
            font=font_en
            )
    
    msg_2 = u"[1] {0}     [2] {1}\n\n[3] {2}    [4] {3}".format(*options)
    logging.debug(msg_2)
    draw.text(
            (40,70),
            msg_2,
            fill = "#000000",
            font=font_nh
            )
    epd = epdlib.EPD()
    epd.init()
    canvas_black = canvas_black.transpose(Image.ROTATE_90)
    canvas_red = canvas_red.transpose(Image.ROTATE_90)
    frame_black = epd.get_frame_buffer(canvas_black)
    frame_red = epd.get_frame_buffer(canvas_red)
    epd.display_frame(frame_black, frame_red)
    answer = get_input()
    return options[answer-1] if answer is not None else None

def print_result(points, success, comment=None):
    """Displays the points, and the success state."""
    from epd import epd2in7b as epdlib
    from PIL import Image, ImageFont, ImageDraw
    if success:
        message = "Correct!"
    else:
        message = u"Wrong!\n {}".format(comment)
    logging.debug(message)
    canvas_black = Image.new("L", (264, 176), "#ffffff")
    canvas_red = Image.new("L", (264, 176), "#ffffff")
    font_path = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf"
    font = ImageFont.truetype(font_path, 20)
    draw = ImageDraw.Draw(canvas_black)
    draw.text(
        (80,25),
        message,
        fill="#000000",
        font=font)
    font_tiny = ImageFont.truetype(font_path, 12)
    draw.text(
            (30, 120),
            "[Press 1-3 to continue. 4 to exit.]",
            fill="#000000",
            font=font_tiny
            )
    font_r = ImageFont.truetype(font_path, 18)
    draw = ImageDraw.Draw(canvas_red)
    msg =  "Score: {}".format(points)
    logging.debug(msg)
    draw.text(
        (50, 80),
        msg,
        fill="#000000",
        font=font_r
        )
    epd = epdlib.EPD()
    epd.init()
    frame_b = epd.get_frame_buffer(canvas_black.transpose(Image.ROTATE_90))
    frame_r = epd.get_frame_buffer(canvas_red.transpose(Image.ROTATE_90))
    epd.display_frame(frame_b, frame_r)


def start_quiz():
    """Starts the epaperhat quiz."""
    import random
    hiragana = get_hiragana()
    points = 0
    while True:
        hiragana_to_test = random.choice(list(hiragana.keys()))

        correct_kana = hiragana[hiragana_to_test]
        other_options = [x for x in hiragana.values() if x != correct_kana]
        other_options = random.sample(other_options, 3)
        other_options.append(correct_kana)
        random.shuffle(other_options)
        answer = test_romaji_hiragana(hiragana_to_test, other_options)
        if answer == correct_kana:
            points+=1
            success=True
            comment = None
        else:
            success=False
            comment = u"{} =  {}".format(hiragana_to_test, correct_kana)

        print_result(points, success, comment)
        reply = get_input(wait=100)
        if reply == 4:
            break
        
if __name__ == "__main__":
    start_quiz()


