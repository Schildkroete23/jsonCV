#!/usr/bin/env python3
import json
import os
import sys

# read cv data in
with open(sys.argv[1], 'r') as jsonData:
    data = json.load(jsonData)

# write data to tex file
latex = "\\documentclass[11pt]{article}\n"
latex += "\\usepackage[ngerman]{babel}\n"
latex += "\\usepackage{fontawesome}\n"
# set main font type
latex += "\\setmainfont{SOURCE SANS PRO}\n"
latex += "\\usepackage{hyperref}\n"
latex += ("\\usepackage[a4paper, top=0.5cm, bottom=1cm, left=1cm, right=1cm]"
          "{geometry}\n")
latex += "\\usepackage{titlesec}\n"
latex += "\\titleformat{\\section}{\\Large\\scshape\\raggedright}{}{0ex}{}"
latex += "[\\titlerule]\n"
latex += "\\titlespacing*{\\section}{0em}{2ex}{2ex}\n"
latex += "\\titleformat{\\subsection}{\\large\\bfseries\\raggedright}{}"
latex += "{0ex}{}\n"
latex += "\\titlespacing*{\\subsection}{0ex}{2ex}{0ex}\n"
latex += "\\begin{document}%\n"
# turn off page numbering
latex += "\\pagenumbering{gobble}%\n"
# general information
latex += "\\noindent\n"
latex += "\parbox[t][.99\\textheight]{.25\\textwidth}{%\n"
latex += "\\vspace{0pt}%\n"
# picture
if data.get("picture", False):
    latex += "\\includegraphics[width=.25\\textwidth]{{{0}}}\n".format(
        data["picture"])
latex += "\\begin{tabbing}%\n"
latex += "{{\\huge\\scshape{{{0}}}}}".format(data["name"])
# job
if data.get("job", False):
    latex += "\\\\\n\\faBriefcase\\ {}".format(data["job"])
# address
if (data.get("street", False)
        or data.get("city", False)
        or data.get("country", False)):
    latex += "\\\\\n\\faHome\ \= "
    tab = False
if data.get("street", False):
    latex += "{}".format(data["street"])
    tab = True
if data.get("zip", False):
    if tab:
        latex += "\\\\\n\\>{} ".format(data["zip"])
    else:
        latex += "{} ".format(data["zip"])
        tab = True
if data.get("city", False):
    if tab and not data.get("zip", False):
        latex += "\\\\\n\\>{}".format(data["city"])
    else:
        latex += "{}".format(data["city"])
        tab = True
if data.get("country", False):
    if tab:
        latex += "\\\\\n\>{}".format(data["country"])
    else:
        latex += "\\\\\n{}".format(data["country"])
# email address
if data.get("mail", False):
    latex += "\\\\\n\\faEnvelope\\ \\href{{mailto:{0}}}{{{0}}}".format(
        data["mail"])
# phone number
if data.get("phone", False):
    latex += "\\\\\n\\faPhone\\ {0}".format(data["phone"])
# homepage
if data.get("homepage", False):
    latex += "\\\\\n\\faLink\\ \\href{{{0}}}{{{0}}}\n".format(data["homepage"])
latex += "\\end{tabbing}%\n"
latex += "{\\raggedright{%\n"
# personal data
if (data.get("nationality", False)
        or data.get("birthday", False)
        or data.get("birthplace", False)):
    latex += "\\subsection*{\\faInfo\\ Persönliche Daten}\n"
if data.get("nationality", False):
    latex += "Staatsangehörigkeit:\\\\ {\\textit{"
    counter = 0
    for nation in data["nationality"]:
        counter += 1
        latex += nation
        if counter != len(data["nationality"]):
            latex += ", "
    latex += "}}\\\\\n"
if data.get("birthday", False):
    latex += "Geburtsdatum:\\\\{{\\textit{{{}}}}}\\\\\n".format(
        data["birthday"])
if data.get("birthplace", False):
    latex += "Geburtsort:\\\\{{\\textit{{{}}}}}\\\\\n".format(
        data["birthplace"])
