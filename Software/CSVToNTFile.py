import pandas as pd
from rdflib import Graph, RDF, URIRef, Literal, XSD


def read_nt(file):
    graph = Graph()
    graph.parse(file, format='nt')
    return graph


def unreify_statements(file):
    reified_statements = read_nt(file)
    new_graph = Graph()
    reification_dict = {}
    for stmt_uri in reified_statements.subjects(RDF.type, RDF.Statement):
        subject = reified_statements.value(stmt_uri, RDF.subject)
        predicate = reified_statements.value(stmt_uri, RDF.predicate)
        obj = reified_statements.value(stmt_uri, RDF.object)
        new_graph.add((subject, predicate, obj))
        key = (str(subject), str(predicate), str(obj))
        reification_dict[key] = stmt_uri
    return new_graph, reification_dict


# read reified statements, turn to NT
dataset="FAVEL"
folder="FaVEL"

# trainingData, train_dict = unreify_statements(f"/home/aams/Desktop/FAVEL_reified/{dataset}_train_reified.nt")
testingData, test_dict = unreify_statements(f"./FAVEL_ALL_RESULTS/{folder}/reified/{dataset}_test_reified.nt")

# read file with all results
favel_result = pd.read_csv(f"./favel/Evaluation/test/input/Output_it0.csv")

# create NT file for each column of the dataframe
approaches = ("ensemble_score",)
truth_pred = URIRef("http://swc2017.aksw.org/hasTruthValue")
for approach in approaches:
    approach_graph = Graph()
    partial = favel_result[['subject', 'predicate', 'object', approach]]
    for i, row in partial.iterrows():
        s, p, o, a = row
        stmt_uri = test_dict[(s,p,o)]
        approach_graph.add((URIRef(stmt_uri), truth_pred, Literal(a, datatype=XSD.double)))
    # save to file
    approach_graph.serialize(destination=f"./favel/Evaluation/test/input/{dataset}_{approach}_test.nt",
                             format="nt")
