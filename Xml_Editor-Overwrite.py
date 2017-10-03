__author__ = 'trogers&jkenyon'

from lxml import etree
import os
from sys import exit
import sys
# import csv

file_path = r"C:/Users/Taylor/Documents/!USGS/Metadata Work/Data on influence of atmospheric rivers on veg - Copy/"

file_count = 0 #this is so we can keep track of how many files it goes through. Print at the end so we know if it missed any

print "Starting program..."

def file_read():
    file_list = []
    for root, dirs, files in os.walk(file_path): #this looks at every item at the filepath above and does the following:
        for filename in files: #this looks at each files name for each item
            md_file_number = 0 #this creates a variable that represents how many files the program found that match the parameters below. Obviously, we start at zero
            if filename.endswith(".xml") and not filename.endswith(".aux.xml"): #if any file name ends with .xml, but not .aux.xml then...
                md_file_number += 1 #This SHOULD add 1 to the number of metadata files that the program has found,
                print "Found a file that fits your parameters! The number of files that meet your requirements: "+str(md_file_number)
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file)
            else:
                print "This file does not meet your requirements." #NOTE: this never shows up. It must not work properly.
    grab_title(file_list)

#tree = []

def grab_title(md_files): #file_list was just renamed to md_files.

    for source in md_files:
        tree = etree.parse(source) #reading the file. so "tree" is the whole doc.  Similar to "root = xml.etree.ElementTree.fromstring"
        #root = tree.getroot()  #This gets us the very first tag in the "tree", or the entire file. We named it root
        root = tree.find("//distinfo")
        #distinfo = etree.SubElement(root, "distinfo") #This creates (in python memory, not the doc) a nested tag called "distinfo" inside the root tag (metadata)
        #distrib = etree.SubElement(distinfo, "distrib")
#so, I noticed a problem where the program is creating a new <distinfo> section, like it is made to do, but there already is one.
#This means I was going about it all wrong and that I should be overwriting existing tags, not creating new tags.
#I could also do this by deleting <distinfo> and all children first, THEN writing all the new stuff.
        #cntinfo = etree.SubElement(distrib, "cntinfo")
        #cntorgp = etree.SubElement(cntinfo, "cntorgp")
        #cntorg = etree.SubElement(cntorgp, "cntorg")
        cntorg.text = "U.S. Geological Survey - ScienceBase"
        cntper.remove #this should remove the tag <cntper> because it doesn't apply to USGS
        cntpos.remove
        #cntaddr = etree.SubElement(cntinfo, "cntaddr")
        #addrtype = etree.SubElement(cntinfo, "addrtype")
        addrtype.text = "mailing"
        #address = etree.SubElement(cntaddr, "address")
        address.text = "Denver Federal Center, Building 810, Mail Stop 302"
        #city = etree.SubElement(cntaddr, "city")
        city.text = "Denver"
        #state = etree.SubElement(cntaddr, "state")
        state.text = "CO"
        #postal = etree.SubElement(cntaddr, "postal")
        postal.text = "80225"
        #cntvoice = etree.SubElement(cntinfo, "cntvoice")
        cntvoice.text = "1-888-275-8747"
        #cntemail = etree.SubElement(cntinfo, "cntemail")
        cntemail.text = "sciencebase@usgs.gov"
        #distliab = etree.SubElement(distinfo, "distliab")
        distliab.text = "Unless otherwise stated, all data, metadata and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data on any other system or for general or scientific purposes, nor shall the act of distribution constitute any such warranty."

        root.insert(5, distinfo) #this inserts <distinfo> as the 6th child of "root"


        print etree.tostring(tree, pretty_print=True) #.tostring makes the memory, prints it legibly(pretty) to the console
        print "Found "+str(source)+" that matches your file type.\n"
        print """
            Does that look right? \n
            Type \'y\', then return (enter) if it looks right and you want to continue and permantently write the section to the file. \n
            Type \'n\', then return (enter) to stop the program and not write anything to the file.\n
            Type anything else and press return (enter) to skip writing to the current file, but continue to the next file.
            """
        print "Files written:"+str(file_count)
        #^why doesn't this pull from the global variable?

        choice = raw_input("> ")
        command(choice,tree,source) #this is how you pass tree and source to the next function (but must be in order, if mixed you just renamed them to the other's name)

def command(choice,tree,source): #must also pass here. Obviously.
    #file_count = 0 #this is so we can keep track of how many files it goes through. Print at the end so we know if it missed any
    #^this can't be created here because it needs to be read and printed in the function before it.
    if choice == "y":
        tree.write(source) #This permanently writes the output to the file
        #^why doesn't this pull from the global variable?
        global file_count
        file_count += 1 #this adds each file you write to together, so you know the total
    elif "n" in choice:
        sys.exit()
        #end=True
        #end_all(end)
    else:
        print "Onward!\n\n\n------------------\n\n\n"
        file_count += 0
#def end_all(end):
#    sys.exit()

#        file_count += 1
#        tree.write(source) #This permanently writes the output to the file. IF you have a TON of files, and don't want to check each one...
#Then do this: check one, break the program, and come back here and un-comment the "write" command and the "file_count" command above
#and comment out the 'command' function, the "choice" variable, and the two "print" commands that ask for input above.
#Then it will go through and do all of the files without your input.





file_read() #This starts the entire program.