# languages
if data.get("languages", False):
    latex += "\\subsection*{\\faGlobe\\ Sprachen}\n"
    for language in data["languages"]:
        latex += language
        if language != data["languages"][-1]:
            latex += ", "
# coding skills
if data.get("coding", False):
    latex += "\n\\subsection*{\\faCode\\ Computerprachen}\n"
    for item in data["coding"]:
        latex += item
        if item != data["coding"][-1]:
            latex += ", "
# software skills
if data.get("software", False):
    latex += "\n\\subsection*{\\faDesktop\\ Software}\n"
    for item in data["software"]:
        latex += item
        if item != data["software"][-1]:
            latex += ", "
latex += "}}%\n"
latex += "\\vfill\n"
# place and date for signature
latex += "{}, \\today\\\\\n\\\\\n\\\\%\n}}%\n".format(data["city"])
latex += "\\hfill\\vline\\hfill%\n"
latex += "\parbox[t][.99\\textheight]{.7\\textwidth}{%\n"
latex += "\\vspace{0pt}%\n"
# education
if data.get("education", False):
    latex += "\\section*{\\faGraduationCap\\ Bildung}\n"
    for i in range(len(data["education"])):
        institute = data["education"][i]
        latex += "\\subsection*{{{0}}}\n".format(institute["institution"])
        latex += "\\faMapMarker\\ {}".format(institute["place"])
        if institute.get("end", False):
            latex += " \\ \\faCalendar\\ {} - {}".format(
                institute["begin"], institute["end"])
        else:
            latex += " \\ \\faCalendar\\ {}".format(institute["begin"])
        if institute.get("role", False):
            latex += "\\\\\n\\textit{{{0}}}".format(institute["role"])
        if institute.get("graduation", False):
            latex += "\\\\\nAbschluss: " + institute["graduation"]
        if institute.get("ba_topic", False):
            latex += "\\\\\nThema der Bachelorarbeit: "
            latex += institute["ba_topic"]
        if institute.get("focus", False):
            latex += "\\\\\nSchwerpunkte: "
            for item in institute["focus"]:
                latex += item
                if item != institute["focus"][-1]:
                    latex += ", "
# work experience
if data.get("work", False):
    latex += "\\section*{\\faGears\\ Arbeitserfahrung}\n"
    for company in data["work"]:
        latex += "\\subsection*{{{0}}}\n".format(company["company"])
        latex += "\\faMapMarker\\ {}".format(company["place"])
        if company.get("end", False):
            latex += " \\ \\faCalendar\\ {} - {}".format(
                company["begin"], company["end"])
        else:
            latex += " \\ \\faCalendar\\ {}".format(company["begin"])
        if company.get("duration", False):
            latex += " ({})".format(company["duration"])
        if company.get("role", False):
            latex += "\\\\\n\\textit{{{0}}}".format(company["role"])
        if company.get("tasks", False):
            latex += "\\\\\n"
            for task in company["tasks"]:
                latex += task
                if task != company["tasks"][-1]:
                    latex += ", "
        latex += "\n"
# civil service
if data.get("civil_service", False):
    latex += "\\section*{\\faGroup\\ Zivildienst}\n"
    for company in data["civil_service"]:
        tmpWord = ""
        for letter in company["company"]:
            if letter == '&':
                tmpWord += '\\'
            tmpWord += letter
        company["company"] = tmpWord
        latex += "\\subsection*{{{0}}}\n".format(company["company"])
        latex += "\\faMapMarker\\ {}".format(company["place"])
        if company.get("end", False):
            latex += " \\ \\faCalendar\\ {} - {}".format(
                company["begin"], company["end"])
        else:
            latex += " \\ \\faCalendar\\ {}".format(company["begin"])
        if company.get("role", False):
            latex += "\\\\\n\\textit{{{0}}}".format(company["role"])
        if company.get("tasks", False):
            latex += "\\\\\n"
            for task in company["tasks"]:
                latex += task
                if task != company["tasks"][-1]:
                    latex += ", "
        latex += "\n"
latex += "\n}\n"
latex += "\\end{document}"

with open("cv.tex", 'w') as tex:
    tex.write(latex)

# use lualatex for generating pdf
os.system("lualatex cv.tex")
