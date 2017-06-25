#!/usr/bin/env python3
import json
import os
import sys

# read cv data in
with open(sys.argv[1], 'r') as jsonData:
    data = json.load(jsonData)

if sys.argv[-1].lower() == "pdf":
    # write data to tex file
    latex = "\\documentclass[11pt]{article}\n"
    latex += "\\usepackage[ngerman, english]{babel}\n"
    latex += "\\usepackage{fontawesome}\n"
    # set main font type
    latex += "\\setmainfont{SOURCE SANS PRO}\n"
    latex += "\\usepackage{hyperref}\n"
    latex += ("\\usepackage[a4paper, top=0.5cm, bottom=1cm, left=1cm, "
              "right=1cm]{geometry}\n")
    latex += "\\usepackage{titlesec}\n"
    latex += "\\titleformat{\\section}{\\Large\\scshape\\raggedright}{}{0ex}{}"
    latex += "[\\titlerule]\n"
    latex += "\\titlespacing*{\\section}{0em}{2ex}{2ex}\n"
    latex += "\\titleformat{\\subsection}{\\large\\bfseries\\raggedright}{}"
    latex += "{0ex}{}\n"
    latex += "\\titlespacing*{\\subsection}{0ex}{2ex}{0ex}\n"
    latex += "\\begin{document}%\n"
    if data["language"] == "german":
        latex += "\selectlanguage{ngerman}\n"
    # turn off page numbering
    latex += "\\pagenumbering{gobble}%\n"
    # general information
    latex += "\\noindent\n"
    latex += "\parbox[t][.99\\textheight]{.25\\textwidth}{%\n"
    latex += "\\vspace{0pt}%\n"
    # picture
    if data.get("picture", False):
        latex += "\\includegraphics[width=\\linewidth]{{{0}}}\n".format(
            data["picture"])
    latex += "\\begin{tabbing}%\n"
    latex += "\\textbf{{\\LARGE\\scshape{{{0}}}}}".format(data["name"])
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
        latex += "\\\\\n\\faLink\\ \\href{{{0}}}{{{0}}}\n".format(
            data["homepage"])
    latex += "\\end{tabbing}%\n"
    # personal data
    if (data.get("nationality", False)
            or data.get("birthday", False)
            or data.get("birthplace", False)):
        if data["language"] == "german":
            latex += "\\subsection*{\\faInfo\\ Persönliche Daten}\n"
        else:
            latex += "\\subsection*{\\faInfo\\ Personal Data}\n"
    if data.get("nationality", False):
        if data["language"] == "german":
            latex += "Staatsangehörigkeit:\\\\ {\\textit{"
        else:
            latex += "Nationality:\\\\ {\\textit{"
        counter = 0
        for nation in data["nationality"]:
            counter += 1
            latex += nation
            if counter != len(data["nationality"]):
                latex += ", "
        latex += "}}\\\\\n"
    if data.get("birthday", False):
        if data["language"] == "german":
            latex += "Geburtsdatum:\\\\{{\\textit{{{}}}}}\\\\\n".format(
                data["birthday"])
        else:
            latex += "Date of Birth:\\\\{{\\textit{{{}}}}}\\\\\n".format(
                data["birthday"])
    if data.get("birthplace", False):
        if data["language"] == "german":
            latex += "Geburtsort:\\\\{{\\textit{{{}}}}}\n".format(
                data["birthplace"])
        else:
            latex += "Place of Birth:\\\\{{\\textit{{{}}}}}\n".format(
                data["birthplace"])
    # languages
    if data.get("languages", False):
        if data["language"] == "german":
            latex += "\\subsection*{\\faGlobe\\ Sprachen}\n"
        else:
            latex += "\\subsection*{\\faGlobe\\ Languages}\n"
        latex += "\\begin{flushleft}\n"
        for language in data["languages"]:
            latex += language
            if language != data["languages"][-1]:
                latex += ", "
        latex += "\n\\end{flushleft}"
    # coding skills
    if data.get("coding", False):
        if data["language"] == "german":
            latex += "\n\\subsection*{\\faCode\\ Computerprachen}\n"
        else:
            latex += "\n\\subsection*{\\faCode\\ Coding}\n"
        latex += "\\begin{flushleft}\n"
        for item in data["coding"]:
            latex += item
            if item != data["coding"][-1]:
                latex += ", "
        latex += "\n\\end{flushleft}"
    # software skills
    if data.get("software", False):
        latex += "\n\\subsection*{\\faDesktop\\ Software}\n"
        latex += "\\begin{flushleft}\n"
        for item in data["software"]:
            latex += item
            if item != data["software"][-1]:
                latex += ", "
        latex += "\n\\end{flushleft}"
    latex += "\n\\vfill\n"
    # place and date for signature
    latex += "{}, \\today\\\\\n\\\\\n\\\\%\n}}%\n".format(data["city"])
    latex += "\\hfill\\vline\\hfill%\n"
    latex += "\parbox[t][.99\\textheight]{.7\\textwidth}{%\n"
    latex += "\\vspace{0pt}%\n"
    # education
    if data.get("education", False):
        if data["language"] == "german":
            latex += "\\section*{\\faGraduationCap\\ Bildung}\n"
        else:
            latex += "\\section*{\\faGraduationCap\\ Education}\n"
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
                if data["language"] == "german":
                    latex += "\\\\\n\\underline{Abschluss}: "
                else:
                    latex += "\\\\\n\\underline{Degree}: "
                latex += institute["graduation"]
            if institute.get("ba_topic", False):
                if data["language"] == "german":
                    latex += "\\\\\n\\underline{Thema der Bachelorarbeit}: "
                else:
                    latex += "\\\\\n\\underline{Topic of Bachelorthesis}: "
                latex += institute["ba_topic"]
            if institute.get("focus", False):
                if data["language"] == "german":
                    if institute.get("focus", False):
                        latex += "\\\\\n\\underline{Schwerpunkt}: "
                    else:
                        latex += "\\\\\n\\underline{Schwerpunkte}: "
                else:
                    latex += "\\\\\n\\underline{Focus}: "
                for item in institute["focus"]:
                    latex += item
                    if item != institute["focus"][-1]:
                        latex += ", "
    # work experience
    if data.get("work", False):
        if data["language"] == "german":
            latex += "\\section*{\\faGears\\ Arbeitserfahrung}\n"
        else:
            latex += "\\section*{\\faGears\\ Work Experience}\n"
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
                        latex += "; "
            latex += "\n"
    # civil service
    if data.get("civil_service", False):
        if data["language"] == "german":
            latex += "\\section*{\\faGroup\\ Zivildienst}\n"
        else:
            latex += "\\section*{\\faGroup\\ Civil Service}\n"
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
                        latex += "; "
            latex += "\n"
    latex += "\n}\n"
    latex += "\\end{document}"

    with open("cv.tex", 'w') as tex:
        tex.write(latex)

    # use lualatex for generating pdf
    os.system("lualatex cv.tex")


