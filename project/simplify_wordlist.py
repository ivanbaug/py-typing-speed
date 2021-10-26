import json
import random


def load_words():
    with open("project\\assets\\words_dictionary.json") as word_file:
        valid_words = json.load(word_file)

    return valid_words


def save_new_dict(new_dict):
    with open("project\\assets\\simple_dictionary.json", "w") as word_file:
        json.dump(new_dict, word_file)


if __name__ == "__main__":

    english_words = load_words()
    print(f"Original dict size: {len(english_words)}")
    # english_words = {"Fruit": 22, "Plain": 14, "Cinnamon": 4, "Cheese": 21}

    # Make new dict to save the words with the desired lenght
    simple_words = {}

    for w in english_words:
        if len(w) >= 4 and len(w) <= 7:
            simple_words[w] = 1

    print(f"New dict size: {len(simple_words)}")

    # Save the new dict
    # save_new_dict(simple_words)

    mlist = list(simple_words.keys())

    ran = random.choices(mlist, k=random.randint(15, 20))
    print(ran)
