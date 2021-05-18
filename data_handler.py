import csv


def get_data(ourfile):
    data=[]
    with open (ourfile, 'r') as mydata:
        mydata = csv.DictReader(mydata)
        for  line in mydata:
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