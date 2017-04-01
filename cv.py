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
latex += "\\end{document}"

with open("cv.tex", 'w') as tex:
    tex.write(latex)

# use lualatex for generating pdf
os.system("lualatex cv.tex")
