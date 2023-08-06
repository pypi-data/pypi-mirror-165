# wordconstraints

A small python module for filtering a list of words by letter inclusion and exclusion (over a whole word or at paticular positions), and by word type (e.g verb, plural noun).

# About

Originally made for use in word based puzzle solvers for things like crosswords or wordle.

Processing of word types heavily uses [LemmInflect](https://github.com/bjascob/LemmInflect).


# Example Uses

## Wordle Filtering
This example demonstrates filtering by letter inclusion and exclusion, both over a whole word and at paticular positions. Here we have a wordle game (spoilers for 30/08/2022):

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1FvXHPWbosbxWX0r3iEDrpRWY_ngr5ABR" height = "200">
</p>

At this point we know quite a lot of information about the target word:
- H,A,R,P,I,L,F,U and D are excluded from the word.
- An E is included at the 4th position.
- S,E,O and N are included somewhere in the word but those letters are not present at that position.

Using find_words we can find words that meet all these constraints:

![alt text](https://drive.google.com/uc?export=view&id=1v14b6GyHmK-4TvIS6YhKsNcdyGugvXtE)

And we find that there is only one word (in the default word list) that meets these constraints:

```
['onset']
```


And sure enough that's the answer!

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1gVBIcrvnkCbdqeZdcEr26JPw3PaFX0xV" height = "200">
</p>

## Crossword Clues
These examples demonstrates the use of the universal parts of speech tags and penn tags.

### General Word Type (Noun, Verb e.t.c)
Universal parts of speech tags (or upos tags) like "NOUN", "ADJ", or "VERB" can be used to get words only of that type.

Using the upos_tag "NOUN" we can further narrow down the potential words that might be the answer to the crossword clue "Melee".

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1UR9dSDNzwiMl1D29jtIfxt33tTEi3Oau" height = "200">
</p>


Using the default word list and the information we have, plus the "NOUN" upos tag we get the following possible words ("brawl" seems like a pretty likely candidate here)
```
['Snows', 'blows', 'brawl', 'brawn', 'brews', 'brown', 'brows', 'chews', 'claws', 'clews', 'clown', 'crawl', 'craws', 'crews', 'crowd', 'crown', 'crows', 'draws', 'flaws', 'flows', 'frown', 'growl', 'known', 'plows', 'prawn', 'prowl', 'prows', 'scowl', 'shawl', 'shows', 'snows', 'spawn', 'stews', 'thaws', 'trawl', 'views']
```

### More Specific Word Type (Singular vs Plural, Tense e.t.c)
Penn tags are like more specific versions of upos tags. Rather than just filtering for verbs or nouns, we can filter more specifically for things like verbs of a certain tense. This can be quite useful for situations like crossword puzzles where single word clues are conventionally given in the same tense/plurality as the answer.

Here the clue "covers" is a non 3rd person singular present verb. So we can expect the answer will be the same. 
<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1KC57Ksd2QZU3N5mm7jWtn-8NWCa12oTS" height = "200">
</p>

Using the corresponding penn_tag "VBP" we can narrow down the number of potential answers in the default word list from 56 to 10 ('coats' seems like the right answer here). 

```
['chaps', 'chars', 'chats', 'clads', 'clams', 'claps', 'claws', 'coats', 'crabs', 'crams']
```



# Full Details

The only front facing function is find_words. To use:

```
import wordconstraints as wc
```
```
wc.find_words()
```

The find_words function takes a few different parameters, all optional.

<p align = "center">
<img src="https://drive.google.com/uc?export=view&id=1fqSRiyC8JQQdnkv_gT-eXTULsMS1-BEl" width="420">
</p>

- word_list
    - The list of words to filter with constraints. 
    - Underscores, hyphens and apostrophes in provided strings will be removed. 
    - If no word list is given filtering will be done over the nltk list of around 23,000 words. (See section 4.1 [here](https://www.nltk.org/book/ch02.html) for nltk word list docs and source)
- num_letters
    - If an integer is provided, words must have this length.
    - If a list of integers is provided, then words must match one of the provided lengths.
- includes
    - If provided, words must include ALL of the listed letters somewhere in the word.  
    - Letters should be lowercase.
    - Letters are only counted 'once', i.e you currently can't filter specifically for words that have multiple copies of a letter.
- excludes
    - If provided, words must not include ANY of the listed letters anywhere in the word.  
    - Letters should be lowercase.
- includes_at_idxs
    - If provided, words must include one of the listed letters at each keyed index.
    - Values should be a list containing lowercase letters.
    - Keys should be integer indexes.
- excludes_at_idxs
    - If provided, words must exclude all of the listed letters at each keyed index.
    - Values should be a list containing lowercase letters.
    - Keys should be integer indexes.
- upos_tag
    - If provided, words must have this universal part of speech tag.
    - Valid tags are "NOUN", "VERB", "ADJ", "ADV", "PROPN" (proper noun), and "AUX" (auxilliary verb). 
    - [Universal parts of speech info](https://universaldependencies.org/u/pos/)
    - Uses [LemmInflect](https://github.com/bjascob/LemmInflect). 
- penn_tag
    - If provided, words must have this Penn Treebank tag. 
    - Some helpful tags are "NN" and "NNS" for singular and plural nouns, and the verb tags "VBD", "VBG", "VBN", "VBP", and "VBZ" for various tenses.
    - More info on Penn Treebank tags [here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
    - Uses [LemmInflect](https://github.com/bjascob/LemmInflect).
- shorter_than
    - If provided, words must have a length which is less than provided integer.
- longer_than
    - If provided, words must have a length which is more than provided integer.

# Issues

- Filtering of strings with upper case letters might be buggy, so its possible that filtering of proper nouns might not work correctly at the moment.


# Possible Features to Add

- Add the ability to match the type of a provided word (useful for crosswords, where for example, a plural noun clue means the answer is also a plural noun)
- Make a more user friendly way to interact with universal parts of speech tags and penn tags. For example, a more user friendly way to get all penn tags for past tense verbs (without having to know what a past participle is)
- Add ability to require that letter have multiple copies of a single letter. e.g the word must contain two of the letter 'e'.

