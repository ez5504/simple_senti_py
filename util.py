# Copyright 2016 Jacob Taylor - Idkoru Technologies

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from itertools import *
import re

## Helper class for SimpleSentiPy.
# A class containing functions to perform various text pre-processing and
# sentiment analysis helper functions.
class Utility():

    ## Trims words based on provided characters
    # Example: trim("hello#1", "#") --> "hello"
    # @param self The object pointer.
    # @param word The word to be trimmed.
    # @param char The character at which the word will stop.
    # \return   A trimmed word based on the character provided
    def trim(self, word, char):
        i = word.find(char)
        if i != -1:
            return word[0:i]

    ## Performs a very basic word/punctuation split.
    # Runs text through the pre-tokenizer function and then splits up punctuation
    # and finally removes certain unneeded words.
    # \return   List of tokens in sentence
    def tokenize(self, text):
        text = text.lower()
        text = text.split()
        self.pre_tokenize(text)
        text = ' '.join(text)
        text = re.findall(r"[\w']+|[.,!?;]", text) # splits punctuation into separate tokens
        text = ' '.join(text)
        tmp = ' '.join([w for w in text.split() if (len(w) >= 3 or w == "!" or\
                        w == "," or w == "." or w == ";" or  w == "?" or w == "URL")])
        tmp = tmp.split()
        return tmp # returns list of tokens

    ## Replaces emoticons with default words stored in the data file.
    # @param self The object pointer.
    # @param word The word being checked/altered.
    # \return   Either the original word or one of the three replacements (SMILE, FROWN, LAUGH)
    def check_emotes(self, word):
        smiles = ":) :] :-P :P :-) :-] :o :-o 8) 8-) 8] 8-] :D 8D :-D 8-D =) =D =] xD xP"
        frowns = ":( :[ :-( :-[ 8( 8-( 8-[ 8-[ =[ =("
        if word in smiles:
            return "SMILE"
        elif word in frowns:
            return "FROWN"
        elif "lol" in word:
            return "LAUGH"
        elif "haha" in word:
            return "LAUGH"
        else:
            return word

    ## Pre-processor for text.
    # Runs each word through the check_emotes function and replaces URLS
    # with URL and usernames with USER
    # @param self The object pointer.
    # @param text The unprocessed line being altered.
    # \Returns Nothing. Operates in-place on list.
    def pre_tokenize(self, text):
        for i in range(len(text)):
            text[i] = self.check_emotes(text[i])
            if "http:" in text[i]:
                text[i] = "URL"
            elif "@" in text[i]:
                text[i] = "USER"

    ## Outputs the bigrams of the supplied text/sentence.
    # Constructs and returns the bigrams of the provided sentence.
    # @param self The object pointer.
    # @param text The sentence to be broken down.
    # \returns  The bigrams of the sentence.
    def bigrams(self, text):
        text = self.tokenize(text)
        tmp = list()
        for i in range(0, len(text) - 1):
            tmp.append((text[i], text[i+1]))
        return tmp

    ## Returns "position", if any, of intensifier in a bigram.
    # @param self The object pointer.
    # @param word The bigram to be checked.
    # \returns  The "location" of intensifers in the bigram via Boolean values.
    def intensifier(self, word):
        intensifiers = ''' really very awful fantastically
        moderately not radically real quite holy fully frightfully
        amazingly bare dreadfully especially precious excessively
        extremely exceptionally dead crazy insanely incredibly
        right sick so somewhat strikingly remarkably terribly
        terrifically too totally unusually wicked veritable
        '''
        loc1 = True if word[0] in intensifiers else False
        loc2 = True if word[1] in intensifiers else False
        return loc1, loc2
