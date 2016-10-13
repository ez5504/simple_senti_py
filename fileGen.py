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
import cPickle as pickle

## File generator for SimpleSentiPy.
# A class to read in the SentiWordNet lexicon and create a dictionary. This
# dictionary gets written out as a Python Pickle file for use in the main
# SimpleSentiPy class, SentimentAnalysis.
class FileGen():

    ## Dictionary to temporarily store the contents of SentiWordNet.
    senti = dict()

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

    ## FileGen
    # Reads in SentiWordNet, appends the POS of the word to it, and adds it to
    # the senti dictionary which will later be written to a file.
    # @param self The object pointer.
    def __init__(self):
        with open("SimpleSentiPy.txt", "r") as f:
            while True:
                new_lines = list(islice(f, 30))
                if not new_lines:
                    break
                for line in new_lines:
                    # ignore lines beginning with # to disregard commented lines
                    if line.startswith("#"):
                        continue
                    else:
                        line = line.split()
                        for i in range(0, len(line)-1):
                            if line[i].find("#") != -1:
                                self.trim(line[i], "#")
                            if i > 4 and line[i].find("#") == -1:
                                # intial setup for each entry
                                vals =[float(line[2]), float(line[3]), 1.0]
                                keys = line[4:i]
                                for i in keys:
                                    if "_" in i:
                                        # ignores multi-word entries
                                        continue
                                    i = self.trim(i, "#")
                                    i += "/" + line[0]
                                    if i in self.senti:
                                        # adjusts existing entry with new values
                                        tmp = self.senti.get(i)
                                        if tmp[0] == 0 and tmp[1] == 0:
                                            continue
                                        tmp[0] += vals[0]
                                        tmp[1] += vals[1]
                                        tmp[2] += 1
                                        self.senti.update({i:tmp})
                                    else:
                                        # adds entry if not in dict
                                        self.senti.update({i:vals})
                                break
        # calculates the "average" values, if there are multiples of the word
        # with the same POS
        for key, val in self.senti.iteritems():
            val[0] = val[0] / val[2]
            val[1] = val[1] / val[2]
            val[2] = 1
        pickle.dump(self.senti, open("data.pkl", "wb"), pickle.HIGHEST_PROTOCOL)

c = FileGen()
