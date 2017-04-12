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
latex += "\\usepackage{hyperref}\n"
latex += "\\usepackage{multicol}\n"
latex += "\\usepackage{titlesec}\n"
latex += ("\\usepackage[a4paper, top=1.5cm, bottom=2cm, left=2cm, right=2cm]"
          "{geometry}\n")
latex += "\\titleformat{\\section}{\\Large\\scshape\\raggedright}{}{0em}{}"
latex += "[\\titlerule]\n"
latex += "\\titlespacing*{\\section}{0em}{1em}{1ex}\n"
latex += "\\titleformat{\\subsection}{\\large\\bfseries\\raggedright}{}"
latex += "{0em}{}\n"
latex += "\\titlespacing*{\\subsection}{0em}{1ex}{0em}\n"
latex += "\\setlength{\\multicolsep}{0em}\n"
latex += "\\begin{document}\n"
# turn off page numbering
latex += "\\pagenumbering{gobble}\n"
# general information
if data.get("picture", False):
    latex += "\\noindent\\begin{minipage}{0.85\\textwidth}\\raggedright%\n"
    latex += "{{\\Huge\\scshape{{{0}}}}}\\\\\n".format(data["name"])
    latex += "{\\sffamily\\large{%\n"
    latex += "\\faHome\\ {0}, {1} {2}\\\\\n".format(data["street"],
                                                    data["zip"], data["city"])
    latex += "\\faEnvelope\\ \\href{{mailto:{0}}}{{{0}}}\\\\\n".format(
        data["mail"])
    latex += "\\faPhone\\ {0}\\\\\n".format(data["phone"])
    if data.get("homepage", False):
        latex += "\\faLink\\ \\href{{{0}}}{{{0}}}\n".format(data["homepage"])
    latex += "}}\n"
    latex += "\end{minipage}\n"
    latex += "\\noindent\\begin{minipage}{0.15\\textwidth}\n"
    latex += "\\includegraphics[width=0.9\\textwidth]{{{0}}}\n".format(
        data["picture"])
    latex += "\end{minipage}%\n"
else:
    latex += "\\begin{center}\n"
    latex += "{{\\Huge\\scshape{{{0}}}}}\\\\\n".format(data["name"])
    latex += "{\\sffamily\\large{%\n"
    latex += "\\faHome\\ {0}, {1} {2}\\\\\n".format(data["street"],
                                                    data["zip"], data["city"])
    latex += "\\faEnvelope\\ \\href{{mailto:{0}}}{{{0}}}\n".format(
        data["mail"])
    latex += "\\faPhone\\ {0}\n".format(data["phone"])
    if data.get("homepage", False):
        latex += "\\faLink\\ \\href{{{0}}}{{{0}}}\n".format(data["homepage"])
    latex += "}}\n"
    latex += "\\end{center}\n"
# education
latex += "\\section*{\\faGraduationCap\\ Bildung}\n"
for i in range(len(data["education"])):
    institute = data["education"][i]
    latex += "\\subsection*{{{0}}}\n".format(institute["institution"])
    latex += "\\faMapMarker\\ {}".format(institute["place"])
    if institute.get("end", False):
        latex += " \\ \\faCalendar\\ {} - {}\\\\\n".format(
            institute["begin"], institute["end"])
    else:
        latex += " \\ \\faCalendar\\ {}\\\\\n".format(institute["begin"])
    latex += "\\textit{{{0}}}".format(institute["role"])
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
latex += "\\section*{\\faBriefcase\\ Arbeitserfahrung}\n"
for company in data["work"]:
    latex += "\\subsection*{{{0}}}\n".format(company["company"])
    latex += "\\faMapMarker\\ {}".format(company["place"])
    if company.get("end", False):
        latex += " \\ \\faCalendar\\ {} - {}\\\\\n".format(
            company["begin"], company["end"])
    else:
        latex += " \\ \\faCalendar\\ {}\\\\\n".format(company["begin"])
    latex += "\\textit{{{0}}}\\\\\n".format(company["role"])
    for task in company["tasks"]:
        latex += task
        if task != company["tasks"][-1]:
            latex += ", "
    latex += "\n"
# skills
latex += "\\section*{\\faCogs\\ Kenntnisse \\& Fähigkeiten}\n"
latex += "\\begin{multicols}{2}\n"
latex += "\\raggedright\n"
# languages
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
latex += "\n\\end{multicols}\n"
latex += "\\end{document}"

with open("cv.tex", 'w') as tex:
    tex.write(latex)

# use lualatex for generating pdf
os.system("lualatex cv.tex")
