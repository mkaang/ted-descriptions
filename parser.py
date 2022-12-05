#!/usr/bin/env python
# coding: utf-8

# import required libraries
import sys
import glob

import xml
from xml.dom import minidom

import random

import pandas as pd


def detect_lang(tree, node):
    while not node.hasAttribute("LG"):
        node = node.parentNode
    return node.getAttribute("LG")


def get_descr(tree, node):
    descr = ""
    if isinstance(node, minidom.Node):
        for c in node.childNodes:
            if (c.nodeType == 1):
                descr = descr + ' ' + c.toxml()[3:-4]
            else:
                for d in c.childNodes:
                    if (d.nodeType == 1):
                        descr = descr + ' ' + d.toxml()[3:-4]
    return descr


def parser_local(year):
    path = "..."
    fileList = glob.glob(path + str(year)+"/*.xml")

    data = []

    for file in fileList:
        try:
            DOMTree = xml.dom.minidom.parse(file)

            # TD_DOCUMENT_TYPE
            doc_type = DOMTree.getElementsByTagName('TD_DOCUMENT_TYPE')[0].getAttribute("CODE")
            # If document type is 3 Contract Notices 7 Contract Award Notices
            if doc_type == "7":

                # NO_DOC_OJS
                nodoc = DOMTree.getElementsByTagName('NO_DOC_OJS')[0].toxml()
                no_doc_ojs = nodoc.split("-")[0].split(">")[1][:4] + nodoc.split("-")[1].split("<")[0].lstrip("0")

                # LG_ORIG
                lg_orig = []
                for node in DOMTree.getElementsByTagName('LG_ORIG'):
                    lang = node.toxml().split(">")[1].split("<")[0]
                    lg_orig.append(lang)

                if len(lg_orig) == 1:
                    selected_orig = lg_orig[0]
                elif "EN" in lg_orig:
                    selected_orig = "EN"
                else:
                    selected_orig = random.choice(lg_orig)

                # SHORT_DESCR

                if DOMTree.getElementsByTagName('SHORT_DESCR'):
                    for node in DOMTree.getElementsByTagName('SHORT_DESCR'):

                        # Control whether related node is in selected language
                        if detect_lang(DOMTree, node).strip() == selected_orig:
  
                            if node.parentNode.tagName == "OBJECT_CONTRACT":
                                short_descr = get_descr(DOMTree, node)
                                

            data.append(no_doc_ojs, short_descr)

        except:
            pass

    columns = ["NO_DOC_OJS", "SHORT_DESCR"]

    pd.DataFrame(data, columns = columns).to_csv(f"{path}/descriptions_award_{str(year)}.csv")

if __name__ == "__main__":
    year = sys.argv[1]
    parser_local(year)


