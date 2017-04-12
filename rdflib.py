# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 15:38:57 2016

@author: U6038155
"""

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF
import RDFClosure as rdfc
import pandas as pd

def query_rdf(data_file, query_file_name):
    g = rdflib.ConjunctiveGraph()
    g.parse("examples/"+data_file, format="nt")
    with open("examples/"+query_file_name) as query_file:
        sparql_query = query_file.read()
    result = g.query(sparql_query)
    return result
