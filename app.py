import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import collect
from flask_wtf import Form
from wtforms import SubmitField

# import MySQLdbff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ky1015'

# A simple function to verify if user's input is legal.
# Can potientialy eliminate a lot of malicous searches by hackers.
dpt_list = ["CSCE", "AERO", "BMEN", "CHEN",
            "SENG", "CVEN", "ENGR", "ICPE", "ECEN", "TCMT", "IDIS",
            "ESET", "ISEN", "MSEN", "MEEN", "MMET", "NUEN", "OCEN", "PETE",
            "ASCC", "AGCJ", "ALEC", "ALED", "UGST", "ARCH", "CARC", "VIZA",
            "VIST", "URSC", "ARTS", "COSC", "CARC", "ENDS", "ACCT", "BUAD",
            "BUSN", "IBUS", "FINC", "ISTM", "SCMT", "OBIO", "DDHS", "CEHD",
            "EDAD", "EHRD", "TCMG", "BEFB", "BIED", "CPSY", "EDTC", "EPFB",
            "EPSY", "INST", "SPED", "SPSY", "ATTR", "DCED", "HEFB", "HLTH",
            "KINE", "KNFB", "SPMT", "EDCI", "MASC", "MEFB", "RDNG", "TEFB",
            "BUSH", "INTA", "PSAA", "ATMO", "GEOS", "WMHS", "GEOG", "GEOL",
            "GEOP", "OCNG", "ANTH", "AFST", "FILM", "LBAR", "HHUM", "RELS",
            "WGST", "COMM", "JOUR", "ECMT", "ECON", "ENGL", "SPAN", "HIST",
            "HISP", "LING", "ARAB", "ASIA", "CHIN", "CLAS", "FREN", "GERM",
            "INTS", "JAPN", "MODL", "RUSS", "MUSC", "PERF", "THAR", "PHIL",
            "POLS", "PSYC", "SOCI", "EDHP", "HCPI", "MPIM", "MSCI", "AERS",
            "SOMS", "MLSC", "NVSC", "NURS", "PHEO", "PHEB", "PHPM", "HPCH",
            "PHLT", "SOPH", "BIOL", "CHEM", "NRSC", "MATH", "ASTR", "PHYS",
            "STAT", "BIMS", "VMID", "VIBS", "VTPP", "VTMI", "VTPB", "AGEC",
            "AGLS", "AGSC", "AGSM", "ANSC", "ECEN", "MKTG", "BICH", "RPTS",
            "SCSC", "WFSC", "ENTO", "ESSM", "GENE", "HORT", "OCNG", "URPN",
            "RDNG", "NFSC", "POSC", "RENR", "OCEN", "L,", "ECMT", "ICPE",
            "BESC", "PLAN", "FIVS", "NUTR", "PLPA", "FSTC", "TCMT", "LDEV",
            "ISYS", "EEBL", "ITAL", "ORTH", "TEED", "MEPS", "SEFB", "BIOT",
            "SCEN", "DASC", "MEMA", "ENTC", "EVEN", "VPAT", "CEHD", "STLC",
            "AEGD", "OBIO", "EURO", "VMID", "AREN"]


def validaiton(dpt, num):
    if (num > 700 or num < 99):
        print("num")
        return 0
    if (len(dpt) != 4):
        print("len")
        return 0
    for i in dpt_list:
        # print(i)
        if (dpt.upper() == i):
            # print("dpt: ", dpt.upper())
            return 1
    return 1


def validaiton2(dpt):
    if (len(dpt) != 4):
        print("len")
        return 0
    for i in dpt_list:
        # print(i)
        if (dpt.upper() == i):
            # print("dpt: ", dpt.upper())
            return 1
    return 1


@app.route("/", methods=['GET', 'POST'])
def test():
    # collect info from user's input
    form = collect()
    # if inputs are valid, then redirect to table.html
    if (form.validate_on_submit()):
        department = form.department.data
        number = form.course_number.data
        d_name = form.d_name.data
        p_name = form.p_name.data
        if department and number and (validaiton(department, number) == 1):
            return redirect(url_for('table', dpt=department, num=number))
        elif d_name and validaiton2(d_name):
            return redirect(url_for('table2', dpt=d_name))
        elif p_name:
            return redirect(url_for('table3', prf=p_name))
    # if inputs aren't valid, enter again (this portion is not working properly)
    # flash("Invalid input")

    return render_template("collect.html", form=form)


# this route output the Department, Course num, GPA, % of A, % of B, Professor's name, Semester

