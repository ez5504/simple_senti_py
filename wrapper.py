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
