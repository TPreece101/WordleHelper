import streamlit as st
import pandas as pd
import numpy as np

import string

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

st.dataframe(df[filters])