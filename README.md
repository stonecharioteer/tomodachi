# tomodachi

This is an application I'm making to help me learn
nihongo.

It'll be a "Who Wants to be a Millionaire?" style quiz 
with four options.

First, it'll be for learning the hiragana, the katakana
and the kanji.

## Hardware

This script is designed to be run on a Raspberry Pi 3, using the waveshare 
e-paper-hat (2.7" model b with dual color support). However, there is no reason why
it should not run on other models of the Raspberry Pi.

## Python Version

Right now, the module that this depends on, the epd libraries supplied by
waveshare, are coded only with Python 2 in mind. I'm going to change that later
so this uses Python 3 for its excellent unicode support.

## Photos

**Questionnaire:**

![Photo 1](images/photo_01.jpeg)

**Success Screen:**

![Photo 2](images/photo_02.jpeg)

**Wrong Answer Screen:**

![Photo 3](images/photo_03.jpeg)


## TODO:

    [x] Implement basic quiz.
    [x] Implement romaji-hiragana quiz.
    [*] Implement romaji-katakana quiz.
    [*] Implement hiragana-romaji quiz.
    [*] Implement katakana-romaji quiz.
    [*] Implement romaji-kana quiz.
    [*] Implement kana-romaji quiz.
    [*] Implement score log and show top high score list.
    [*] Move the characters to an sqllite database instead of dedicated functions.
    [*] Implement argparse to enable/disable debug.
    [*] Remove the epd module from this repository, fork the original and fix the python3 implementation.
    [*] Implement quiz mode selector at the start screen.
    



-----------------------
