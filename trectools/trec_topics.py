from trectools.misc import remove_punctuation
from lxml import etree
import codecs
from bs4 import BeautifulSoup
import os

class TrecTopics:

    def __init__(self, topics={}):
        self.set_topics(topics)

    @classmethod
    def read_topics_from_file(cls, filename, topic_tag='topic', numberid_tag='number',
       number_attr=True, querytext_tag="query", encoding='ISO-8859-1', debug=False):
        # TODO: throw an exception for errors when reading the topics.
        trec_topics = cls()
        soup = BeautifulSoup(codecs.open(filename, "r", encoding=encoding), "lxml")

        for topic in soup.findAll(topic_tag):
            if number_attr:
                topic_id = topic.get(numberid_tag).strip()
            else:
                topic_id = topic.findNext(numberid_tag).getText().strip()

            query = topic.findNext(querytext_tag).getText().strip()
            if debug:
                print("Number: %s Query: %s" % (topic_id, query))
            trec_topics.set_topic(topic_id, query)
        return trec_topics
    
    def set_topics(self, topics):
        self.topics = topics

    def set_topic(self, topic_id, topic_text):
        self.topics[topic_id] = topic_text

    def clean_topics(self):
        result = {}
        for topid, text in self.topics.items():
            cleaned_text = remove_punctuation(text)
            result[topid] = cleaned_text
        self.topics = result

    def printfile(self, filename="output.xml", fileformat="terrier", outputdir=None, debug=True):
        """
            Writes out the topics to a file.
            After one runs this method, TrecTopics.outputfile is available with the
            filepath to the created file.
            fileformat: terrier, indri or indribaseline
        """
        if outputdir is None:
            outputdir = os.getcwd()

        self.outputfile = os.path.join(outputdir, filename)
        if debug == True:
            print("Writing topics to %s" % (self.outputfile))

        if fileformat == "terrier":
            # Creates file object
            root = etree.Element('topics')
            for qid, text in sorted(iter(self.topics.items()), key=lambda x:x[0]):
                topic = etree.SubElement(root, 'top')
                tid = etree.SubElement(topic, 'num')
                tid.text = str(qid)
                ttext = etree.SubElement(topic, 'title')
                ttext.text = text
        elif fileformat == "indri" or fileformat == "indribaseline":
            root = etree.Element('parameters')
            trecformat = etree.SubElement(root, 'trecFormat')
            trecformat.text = "true"
            for qid, text in sorted(iter(self.topics.items()), key=lambda x:x[0]):
                topic = etree.SubElement(root, 'query')
                tid = etree.SubElement(topic, 'id')
                tid.text = str(qid)
                ttext = etree.SubElement(topic, 'text')
                cleaned_text = remove_punctuation(text)
                if fileformat == "indri":
                    ttext.text = "#combine( " + cleaned_text + " )"
                elif fileformat == "indribaseline":
                    ttext.text = cleaned_text

        f = open(self.outputfile, "w")
        f.writelines(etree.tostring(root, pretty_print=True))
        f.close()

