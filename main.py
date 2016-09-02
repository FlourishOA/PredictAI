import json
import csv
import scipy.io
from scipy.sparse import csr_matrix, coo_matrix
from scipy.stats import stats
import numpy as np
with open("data/journal_list.csv", "r") as f:
    ids_in_matrix = next(csv.reader(f))

id_to_name = {}
with open("data/journal_names.tsv") as f:
    id_to_name = {i: j for (i,j) in csv.reader(f, dialect=csv.excel_tab)}

venue_matrix = scipy.io.mmread("./data/mag_venue_sparse.mtx").tocsr()
print venue_matrix.shape
it_mtx = coo_matrix(venue_matrix)
old_row = 0
row_sum = 0
id_to_citations = {}
for row,col,data in zip(it_mtx.row, it_mtx.col, it_mtx.data):
    if ids_in_matrix[row][0] == "B":
        continue
    if row == old_row:
        row_sum += data
    else:
        id_to_citations[ids_in_matrix[row-1][1:]] = row_sum
        row_sum = data
        old_row = row

# catching final journal edge case
id_to_citations[ids_in_matrix[row-1][1:]] = row_sum

name_to_citations = {}
for key in id_to_citations:
    if key in id_to_name:
        name_to_citations[id_to_name[key]] = id_to_citations[key]

name_to_ai = {}
name_to_issn = {}

with open("./data/journals_EF_AI_2014.txt") as f:
    for row in csv.reader(f, dialect=csv.excel_tab):
        name_to_ai[row[3]] = row[15]
        name_to_issn[row[3]] = row[1]

valid_names = set()

# finding journals we have pricing info for
with open("./data/journal_requests.json") as f:
    json_data = json.loads(f.read())
    for i in json_data:
        valid_names.add(i['journal_name'])

valid_count = 0
no_ai_count = 0
citations_list = []
ai_list = []
tb_predicted = []
# building the name -> citations map,
# as well as the regression lists
# (using citations to predict ArticleInfluence)

for name in name_to_citations:
    if name in name_to_ai:
        valid_count += 1
        citations_list.append(name_to_citations[name])
        ai_list.append(name_to_ai[name])
    elif name in valid_names:
        print name
        tb_predicted.append(name)
        no_ai_count += 1

print "For training: " + str(valid_count)
print "To be predicted: " + str(no_ai_count)

# actually performing the regression
slope, intercept, r_val, p_val, std_err = stats.linregress(
        np.array(citations_list).astype(np.float),
        np.array(ai_list).astype(np.float)
        )

