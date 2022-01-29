import streamlit as st
import pandas as pd
import numpy as np

import string
from collections import Counter

def load_words():
    with open('wordlist_solutions.txt') as file:
        words = file.readlines()
    
    return words

st.title("Wordle Helper")

words = load_words()

known_letters = st.text_input('Known letters (? = Wildcard)', max_chars=5)
regex = known_letters.lower().replace('?', '\w')

includes_letters = st.multiselect('Includes', list(string.ascii_lowercase))
excludes_letters = st.multiselect('Excludes', list(string.ascii_lowercase))

df = pd.DataFrame({'words':words})

filters = np.full(df.shape[0], True)

# Known letters
filters = (
    filters
    & (df.words.str.contains(regex))
)

# Includes letters
if len(includes_letters) > 0:
    for letter in includes_letters:
        filters = (
            filters
            & (df.words.str.contains(letter))
        )

# Excludes letters
if len(excludes_letters) > 0:
    for letter in excludes_letters:
        filters = (
            filters
            & (~df.words.str.contains(letter))
        )

filtered_df = df[filters]

words_concat = ''.join(filtered_df.words.values).replace('\n', '')
letter_dist = Counter(words_concat)

def get_score(word, letter_dist):
    return sum([letter_dist[w] for w in word])

display_df = (
    filtered_df
    .assign(
        score = lambda x: x.words.apply(lambda y: get_score(y, letter_dist))
    )
    .sort_values(by='score', ascending=False)
)

st.dataframe(display_df)