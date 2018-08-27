import sys
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring
from xml.dom import minidom

class LTML(object):
    def __init__(self, xmlstr = None, encoding="utf-8"):
        if xmlstr is not None:
            self.dom = ET.fromstring(xmlstr)

    def _set_sent_on_note(self):
        self.note.set("sent", "y")

    def _set_word_on_note(self):
        self._set_sent_on_note()
        self.note.set("word", "y")

    def _set_pos_on_note(self):
        self._set_word_on_note()
        self.note.set("pos", "y")

    def _set_ne_on_note(self):
        self._set_pos_on_note()
        self.note.set("ne", "y")

    def _set_parser_on_note(self):
        self._set_pos_on_note()
        self.note.set("parser", "y")

    def _set_semantic_parser_on_note(self):
        self._set_pos_on_note()
        self.note.set("semparser", "y")

    def _set_semantic_graph_parser_on_note(self):
        self._set_pos_on_note()
        self.note.set("lstmsemparser", "y")

    def _set_srl_on_note(self):
        self._set_parser_on_note()
        self.note.set("srl", "y")

    def _set_all_on_note(self):
        self._set_srl_on_note()
        self.note.set("ne", "y")

    def _clean_note(self):
        self.note.set("sent",          "n")
        self.note.set("word",          "n")
        self.note.set("pos",           "n")
        self.note.set("ne",            "n")
        self.note.set("parser",        "n")
        self.note.set("semparser",     "n")
        self.note.set("lstmsemparser", "n")
        self.note.set("srl",           "n")

    # build ltml from string
    #
    #   @param[in]  buffer      the string buffer
    #   @param[in]  encoding    the encoding
    #   @return     the xml
    def build(self, buffer, encoding="utf-8"):
        self.xml4nlp = Element('xml4nlp')
        self.note    = SubElement(self.xml4nlp, 'note')
        self.doc     = SubElement(self.xml4nlp, 'doc')

        para    = SubElement(self.doc, 'para')
        para.set("id", "0")
        para.text = buffer.decode(encoding)

        self._clean_note()
        self.dom = self.xml4nlp

    # 
    # build ltml from words, automatically detect input type
    #
    #   @param[in]  words       the words, list(str), list(list), 
    #                           list(tuple) is supported
    def build_from_words(self, words, encoding="utf-8"):
        if isinstance(words, str):
            self.build(words)
        elif isinstance(words, list):
            flag = "seg"
            assert len(words) > 0

            word = words[0]
            if isinstance(word, str):
                flag = "seg"
            elif ((isinstance(word, list) or isinstance(word, tuple))
                    and len(word) == 2
                    and isinstance(word[0], str)
                    and isinstance(word[1], str)):
                flag = "pos"
            elif ((isinstance(word, list) or isinstance(word, tuple))
                    and len(word) == 4
                    and isinstance(word[0], str)
                    and isinstance(word[1], str)):
                flag = "dp"
            else:
                flag = "unknown"

            self.xml4nlp = Element('xml4nlp')
            self.note    = SubElement(self.xml4nlp, 'note')
            self.doc     = SubElement(self.xml4nlp, 'doc')

            para    = SubElement(self.doc, 'para')
            sent    = SubElement(para, 'sent')

            para.set("id", "0")
            sent.set("id", "0")

            self._clean_note()

            if flag == "seg":
                for i, word in enumerate(words):
                    sent.append(Element('word', {
                        'id': ('%d' % i),
                        'cont': word,}))

                sent.set('cont', ("".join(words)))
                self._set_word_on_note()
            elif flag == "pos":
                for i, wordpos in enumerate(words):
                    word, pos  = wordpos
                    sent.append(Element('word', {
                        'id': ('%d' % i),
                        'cont' : word.decode(encoding),
                        'pos' : pos,}))
                sent.set('cont', ("".join([word[0] for word in words])))
                self._set_pos_on_note()
            elif flag == "dp":
                for i, rep in enumerate(words):
                    word, pos, head, deprel = rep
                    sent.append(Element('word', {
                        'id': ('%d' % i),
                        'cont' : word.decode(encoding),
                        'pos' : pos,
                        'parent': str(int(head)-1),
                        'relation': deprel}))
                sent.set('cont', ("".join([word[0] for word in words])))
                self._set_parser_on_note()

            self.dom = self.xml4nlp

    def tostring(self, encoding="utf-8"):
        return tostring(self.dom, encoding)

    def prettify(self, encoding="utf-8"):
        """Return a pretty-printed XML string for the Element."""
        rough_string = tostring(self.dom, encoding)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t").encode(encoding)
