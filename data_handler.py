import csv

import myutility


def get_data(ourfile):
    data=[]
    with open (ourfile, 'r') as mydata:
        mydata = csv.DictReader(mydata)
        for line in mydata:
            line['submission_time'] = int(line['submission_time'])
            line['vote_number'] = int(line['vote_number'])
            if ourfile == "sample_data/question.csv":
                line['view_number'] = int(line['view_number'])
            data.append(line)
    return data



def write_data(ourfile, data, header):
    with open (ourfile, 'w') as mydata:
        mydata = csv.DictWriter(mydata, fieldnames=header)
        mydata.writeheader()
        for item in data:
            item["id"] = data.index(item) + 1
        for line in data:
            mydata.writerow(line)