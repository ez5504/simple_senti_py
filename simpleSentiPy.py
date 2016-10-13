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
import re
import os
from itertools import *
from util import Utility
import cPickle as pickle
import math

## Main class of SimpleSentiPy.
# SimpleSentiPy is a simplified sentiment analysis tool designed in Python.
# The primary method uses a naive bigram sentiment analysis to allow for context.
# Used in conjunction with the accompanying Utility class, text gets tokenized and processed
# to remove emotes, "laugh" text, URLs and Twitter usernames. After, bigrams are generated
# which are later passed through a function to check for intensifiers which adjust the output
# accordingly, depending on the context around it.
class SentimentAnalysis():

    ## Dictionary to store sentiment values
    senti = dict()
    ## Creates an instance of the Utility object
    util = Utility()

    ## Normalizes the sentiment values and returns the overall "average" score
    #
    # @param self The object pointer.
    # @param pos The positive total of the sentence
    # @param neg The negative total of the sentence
    # @param alpha Weighted value used for averaging
    # \returns  The overall sentiment value of the sentence
    def normalize(self, pos, neg, alpha=15):
        sum = pos - neg
        norm = sum / math.sqrt((sum * sum) + alpha)
        return norm

    ## Basic Sentiment Parsing
    #
    # @param self The object pointer.
    # @param text The line of text being analyzed
    # \returns A string with Overall, Positive, Negative, and Neutral/Objective sentiment values
    def sentiment(self, text):
        words = self.util.tokenize(text) # Runs text through Utility tokenizer
        pos = 0.0
        neg = 0.0
        posCt = 0
        negCt = 0
        for word in words:
            # first the SentiWordNet POS's get appended to the word
            keys =[word + "/r", word + "/a", word+"/n", word+"/e", word+"/v"]
            for key in keys:
                # Checks to see if new "key" exists in the dictionary
                if key in self.senti:
                    tmp = self.senti[key]
                    if(tmp[0] > 0):
                        pos += float(tmp[0]) # Add positive sentiment vals to positive total (pos)
                        posCt += 1
                    if(tmp[1] > 0):
                        neg += float(tmp[1]) # Add negative sentiment vals to negative total (neg)
                        negCt += 1
                else:
                    continue
        overall = self.normalize(pos, neg)
        if posCt > 0:
            pos /= float(posCt) # Calculates positive portion of sentiment
        if negCt > 0:
            neg /= float(negCt) # Calculates negative portion of sentiment
        obj = 1.0 - (pos + neg) # calculate objective (neutral) portion of sentiment
        pos = "{0:.4f}".format(pos); neg = "{0:.4f}".format(neg)
        overall = "{0:.4f}".format(overall); obj = "{0:.4f}".format(obj)
        out = "Overall: {:>7} Pos: {:>6} Neg: {:>6} Obj: {:>6}\n".format(overall, pos, neg, obj)
        return out

    ## Processes multiple sentences in a list
    #
    # @param self The object pointer.
    # @param sentences A list of sentences to be analyzed
    def batch_proc(self, sentences):
        for sentence in sentences:
            result = self.bigram_sent(sentence)
            print(result)

    ## Processes sentences as bigrams (pairs of words)
    #
    # @param self The object pointer.
    # @param text The line/sentence being analyzed
    # \returns A string with Overall, Positive, Negative, and Neutral/Objective sentiment values
    def bigram_sent(self, text):
        bigrams = self.util.bigrams(text) # Tokenizes text and returns bigrams
        pos = 0
        neg = 0
        posCt = 0
        negCt = 0
        flag = 0
        for bigram in bigrams:
            loc1, loc2 = self.util.intensifier(bigram) # gets location of intensifier in bigram (0 or 1)
            word1 = bigram[0]; word2 = bigram[1]
            keys =[word1+"/r", word1+"/a", word1+"/n", word1+"/e", word1+"/v"]
            keys += [word2+"/r", word2+"/a", word2+"/n", word2+"/e", word2+"/v"]
            for key in keys:
                if key in self.senti:
                    tmp = self.senti[key]
                    if(tmp[0] > 0):
                        # if first word is positive intensifier and second is regular word
                        if loc1 == True and loc2 == False:
                            pos += 1.25
                            neg -= 1
                        pos += float(tmp[0])
                        posCt += 1
                        flag = 0
                    if(tmp[1] > 0):
                        # if first word is negative intensifier and second is regular word
                        if loc1 == True and loc2 == False:
                            neg += 1.25
                            pos -= 1
                        neg += float(tmp[1])
                        negCt += 1
                        flag = 1
                else:
                    continue
            # if bigram contains two intensifier values
            if loc1 == True and loc2 == True:
                if flag == 1:
                    neg += 1.0
                    pos -= 0.5
                elif flag == 0:
                    pos += 1.0
                    neg -= 0.5
        # gets averaged overall sentiment score
        overall = self.normalize(pos, neg)
        if posCt > 0:
            pos /= float(posCt)
        if negCt > 0:
            neg /= float(negCt)
        obj = 1.0 - (pos + neg)
        out = "Overall: " + "{0:.4f}".format(overall) + " Pos: " + "{0:.4f}".format(pos)
        out += " Neg: " + "{0:.4f}".format(neg) + " Obj: " + "{0:.4f}".format(obj) + "\n"
        return out

    ## Processes multiple sentences from a file
    #
    # @param self The object pointer.
    # @param infile The file containing all of the sentences.
    # @param outfile The file to which overall values will be written.
    # @param raw_out The file to which all "raw" data will be written.
    def file_proc(self, infile, outfile, raw_out):
        with open(infile, "r") as inf:
            if os.path.isfile(infile):
                with open(outfile, "w") as out:
                    if os.path.isfile(outfile):
                        with open(raw_out, "w") as raw:
                            if os.path.isfile(raw_out):
                                while True:
                                    new_lines = list(islice(inf, 30)) # reads file 30 lines at a time
                                    if not new_lines:
                                        break
                                    for line in new_lines:
                                        result = self.bigram_sent(line)
                                        raw.write(result) # writes raw (all) output to raw file
                                        result = str(result.split()[1]) + "\n"
                                        out.write(result) # writes only overall score to main output file
                            else:
                                return False
                                raise raw_out
                            raw.close()
                    else:
                        return False
                        raise outfile
                    out.close()
            else:
                return False
                raise infile
            inf.close()


    ## Class Constructor
    # loads data from Pickle file upon object creation
    # @param self The object pointer.
    def __init__(self):
        self.senti = pickle.load(open("simple_senti_py/data.pkl", "rb"))
