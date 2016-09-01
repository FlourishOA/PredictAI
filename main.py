import csv
import scipy.io
from scipy.sparse import csr_matrix, coo_matrix
with open("data/journal_list.csv", "r") as f:
    names_in_matrix = next(csv.reader(f))
for name in names_in_matrix:
    print name
venue_matrix = scipy.io.mmread("./data/mag_venue_sparse.mtx").tocsr()
print venue_matrix.shape
