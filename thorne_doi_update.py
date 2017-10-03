__author__ = 'jkenyon'

from lxml import etree
import os
# import csv

file_path = r"C:/Users/jkenyon/Desktop/Projects/CSCs/NW Projects/FY12/Takekawa_Thorne/data/Northwest/elevation_metadata/"


def file_read():
    file_list = []
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if filename.endswith("fgdc.xml") and not filename.endswith(".aux.xml"):
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file)
    grab_title(file_list)


def grab_title(md_files):
    file_count = 0
    for source in md_files:
        tree = etree.parse(source)
        root = tree.find("//idinfo//citation//citeinfo")
        othercit = etree.SubElement(root, "othercit")
        othercit.text = "doi:10.5066/F7SJ1HNC"
        onlink = etree.SubElement(root, "onlink")
        onlink.text = "http://dx.doi.org/10.5066/F7SJ1HNC"

        home = tree.getroot()
        distinfo = etree.SubElement(home, "distinfo")
        distrib = etree.SubElement(distinfo, "distrib")
        cntinfo = etree.SubElement(distrib, "cntinfo")
        cntorgp = etree.SubElement(cntinfo, "cntorgp")
        cntorg = etree.SubElement(cntorgp, "cntorg")
        cntorg.text = "U.S. Geological Survey - ScienceBase"
        cntaddr = etree.SubElement(cntinfo, "cntaddr")
        addrtype = etree.SubElement(cntinfo, "addrtype")
        addrtype.text = "mailing"
        address = etree.SubElement(cntaddr, "address")
        address.text = "Denver Federal Center, Building 810, Mail Stop 302"
        city = etree.SubElement(cntaddr, "city")
        city.text = "Denver"
        state = etree.SubElement(cntaddr, "state")
        state.text = "CO"
        postal = etree.SubElement(cntaddr, "postal")
        postal.text = "80225"
        cntvoice = etree.SubElement(cntinfo, "cntvoice")
        cntvoice.text = "1-888-275-8747"
        cntemail = etree.SubElement(cntinfo, "cntemail")
        cntemail.text = "sciencebase@usgs.gov"
        distliab = etree.SubElement(distinfo, "distliab")
        distliab.text = "Contact ScienceBase for details"
        stdorder = etree.SubElement(distinfo, "stdorder")
        digform = etree.SubElement(stdorder, "digform")
        digtinfo = etree.SubElement(digform, "digtinfo")
        formname = etree.SubElement(digtinfo, "formname")
        formname.text = "Access point for data"
        digtopt = etree.SubElement(digform, "digtopt")
        onlinopt = etree.SubElement(digtopt, "onlinopt")
        computer = etree.SubElement(onlinopt, "computer")
        networka = etree.SubElement(computer, "networka")
        networkr = etree.SubElement(networka, "networkr")
        networkr.text = "http://dx.doi.org/10.5066/F7SJ1HNC"
        fees = etree.SubElement(stdorder, "fees")
        fees.text = "None"

        root.insert(4, othercit)
        root.insert(5, onlink)
        home.insert(5, distinfo)

        print etree.tostring(tree, pretty_print=True)
#        tree.write(source)

        file_count += 1

    print file_count

file_read()