import csv
import scipy.io
from scipy.sparse import csr_matrix, coo_matrix
with open("data/journal_list.csv", "r") as f:
    names_in_matrix = next(csv.reader(f))

venue_matrix = scipy.io.mmread("./data/mag_venue_sparse.mtx").tocsr()
print venue_matrix.shape
it_mtx = coo_matrix(venue_matrix)
old_row = 0
row_sum = 0
name_to_citations = {}
for row,col,data in zip(it_mtx.row, it_mtx.col, it_mtx.data):
    if names_in_matrix[row][0] == "B":
        continue
    if row == old_row:
        row_sum += data
    else:
        name_to_citations[names_in_matrix[row-1]] = row_sum
        row_sum = data
        old_row = row
for key in name_to_citations:
    print str(key) + ": " + str(name_to_citations[key])
