#!/usr/bin/python3
# -*- coding: utf-8 -*-

def get_hiragana():
    """Returns a list of dictionaries of hiragana."""
    import textwrap
    data = """
                    a   i   u   e   o
                ∅   あ  い  う  え  お
                k   か  き  く  け  こ
                s   さ  し  す  せ  そ
                t   た  ち  つ  て  と
                n   な  に  ぬ  ね  の
                h   は  ひ  ふ  へ  ほ
                m   ま  み  む  め  も
                y   や      ゆ      よ
                r   ら  り  る  れ  ろ
                w   わ  ゐ      ゑ  を
            """
    hiragana_table = textwrap.dedent(data)
    hiragana_dict = {}
    for i in hiragana_table.split("\n"):
        items = i.strip().split()
        if len(items) == 5:
            header = items
        elif len(items) == 6:
            key = items[0]
            hiragana = items[1:]
            for h, letter in zip(header, hiragana):
                romaji = "{}{}".format(key, h)
                hiragana_dict[romaji] = letter
    return hiragana_dict

if __name__ == "__main__":
    h = get_hiragana()
    print(h)

