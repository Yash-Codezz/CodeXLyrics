import time
import emoji
def type_lyric(line, char_delay = 0.065):
    for char in line:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()
def print_lyrics():
    lyrics = [
        "\nMujhe Rakhti",
        "ho Chupake",
        "Batar lo",
        "Kahin pe Jod do",

        "\nLifafe",
        "mein Sajake",
        "humein aisi",
        "kyun Saza do",

        "\nki hum Padhke",
        "Jaane Galti",
        "aur Galti",
        "kal se na ho",

        "\nhumein aisi",
        "ek Saza do",
        "ki hum Jaane",
        "Saari... Doori...",

        "\nhumse jo...",
        "Rooth gayi ho",
        "rehti Chup",
        "hoke... pure din",

        "\nTum Likh lo",
        "Jaise Katgarhe",
        "mein hum Khat",
        "Padh Lenge",
        "Shauk se",

        "\nisi ek pal",
        "ke Bahane fir",
        "hum Galti se",
        "Paas aayenge",

        "\nphir kehne",
        "ki thi galti",
        "aur uska..",
        "kya hi kehna....\n"
    ]
    delay = [0.6, 1.4, 0.75,  1.5, 1.0, 1.05, 0.7,  1.35, 1.0, 1.35, 0.85,
             1.3, 1.0, 1.2, 1.0,  1.1, 0.7, 1.1, 1.0,  1.0, 0.9, 0.9, 0.5, 0.25,  1.0, 0.8, 1.3, 0.75,  1.35, 0.75, 1.4, 1.25, 0]
    print(emoji.emojize("\nPlaying Song:musical_note: -> \"Rakhlo Tum Chupaake:red_heart:\" by \"Arpit Bala:\""))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    time.sleep(1.0)
    for i, line in enumerate(lyrics):
        type_lyric(line)
        time.sleep(delay[i])
print_lyrics()
time.sleep(0.02)