import json

with open('test/eu-members.json') as f:
    d = json.load(f)

out = open('test/eu-members.ttl', 'w')

for x in d:
    s = x.get('c')
    if s.startswith("http"):
        s = "<" + s + ">"
    else:
        s = "\"" + s + "\""
    p = x.get('p')
    if p.startswith("http"):
        p = "<" + p + ">"
    else:
        p = "\"" + p + "\""
    o = x.get('o')
    if o.startswith("http"):
        o = "<" + o + ">"
    else:
        o = "\"" + o + "\""

    out.write(s + " " + p + " " + o + " .\n")
