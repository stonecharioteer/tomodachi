#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont

from epd import epd2in7b as epdlib

import RPi.GPIO as GPIO
from tomodachi import get_hiragana

def get_input(wait=100):
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
    counter = 1
    while counter<=wait:
        counter+=1
        input_states = dict((key,GPIO.input(gpio_pin)) for key,gpio_pin in enumerate(keys))
        for key in range(4):
            if input_states[key]:
                selected_key = key+1
                break
        time.sleep(1)
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
    font_path = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
    font_en = ImagFont.truetype(font_path, 24)
    font_nh = Image.truetype(font_path, 18)
    draw = ImageDraw.Draw(canvas_black)
    draw.text(
            (2, 5),
            "What's the hiragana for {}?".format(romaji),
            fill = "#000000",
            font=font_en
            )
    draw.text(
            (2,30),
            "[1] {0}\t [2] {1}\n[3] {2}\t[4] {3}".format(*options),
            fill = "#000000"
            font=font_nh
            )
    epd = epdlib.EPD()
    epd.init()
    frame_black = epd.get_frame_buffer(canvas_black.transpose(Image.ROTATE_90)
    frame_red = epd.get_frame_buffer(canvas_red.transpose(Image.ROTATE_90)
    epd.display_frame(frame_black, frame_red)
    answer = get_input()
    return answer

def print_success(points, success):
    """Displays the points, and the success state."""
    from epd import epd2in7b as epdlib
    from PIL import Image, ImageFont, ImageDraw
    if success:
        message = "Correct!"
    else:
        message = "Wrong!"

    canvas_black = Image.new("L", (264, 176), "#ffffff")
    canvas_red = Image.new("L", (264, 176), "#ffffff")
    font_path = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
    font = ImageFont.truetype(font_path, 20)
    draw = ImageDraw.Draw(canvas_black)
    draw.text(
        (80,25),
        message,
        fill="#000000",
        font=font)
    font_tiny = ImageFont.truetype(font_path, 12)
    draw.text(
            (250, 120),
            "[Press 1-3 to continue. 4 to exit.]",
            fill="#000000",
            font=font_tiny
            )
    font_r = ImageFont.truetype(font_path, 30)
    draw = ImageDraw.Draw(canvas_red)
    draw.text(
        (100, 80),
        "Score: {}",
        fill="#000000",
        font=font_r
        )
    epd = epdlib.EPD()
    epd.init()
    frame_b = epd.get_frame_buffer(image_black.transpose(Image.ROTATE_90))
    frame_r = epd.get_frame_buffer(image_red.transpose(Image.ROTATE_90))
    epd.display(frame_b, frame_r)


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
        reply = get_input(wait=10)
        if reply == 4:
            break
        
if __name__ == "__main__":
    start_quiz()


