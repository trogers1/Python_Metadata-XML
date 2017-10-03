__author__ = 'jkenyon'

import json
from lxml import etree

file_path = r"C:/Users/jkenyon/Desktop/Projects/CSCs/NW Projects/FY12/Takekawa_Thorne/data/Northwest/Model/Nisqually/"
index_path = r"C:/Users/jkenyon/Desktop/Projects/CSCs/NW Projects/FY12/Nolin/Data/finished/sandbox/"
index = {}

def file_read():
    file_list = []
    for root, dirs, files in os.walk(file_path):
        for filename in files:
#           if filename.endswith(".xml") and not filename.endswith(".aux.xml"):
            if filename.endswith(".xml"):
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file)
    grab_title(file_list)

def grab_title(path):
    with open(path, "rb") as indx:
        reader = indx.read()
        indx.close()
    fl = json.loads(reader, encoding="utf-8")

    count = 0
    keys = fl.keys()

    for i in keys:
        if len(fl[i]) < 7:
            continue
        else:
            root = etree.Element("taxonomy")
            keywtax = etree.SubElement(root, "keywtax")
            taxonkt = etree.SubElement(keywtax, "taxonkt")
            taxonkt.text = "Integrated Taxonomic Information System, www.itis.gov"
            taxonkey = etree.SubElement(keywtax, "taxonkey")
            taxonkey.text = "ITIS"
            taxoncl1 = etree.SubElement(root, "taxoncl")
            taxonrn1 = etree.SubElement(taxoncl1, "taxonrn")
            taxonrn1.text = "Kingdom"
            taxonrv1 = etree.SubElement(taxoncl1, "taxonrv")
            taxonrv1.text = fl[i].get("Kingdom")

            taxoncl2 = etree.SubElement(taxoncl1, "taxoncl")
            taxonrn2 = etree.SubElement(taxoncl2, "taxonrn")
            taxonrn2.text = "Phylum"
            taxonrv2 = etree.SubElement(taxoncl2, "taxonrv")
            taxonrv2.text = fl[i].get("Phylum")

            taxoncl3 = etree.SubElement(taxoncl2, "taxoncl")
            taxonrn3 = etree.SubElement(taxoncl3, "taxonrn")
            taxonrn3.text = "Class"
            taxonrv3 = etree.SubElement(taxoncl3, "taxonrv")
            taxonrv3.text = fl[i].get("Class")

            taxoncl4 = etree.SubElement(taxoncl3, "taxoncl")
            taxonrn4 = etree.SubElement(taxoncl4, "taxonrn")
            taxonrn4.text = "Order"
            taxonrv4 = etree.SubElement(taxoncl4, "taxonrv")
            taxonrv4.text = fl[i].get("Order")

            taxoncl5 = etree.SubElement(taxoncl4, "taxoncl")
            taxonrn5 = etree.SubElement(taxoncl5, "taxonrn")
            taxonrn5.text = "Family"
            taxonrv5 = etree.SubElement(taxoncl5, "taxonrv")
            taxonrv5.text = fl[i].get("Family")

            taxoncl6 = etree.SubElement(taxoncl5, "taxoncl")
            taxonrn6 = etree.SubElement(taxoncl6, "taxonrn")
            taxonrn6.text = "Genus"
            taxonrv6 = etree.SubElement(taxoncl6, "taxonrv")
            taxonrv6.text = fl[i].get("Genus")

            taxoncl7 = etree.SubElement(taxoncl6, "taxoncl")
            taxonrn7 = etree.SubElement(taxoncl7, "taxonrn")
            taxonrn7.text = "Species"
            taxonrv7 = etree.SubElement(taxoncl7, "taxonrv")
            taxonrv7.text = fl[i].get("Species")
            cmn_name = etree.SubElement(taxoncl7, "common")
            cmn_name.text = str(i)

            with open(file_path+str(i)+".xml", "wb") as q:
                q.write(etree.tostring(root, pretty_print=True))
            q.close()

            count += 1
    print count

#    with open(file_path+"test.xml", "wb") as f:


grab_index(index_path)
