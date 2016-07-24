# External libraries
import sarge
import os

from trectools import TrecRun

#TODO: sourceforce was offline when I wrote this code. I need to get to the docs to check regarinding the baselines and how to specify them.
class TrecIndri:

    def __init__(self, bin_path):
        self.bin_path = bin_path

    def run(self, index, topics, model="LM", server=None, stopper=None, result_dir=None, result_file="trec_indri.run", ndocs=1000, qexp=False, expTerms=5, expDocs=3, showerrors=True, debug=True, queryOffset=1):

        if result_dir is None:
            # Current dir is used if result_dir is not set
            result_dir = os.getcwd()

        outpath = ""
        if result_dir is not None and result_file is not None:
            outpath = os.path.join(result_dir, result_file)
        elif result_file is not None:
            outpath = result_file

        cmd = "%s %s -index=%s -trecFormat=true -queryOffset=%d " % (self.bin_path, topics, index, queryOffset)

        # Specify number of documents to retrieve
        cmd += " -count=%d " % (ndocs)

        if server is not None:
            cmd += " -server=%s " % (server)

        if stopper is not None:
            cmd += " -stopper.word=%s " % (stopper)

        if qexp == True:
            cmd += " -fbDocs=%d -fbTerms=%d " % (expTerms, expDocs)

        if showerrors == True:
            cmd += (" > %s " % (outpath))
        else:
            cmd += (" 2> %s > %s "  % (os.devnull, outpath))

        if debug:
            print "Running: %s " % (cmd)

        r = sarge.run(cmd).returncode

        if r == 0:
            return TrecRun(os.path.join(result_dir, result_file))
        else:
            print "ERROR with command %s" % (cmd)
            return None

#tt = TrecIndri(bin_path="/data/palotti/terrier/terrier-4.0-trec-cds/bin/trec_terrier.sh")
#tr = tt.run(index="/data/palotti/terrier/terrier-4.0-trec-cds/var/index", topics="/data/palotti/trec_cds/metamap/default_summary.xml.gz", qexp=False)

