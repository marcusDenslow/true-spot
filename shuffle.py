from collections import Counter
from pathlib import Path

from debias import clean

OFFSET_FILE = Path("bit_offset.txt")
posittion = int(OFFSET_FILE.read_text() if OFFSET_FILE.exists() else 0)


def next_bit():
    global posittion
    posittion += 1
    return clean[posittion - 1]


def save_position():
    OFFSET_FILE.write_text(str(posittion))
    print(f"bits used: {posittion} of {len(clean)}")


def randwom_below(n):
    k = (n - 1).bit_length()
    while True:
        number = 0
        for _ in range(k):
            number = number * 2 + next_bit()
        if number < n:
            return number


def shuffle(items):
    items = list(items)
    for i in range(len(items) - 1, 0, -1):
        j = randwom_below(i + 1)
        items[i], items[j] = items[j], items[i]
    return items


if __name__ == "__main__":
    songs = [
        "sad song",
        "gym song",
        "the on i always skip",
        "banger",
        "song from 2010",
        "3am song",
    ]
    print(shuffle(songs))

    counts = Counter("".join(shuffle("ABC")) for _ in range(6000))
    for order, count in sorted(counts.items()):
        print(order, count)