elif sys.argv[-1].lower() == "html":
    html = "<!DOCTYPE html><html>"
    # title of page
    html += "<title>Lebenslauf</title>"
    # use unicode
    html += "<meta charset='UTF-8'>"
    # load css
    html += ("<meta name='viewport' content='width=device-width, "
             "initial-scale=1'><link rel='stylesheet' href="
             "'https://www.w3schools.com/w3css/3/w3.css'>"
             "<link rel='stylesheet' href="
             "'https://fonts.googleapis.com/css?family=Roboto'>"
             "<link rel='stylesheet' href='https://cdnjs.cloudflare.com"
             "/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>")
    html += "<style>"
    html += "html,body,h1,h2,h3,h4,h5,h6 {font-family: 'Roboto', sans-serif}"
    html += "</style>"
    html += "<body class='w3-light-grey'>"
    html += "<div class='w3-content w3-margin-top' style='max-width:1400px;'>"
    html += "<div class='w3-row-padding'>"
    html += "<div class='w3-third'>"
    html += "<div class='w3-white w3-text-grey w3-card-4'>"
    # foto
    html += "<div class='w3-display-container'>"
    html += "<img src='{}' style='width:100%' alt='Avatar'>".format(
        data["picture"])
    html += "<div class='w3-display-bottomleft w3-container w3-text-white'>"
    html += "<h2>{0}</h2>".format(data["name"])
    html += "</div></div>"
    # general information
    html += "<div class='w3-container'>"
    # job title
    html += "<p><i class='fa fa-briefcase fa-fw w3-margin-right w3-large "
    html += "w3-text-teal'></i>{0}</p>".format(data["job"])
    # address
    html += "<p><i class='fa fa-home fa-fw w3-margin-right w3-large "
    if data.get("country", False):
        html += "w3-text-teal'></i>{0}, {1}</p>".format(data["city"],
                                                        data["country"])
    else:
        html += "w3-text-teal'></i>{0}</p>".format(data["city"])
    # email
    html += "<p><i class='fa fa-envelope fa-fw w3-margin-right w3-large "
    html += "w3-text-teal'></i>"
    html += "<a href='mailto:{0}' style='text-decoration: none'>{0}".format(
        data["mail"])
    html += "</a></p>"
    # homepage
    if data.get("homepage", False):
        html += "<p><i class='fa fa-link fa-fw w3-margin-right w3-large "
        html += "w3-text-teal'></i>"
        html += "<a href='{0}' style='text-decoration: none'>{0}".format(
            data["homepage"])
        html += "</a></p>"
    # languages
    html += "<hr><p class='w3-large'><b>"
    html += "<i class='fa fa-globe fa-fw w3-margin-right w3-text-teal'>"
    html += "</i>Sprachen</b></p>"
    for language in data["languages"]:
        html += "<div class='w3-container w3-center w3-round-xlarge w3-teal' "
        html += "style='display: inline-block; margin: 3px;'>"
        html += "{0}</div>".format(language)
    # coding skills
    html += "<hr><p class='w3-large'><b>"
    html += "<i class='fa fa-code fa-fw w3-margin-right w3-text-teal'>"
    html += "</i>Computersprachen</b></p>"
    for language in data["coding"]:
        html += "<div class='w3-container w3-center w3-round-xlarge w3-teal' "
        html += "style='display: inline-block; margin: 3px;'>"
        html += "{0}</div>".format(language)
    # software skills
    html += "<hr><p class='w3-large'><b>"
    html += "<i class='fa fa-desktop fa-fw w3-margin-right w3-text-teal'>"
    html += "</i>Software</b></p>"
    for item in data["software"]:
        html += "<div class='w3-container w3-center w3-round-xlarge w3-teal' "
        html += "style='display: inline-block; margin: 3px;'>"
        html += "{0}</div>".format(item)
    html += "</div><br></div></div>"

    html += "<div class='w3-twothird'>"
    # education
    html += "<div class='w3-container w3-card-2 w3-white w3-margin-bottom'>"
    html += "<h2 class='w3-text-grey w3-padding-16'>"
    html += "<i class='fa fa-graduation-cap fa-fw w3-margin-right w3-xxlarge "
    html += "w3-text-teal'></i>Bildung</h2>"
    for institute in data["education"]:
        html += "<div class='w3-container'><h5 class='w3-opacity'><b>"
        html += institute["institution"]
        html += "</b></h5><h6 class='w3-text-teal'>"
        html += "<i class='fa fa-map-marker  fa-fw w3-margin-right'></i>"
        html += institute["place"]
        html += "</h6><h6 class='w3-text-teal'>"
        html += "<i class='fa fa-calendar fa-fw w3-margin-right'></i>"
        html += institute["begin"]
        if institute.get("end", False):
            html += ' - '
            if institute["end"].lower() == "heute":
                html += "<span class='w3-tag w3-teal w3-round'>heute</span>"
            else:
                html += institute["end"]
        if institute.get("duration", False):
            html += " ({})".format(institute["duration"])
        html += "</h6><p><i>"
        html += institute["role"]
        html += "</i>"
        if institute.get("graduation", False):
            html += "<br>Abschluss: {}".format(institute["graduation"])
        if institute.get("ba_topic", False):
            html += "<br>Thema der Bachelorarbeit: {}".format(
                institute["ba_topic"])
        if institute.get("focus", False):
            if len(institute["focus"]) == 1:
                html += "<br>Schwerpunkt: "
            else:
                html += "<br>Schwerpunkte: "
            for item in institute["focus"]:
                html += item
                if item != institute["focus"][-1]:
                    html += ", "
        if institute != data["education"][-1]:
            html += "</p><hr></div>"
        else:
            html += "</p></div>"
    html += "</div>"
    # work experience
    html += "<div class='w3-container w3-card-2 w3-white w3-margin-bottom'>"
    html += "<h2 class='w3-text-grey w3-padding-16'>"
    html += "<i class='fa fa-gears fa-fw w3-margin-right w3-xxlarge "
    html += " w3-text-teal'></i>Arbeitserfahrung</h2>"
    for company in data["work"]:
        html += "<div class='w3-container'><h5 class='w3-opacity'><b>"
        html += company["company"]
        html += "</b></h5><h6 class='w3-text-teal'>"
        html += "<i class='fa fa-map-marker  fa-fw w3-margin-right'></i>"
        html += company["place"]
        html += "</h6><h6 class='w3-text-teal'>"
        html += "<i class='fa fa-calendar fa-fw w3-margin-right'></i>"
        html += company["begin"]
        if company.get("end", False):
            html += ' - '
            if company["end"].lower() == "heute":
                html += "<span class='w3-tag w3-teal w3-round'>heute</span>"
            else:
                html += company["end"]
        if company.get("duration", False):
            html += " ({})".format(company["duration"])
        html += "</h6><p><i>"
        html += company["role"]
        html += "</i><br>"
        for task in company["tasks"]:
            html += task
            if task != company["tasks"][-1]:
                html += "; "
        if company != data["work"][-1]:
            html += "</p><hr></div>"
        else:
            html += "</p></div>"
    html += "</div>"
    # civil service
    if data.get("civil_service", False):
        html += "<div class='w3-container w3-card-2 w3-white'>"
        html += "<h2 class='w3-text-grey w3-padding-16'>"
        html += "<i class='fa fa-users fa-fw w3-margin-right w3-xxlarge "
        html += "w3-text-teal'></i>Zivildienst</h2>"
        for company in data["civil_service"]:
            html += "<div class='w3-container'><h5 class='w3-opacity'><b>"
            html += company["company"]
            html += "</b></h5><h6 class='w3-text-teal'>"
            html += "<i class='fa fa-map-marker  fa-fw w3-margin-right'></i>"
            html += company["place"]
            html += "</h6><h6 class='w3-text-teal'>"
            html += "<i class='fa fa-calendar fa-fw w3-margin-right'></i>"
            html += company["begin"]
            if company.get("end", False):
                html += ' - '
                if company["end"].lower() == "heute":
                    html += "<span class='w3-tag w3-teal w3-round'>"
                    html += "heute</span>"
                else:
                    html += company["end"]
            if company.get("duration", False):
                html += " ({})".format(company["duration"])
            html += "</h6><p><i>"
            html += company["role"]
            html += "</i><br>"
            for task in company["tasks"]:
                html += task
                if task != company["tasks"][-1]:
                    html += "; "
            html += "</p></div>"
    html += "</div></div></div></div>"
    # footer
    html += "<footer class='w3-container w3-teal w3-center w3-margin-top'>"
    if data.get("xing", False):
        html += "<a href='{}' target='_blank'>".format(data["xing"])
        html += "<i class='fa fa-xing w3-hover-opacity'></i></a> "
    if data.get("linkedin", False):
        html += "<a href='{}' target='_blank'>".format(data["linkedin"])
        html += "<i class='fa fa-linkedin w3-hover-opacity'></i></a> "
    if data.get("github", False):
        html += "<a href='{}' target='_blank'>".format("github")
        html += "<i class='fa fa-github w3-hover-opacity'></i></a> "
    html += "<p>Erstellt mit "
    html += "<a href='https://github.com/Schildkroete23/jsonCV' "
    html += "target='_blank'>jsonCV</a>"
    html += " und ausgerüstet mit <a href='https://www.w3schools.com/w3css/"
    html += "default.asp' target='_blank'>w3.css</a>.</p></footer>"
    html += "</body></html>"
    with open("cv.html", 'w') as cvhtml:
        cvhtml.write(html)
else:
    print("Unknown option.")
