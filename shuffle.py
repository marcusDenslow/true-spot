from collections import Counter

from debias import clean

bits = iter(clean)


def randwom_below(n):
    k = (n - 1).bit_length()
    while True:
        number = 0
        for _ in range(k):
            number = number * 2 + next(bits)
        if number < n:
            return number


def shuffle(items):
    items = list(items)
    for i in range(len(items) - 1, 0, -1):
        j = randwom_below(i + 1)
        items[i], items[j] = items[j], items[i]
    return items


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
