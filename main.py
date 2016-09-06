import json
import csv
import scipy.io
from scipy.sparse import csr_matrix, coo_matrix
from scipy.stats import stats
import numpy as np


valid_names = set()

# finding journals we have pricing info for
with open("./data/journal_requests.json") as f:
    json_data = json.loads(f.read())
    for i in json_data:
        valid_names.add(i['journal_name'])

with open("data/journal_list.csv", "r") as f:
    ids_in_matrix = [i[1:] for i in next(csv.reader(f))]

with open("data/journal_names.tsv") as f:
    id_to_name = {i: j for (i, j) in csv.reader(f, dialect=csv.excel_tab)}

venue_matrix = scipy.io.mmread("./data/mag_venue_sparse.mtx")
n = venue_matrix.shape[0]
summed = venue_matrix.sum(axis=1)

name_to_citations = {id_to_name[ids_in_matrix[i]]: mtx[0,0]
                     for i, mtx in enumerate(summed)
                     if ids_in_matrix[i] in id_to_name}

with open("./data/journals_EF_AI_2014.txt") as f:
    name_to_info = {row[3]: (row[15], row[1]) for row in csv.reader(f, dialect=csv.excel_tab)}

# (name, citations)
to_be_predicted = [(key, name_to_citations[key])
                   for key in name_to_citations
                   if key not in name_to_info and key in valid_names]

# (name, citations, AI)
training_data = [(key, name_to_citations[key], name_to_info[key][0])
                 for key in name_to_citations if key in name_to_info]

print len(training_data)
print len(to_be_predicted)
with open("./output/training_data.csv", "w") as f:
    writer = csv.writer(f)
    for row in training_data:
        writer.writerow(row)

with open("./output/to_be_predicted.csv", "w") as f:
    writer = csv.writer(f)
    for row in to_be_predicted:
        writer.writerow(row)