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

from simpleSentiPy import SentimentAnalysis
c = SentimentAnalysis()

## Wrapper function for SimpleSentiPy for use in Prediction Analysis project.
#
# @param array_queries A list of queries to be analyzed
def sspsentiment(array_queries, isConcept, default=""):
    for qry in array_queries:
        if qry != "":
            if isConcept == 1:
                infile = "raw_text/" + qry + "/" + qry + ".txt"
                outfile = "output_files/" + default + "/concepts/" + qry + ".txt"
                raw_out = "output_files/" + qry + "/concepts/sspraw-" + qry + ".txt"
            else:
                infile = "raw_text/" + qry + "/" + qry + ".txt"
                outfile = "output_files/" + qry + "/" + qry + "_ssp.txt"
                raw_out = "output_files/" + qry + "/sspraw-" + qry + ".txt"
            try:
                c.file_proc(infile, outfile, raw_out)
            except:
                return False
    return True
