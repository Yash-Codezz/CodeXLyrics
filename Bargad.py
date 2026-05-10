import time
import emoji
def type_lyric(line, char_delay = 0.065):
    for char in line:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()
def print_lyrics():
    lyrics = [
        "Ki raani teri ek",
        "jhalak se main pagall...........",
        "(main pagall........)",
        "\nSametu teri khushboo ko",
        "choom ke chaadar",
        "(choom ke chaadarrr..........)",
        "\nHawa ko roke dhool",
        "sajata teri",
        "Pehne na tu payal bin",
        "bataaye aati yaadon",
        "mein bhi",
        "Som ka jharoka maano",
        "aankhon mein teri",
        "Inn mein doob sa gaya",
        "hoon karke pooja jo teri",
        "\nYe palkein hain bheeg",
        "jaati",
        "Kyun hai tu",
        "itni pyaari",
        "Meri bhaasha",
        "hi badal di",
        "Pyaari", 
        "seedhi........ saadhi..........",
        "\nKi raani jo tu aaye iss",
        "dil mein ho halchalll..........",
        "(main pagal......)",
        "Bargard tale intezaar tera........",
        "Main karu",
        "kab tak\n",
    ]
    delay = [0.5, 0.3, 0.75, 0.1, 0.5, 0.9, 0.25, 0.1, 0.1, 0.0, 0.0, 0.1, 0.2, 0.1, 0.35, 0.4, 0.7, 0.5, 0.85, 0.7, 1.35, 0.4, 0.9, 0.1, 0.2, 0.45, 1.7, 0.1, 0]
    print(emoji.emojize("\nPlaying Song:musical_note: -> \"Bargad:deciduous_tree:\" by \"Arpit Bala:\""))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    time.sleep(1.0)
    for i, line in enumerate(lyrics):
        type_lyric(line)
        time.sleep(delay[i])
print_lyrics()
time.sleep(0.02)
