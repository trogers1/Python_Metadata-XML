__author__ = 'jkenyon'

from lxml import etree
import os
# import csv

file_path = r"C:/Users/jkenyon/Desktop/Projects/CSCs/NW Projects/FY12/Takekawa_Thorne/data/Northwest/elevation_metadata/"


def file_read(): #This function has the program read the file at the path above,
    file_list = [] #creates an emply dictionary list
    for root, dirs, files in os.walk(file_path): #and walk through the contents of that file
        for filename in files:
            if filename.endswith("fgdc.xml") and not filename.endswith(".aux.xml"):  #if the file ends with fgdc.xml, not .aux.xml, it is made a variable
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file) #And the above dictionary list is appended with that file that was found
    grab_title(file_list) #and then the next function is called using the files that this function found and read


def grab_title(md_files): #file_list was just renamed to md_files.
    file_count = 0 #this is so we can keep track of how many files it goes through. Print at the end so we know if it missed any
    for source in md_files:
        tree = etree.parse(source) #reading the file. so "tree is the whole doc". Similar to "root = xml.etree.ElementTree.fromstring"
        root = tree.find("//idinfo//citation//citeinfo") #This is XPath, and "//" just means that a tag is somewhere nested inside another
        othercit = etree.SubElement(root, "othercit") #This creates (in python memory, not the doc) a nested tag called "othercite" inside citeinfo
        othercit.text = "doi:10.5066/F7SJ1HNC" #The text to be written inside <othercite>
        onlink = etree.SubElement(root, "onlink") #same as above
        onlink.text = "http://dx.doi.org/10.5066/F7SJ1HNC"

        home = tree.getroot() #This gets us the very first tag in the "tree", or the entire file. We named it home
        distinfo = etree.SubElement(home, "distinfo") #We went from "home" because distinfo is a main tag under the <metadata> root tag
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

        root.insert(4, othercit) #The number says that it should be the 5th child of "root" which is <citeinfo>
        root.insert(5, onlink) #this inserts <onlink> as the 6th child of "root", which is <citeinfo>
        home.insert(5, distinfo)

        print etree.tostring(tree, pretty_print=True) #.tostring makes the memory, prints it legibly(pretty) to the console
        print "Does that look right? Type 'y' if it does and you want to continue. Type 'n' to stop the program.
        print "Type anything else if it's not, but you want to continue anyway."

        choice = raw_input("> ")

        def command(choice):
            if choice="y":
                tree.write(source) #This permanently writes the output to the file
                file_count += 1 #this adds each file you write to together, so you know the total
            elif choice="n":
                break
            else:
                continue

#        file_count += 1
#        tree.write(source) #This permanently writes the output to the file. IF you have a TON of files, and don't want to check each one...
#Then do this: check one, break the program, and come back here and un-comment the "write" command and the "file_count" command above
#and comment out the 'command' function, the "choice" variable, and the two "print" commands that ask for input above.
#Then it will go through and do all of the files without your input.



    print file_count

file_read() #This starts the entire program.
