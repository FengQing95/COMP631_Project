import csv
from csv import reader

csvfile = open('yelp_houston.csv', 'r')
dic = {}

csv_reader = reader(csvfile)
id = 0
for row in csv_reader:
    id = id+1
    f = open('./houston_file/' + str(id) + '.csv', 'w+')
    f.writelines(row[1] + '////' + row[2])

'''
for row in range(len(csvfile)):
    # print(csvfile[i])
    name = csvfile[i].split(',')[1]
    if name not in dic.keys():
        dic[name] = 1
    else:
        dic[name] += 1
    # print(name)
    review = csvfile[i].replace(name, '')
    # print(review)
    open(str(name) + str(dic[name]) + '.csv', 'w+').writelines(review)
    i += 1
'''