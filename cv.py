import json
import os

# read cv data in
with open("cv.json", 'r') as jsonData:
    data = json.load(jsonData)
print(type(data["zip"]))
print(type(data["city"]))
# write data to tex file
latex = "\\documentclass[11pt]{article}\n"
print(type(latex))
latex += "\\usepackage[ngerman]{babel}\n"
latex += "\\usepackage{fontawesome}\n"
latex += "\\usepackage{hyperref}\n"
latex += "\\usepackage{multicol}\n"
latex += "\\begin{document}\n"
# turn off page numbering
latex += "\\pagenumbering{gobble}\n"
# general information
latex += "\\begin{center}\n"
latex += "{{\\Huge\\scshape{{{0}}}}}\\\\\n".format(data["name"])
latex += "{\\sffamily\\large{%\n"
latex += "\\faHome\\ {0}, {1} {2}\\\\\n".format(data["street"],
                                                data["zip"], data["city"])
latex += "\\faEnvelope\\ \\href{{mailto:{0}}}{{{0}}}\n".format(
    data["mail"])
latex += "\\faPhone\\ {0}\n".format(data["phone"])
latex += "\\faLink\\ \\href{{{0}}}{{{0}}}\n".format(data["homepage"])
latex += "}}\n"
latex += "\\end{center}\n"
# education
latex += "\\section*{\\faGraduationCap\\ Bildung}\n"
for institute in data["education"]:
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
    latex += "\n\\subsection*{\\faCode\\ Computerprachen}\n"
    for item in data["coding"]:
        latex += item
        if item != data["coding"][-1]:
            latex += ", "
    # software skills
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