@app.route("/table/<dpt>/<num>", methods=['GET', 'POST'])
def table(dpt, num):
    headings = ["Department", "Course num", "Section", "GPA", "% of A", "% of B", "Professor's name", "Semester"]
    headings2 = ["Course title", "Counted hours", "Description"]
    # Connect to an existing database
    dname = dpt.upper()
    cnum = str(num)
    conn = psycopg2.connect(user="aarhjdaudxfplo",
                            password="2d9ff8028281f542340345273cef367c213a62d6ac67276dfaee05919acd0b11",
                            host="ec2-54-156-121-167.compute-1.amazonaws.com",
                            port="5432",
                            database="dfqcb386c03jnf")
    cur = conn.cursor()

    if (cur.execute("SELECT dept_name,course_num,sect_num,sect_gpa,sect_a_pcnt,sect_b_pcnt,prof_name,sect_semester FROM\
     \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id \
     WHERE dept_name= \'%s\' and course_num =\'%s\' ORDER BY sect_semester desc;" % (dname, cnum))):
        print(dname)

    elif (request.form.get('action1')):
        cur.execute("SELECT dept_name,course_num,sect_num,sect_gpa,sect_a_pcnt,sect_b_pcnt,prof_name,sect_semester FROM\
             \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id \
             WHERE dept_name= \'%s\' and course_num =\'%s\' ORDER BY sect_gpa desc;" % (dname, cnum))
    elif (request.form.get('action2')):
        cur.execute("SELECT dept_name,course_num,sect_num,sect_gpa,sect_a_pcnt,sect_b_pcnt,prof_name,sect_semester FROM\
             \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id \
             WHERE dept_name= \'%s\' and course_num =\'%s\' ORDER BY prof_name desc;" % (dname, cnum))
    elif (request.form.get('action3')):
        cur.execute("SELECT dept_name,course_num,sect_num,sect_gpa,sect_a_pcnt,sect_b_pcnt,prof_name,sect_semester FROM\
             \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id \
             WHERE dept_name= \'%s\' and course_num =\'%s\' ORDER BY sect_semester desc;" % (dname, cnum))
    else:
        cur.execute("SELECT dept_name,course_num,sect_num,sect_gpa,sect_a_pcnt,sect_b_pcnt,prof_name,sect_semester FROM\
             \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id \
             WHERE dept_name= \'%s\' and course_num =\'%s\';" % (dname, cnum))  # fetch the data , render the page.
    fetching = cur.fetchall()

    cur.execute(
        "SELECT course_title,course_hours,course_description FROM \"Courses\" WHERE dept_name= \'%s\' and course_num =\'%s\';" % (
        dname, cnum))
    # cur.execute("SELECT * FROM \"Department\";")
    fetching2 = cur.fetchall()
    cur.close()
    return render_template("table.html", headings=headings, headings2=headings2, data=fetching, data2=fetching2)


# this route output the address, office phone number, and email of a specific department
@app.route("/table2/<dpt>/", methods=['GET', 'POST'])
def table2(dpt):
    # connect to the database
    headings = ["Department", "Address", "Phone Number", "Email"]
    # Connect to an existing database
    dname = dpt.upper()
    # cnum = str(num)
    conn = psycopg2.connect(user="aarhjdaudxfplo",
                            password="2d9ff8028281f542340345273cef367c213a62d6ac67276dfaee05919acd0b11",
                            host="ec2-54-156-121-167.compute-1.amazonaws.com",
                            port="5432",
                            database="dfqcb386c03jnf")  # create cursor to fetch the data
    cur = conn.cursor()
    if (cur.execute("SELECT dept_name,dept_office_address,dept_phone,dept_email FROM\
     \"Department\" WHERE dept_name= \'%s\' ORDER BY dept_name;" % (dname))):
        print(dname)
    else:
        cur.execute("SELECT dept_name,dept_office_address,dept_phone,dept_email FROM\
            \"Department\" WHERE dept_name= \'%s\' ORDER BY dept_name;" % (dname))  # fetch the data , render the page.

    fetching = cur.fetchall()
    cur.close()
    return render_template("table2.html", headings=headings, data=fetching)


# this route output the professor name, rate my professor link and courses they teach
@app.route("/table3/<prf>/", methods=['GET', 'POST'])
def table3(prf):
    # connect to the database
    headings = ["Professor", "Department", "Course Number", "Link"]
    # Connect to an existing database
    pname = prf.upper()
    # cnum = str(num)
    conn = psycopg2.connect(user="aarhjdaudxfplo",
                            password="2d9ff8028281f542340345273cef367c213a62d6ac67276dfaee05919acd0b11",
                            host="ec2-54-156-121-167.compute-1.amazonaws.com",
                            port="5432",
                            database="dfqcb386c03jnf")  # create cursor to fetch the data
    cur = conn.cursor()
    if (cur.execute("SELECT prof_name,dept_name,course_num FROM\
     \"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id WHERE prof_name= \'%s\' GROUP BY prof_name,dept_name,course_num;" % (
    pname))):
        print(pname)
    else:
        cur.execute("SELECT C.prof_name,dept_name,course_num ,prof_rmp_link FROM\
            (\"Section\" INNER JOIN \"Courses\" C on C.course_id = \"Section\".course_id) AS C INNER JOIN \"Professors\" P on P.prof_name = C.prof_name WHERE C.prof_name= \'%s\'\
            GROUP BY C.prof_name,prof_rmp_link,dept_name,course_num;" % (pname))  # fetch the data , render the page.

    fetching = cur.fetchall()
    cur.close()
    return render_template("table2.html", headings=headings, data=fetching)


if __name__ == '__main__':
    # app.config['DEBUG'] = True
    app.run()


