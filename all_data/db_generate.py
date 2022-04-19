# This is the py script to generate info from the office or registar

import tabula
import csv
import os


semester = "Spring2021/grd20211"
semester2 = "2020 Spring"
# # dpt = [ "AE", "AG", "AR", "AP", "BA", "ED","EN", "GB", "GE", "LA", "MS","NU","PH" ,"SC", "VM"]
# dpt = [  "AG", "AR", "BA", "ED","EN", "GB", "GE", "LA","MD","MS","SC", "VM"]
dpt = [  "EN" ]



for name in dpt:
    print("converting: "+semester + name +".pdf")

    tabula.convert_into(semester + name +".pdf", name+'_input.csv', output_format="csv", pages='all')


    with open(name+'_input.csv', 'r') as infile, open(semester + name + ".csv", "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(("course","prof","gpa","% of A","% of B","section_","semester"))
        for row in reader:
            if(row[0] != "" and row[0] != "COURSE TOTAL:" and row[0] != "DEPARTMENT TOTAL:" and
            row[0] != "COLLEGE TOTAL:"):
                writer.writerow((
                    (row[0][0]+row[0][1]+row[0][2]+row[0][3] + " " + row[0][5]+row[0][6]+row[0][7]), #course
                    row[14], #prof's name
                    row[7],"{0:.0f}%".format(int(row[1]) / int(row[6]) * 100),
                    "{0:.0f}%".format(int(row[2]) / int(row[6]) * 100), # , GPA, percent of A, percent of B
                    (row[0][9]+row[0][10]+row[0][11]), # section
                    semester2 # semester
                ))
        infile.close()
        outfile.close()
        os.remove(name+'_input.csv')
        os.remove(semester + name +".pdf")
    print(semester + name + ".csv"+" is done")

