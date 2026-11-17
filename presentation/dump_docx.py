import docx, sys
from docx.document import Document as D
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
def walk(path):
    d = docx.Document(path)
    print("=====", path, "sections:", len(d.sections))
    for el in d.element.body.iterchildren():
        if el.tag == qn('w:p'):
            p = Paragraph(el, d)
            t = p.text.strip()
            if t: print(f"[P:{p.style.name}] {t}")
        elif el.tag == qn('w:tbl'):
            tb = Table(el, d)
            print(f"[TABLE {len(tb.rows)}x{len(tb.columns)}]")
            for r in tb.rows:
                cells=[]
                prev=None
                for c in r.cells:
                    if c._tc is prev: continue
                    prev=c._tc
                    cells.append(c.text.strip().replace("\n"," / "))
                print("   | " + " | ".join(cells))
walk(sys.argv[1])
