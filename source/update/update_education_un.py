import requests

from os import getenv

def clean_lines( csv ):
    lines = list(csv.iter_lines())
    lines.pop(0)
    lines[0] = ( ','.join(['', 'country', 'year', 'series', 'value', 'footnote', 'source' ]) ).encode()
    lines_w_newline = []
    for cur_line in lines:
        lines_w_newline.append(cur_line + ("\n").encode() )

    return lines_w_newline

print ("Updating education repos.")
dls = "https://data.un.org/_Docs/SYB/CSV/SYB62_309_201906_Education.csv" 
csv = requests.get(dls)

repo_dir = getenv('DABBOTTCOVID')
f = open(repo_dir+"/data/EducationData.csv", 'wb')
clean_csv = clean_lines(csv)
f.writelines(clean_csv)
f.close()
print ("Done.")
