import requests

def clean_lines( csv ):
    lines = list(csv.iter_lines())
    lines.pop(0)
    lines[0] = ( ','.join(['', 'country', 'year', 'series', 'value', 'footnote', 'source' ]) ).encode()
    lines_w_newline = []
    for cur_line in lines:
        lines_w_newline.append(cur_line + ("\n").encode() )

    return lines_w_newline

dls = "https://data.un.org/_Docs/SYB/CSV/SYB62_230_201904_GDP%20and%20GDP%20Per%20Capita.csv" 
csv = requests.get(dls)

f = open("../data/GDPData.csv", 'wb')
clean_csv = clean_lines(csv)
f.writelines(clean_csv)
f.close()

dls = "https://data.un.org/_Docs/SYB/CSV/SYB62_153_201906_Gross%20Value%20Added%20by%20Economic%20Activity.csv" 
csv = requests.get(dls)

f = open("../data/GVAData.csv", 'wb')
clean_csv = clean_lines(csv)
f.writelines(clean_csv)
f.close()



