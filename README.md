SimpleSentiPy
-------------
### A Simple Sentiment Analysis Tool ###
SimpleSentiPy is a simplified sentiment analysis tool developed using Python. It utilizes the sentiment values provided by [SentiWordNet](http://sentiwordnet.isti.cnr.it/) as its basis. It does not currently contain methods to train the sentiment values. Instead, it takes average values from SentiWordNet and uses those to calculate Overall, Positive, Negative, and Objective sentiment value scores.

The output values from this program range from -1 to 1, with -1 being very negative and 1 being very positive. All values are stored as floating point variables and are stored up to 4 decimal places.

----------------------------------------------
### Using SimpleSentiPy ###
An example of the basic functionality of SimpleSentiPy.

```python
from simpleSentiPy import SentimentAnalysis

ssp = SentimentAnalysis()
ssp.sentiment("This is a good test sentence")
ssp.bigram_sent("This is another very good test sentence")
ssp.batch_proc(("This is the first bad test sentence",\
  "This is hopefully a better test sentence")
ssp.file_proc("test_sentences.txt")
```

SentiWordNet is included, however, should it change, replace the current SimpleSentiPy.txt document with the newest version of SentiWordNet and run the following command:
```python
python fileGen.py
```
which will produce a new data.pkl file, which is the actual data-file used for sentiment analysis.

--------------------------------------------------
### What's Included ###
* simpleSentiPy.py - The python script including the main SentimentAnalysis class
* util.py - A class of helper functions for the SentimentAnalysis class
* fileGen.py - A class to regenerate the data.pkl file based on SimpleSentiPy.txt
* SimpleSentiPy.txt - The sentiment analysis values taken from [SentiWordNet](http://sentiwordnet.isti.cnr.it/) that have been averaged for this particular model. This is the file that would be edited to add new entries.
* data.pkl - The binary Pickle file used for data storage and reading-in.
