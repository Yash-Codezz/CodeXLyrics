import time
import emoji
def type_lyric(line, char_delay = 0.065):
    for char in line:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    print()
def print_lyrics():
    lyrics = [
        "aapka",
        "hi kehna banta.....",
        "keh do na",
        "\nmai sharma ke",
        "keh doongi",
        "maine bhi dil diya",
        "\naankhon...",
        "aankhon ka masla...",
        "acha tha",
        "\nab le jao",
        "apna bna ke",
        "mujhe meri jaan...."
    ]
    delay = [0.4, 1.7,  0.85, 0.25, 0.55,  1.8, 0.3, 1.45,  0.8, 0.35, 0.75, 0]
    print(emoji.emojize("\nPlaying Song:musical_note: -> \"majboor:pink_heart:\" by \"Zoha Waseem:\""))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    time.sleep(0.2)
    for i, line in enumerate(lyrics):
        type_lyric(line)
        time.sleep(delay[i])
print_lyrics()
time.sleep(0.02)
