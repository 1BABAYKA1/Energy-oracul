import pandas

file = pandas.read_csv("data.csv", delimiter=',', index_col=0)
print(file)