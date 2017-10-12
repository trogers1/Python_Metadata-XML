__author__ = 'trogers'

import lxml
from lxml import etree
import os
from sys import exit
import sys
# import csv

file_path = r"/Users/taylorrogers/Documents/#Coding/USGS/'Metadata Creation&Editing'/data/'Sea-level rise projections for and observational data of tidal marshes along the California coast copy'/"
# ^Change this path to the path of the file containing the metadata you would like to edit.

file_count = 0 #this is so we can keep track of how many files the program fully runs through. Print at the end so we know if it missed any
global md_file_number
md_file_number = 0 #this creates a variable that represents how many files the program found that match the parameters below. Obviously, we start at zero
total_examined_file_count = 0 #This creates a variable to represent every file we've looked at, whether or not we've changed it.
remaining_files = int(md_file_number) - int(file_count)
done_files = []
print("Starting program...")

def file_read():
    file_list = []
    for root, dirs, files in os.walk(file_path): #this looks at every item at the filepath above and does the following:
        for filename in files: #this looks at each files name for each item
            if filename.endswith(".xml") and not filename.endswith(".aux.xml"): #if any file name ends with .xml, but not .aux.xml then...
                global md_file_number
                md_file_number += 1 #This adds 1 to the number of metadata files that the program has found for each file that it finds that matches the parameters set forth above
                print("Found a file that fits your parameters!")
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file)
    print("The number of files that meet your requirements: "+str(md_file_number))
    grab_title(file_list)

def file_read_remaining(): #this is the function to find all of the files that haven't already been examined.
    file_list = []
    for root, dirs, files in os.walk(file_path): #this looks at every item at the filepath above and does the following:
        for filename in files: #this looks at each files name for each item
#Make sure the parameters here match the ones above in "file_read"
            if filename.endswith(".xml") and not filename.endswith(".aux.xml"):
                global done_files
                metadata_file = os.path.join(root, filename)
                if metadata_file not in done_files: #if any file name ends with .xml, but not .aux.xml then...
                    #metadata_file = os.path.join(root, filename)
                    file_list.append(metadata_file)
                    #print file_list #I used this for troubleshooting.
    write_all(file_list)


def grab_title(md_files): #file_list was just renamed to md_files.

    for source in md_files:
#below is the function that defines exactly what you are doing to each metadata file. Edit the code below to change what exactly you are doing to each file.
#to be able to correctly use the "all" command, copy the code from the line below to the comment just before all the printing and paste it between the comments in the function "write_all".
        parser = etree.XMLParser(remove_blank_text=True) #this takes away all the previous indentation so we can reset it and print it prettily later.
        tree = etree.parse(source, parser) #reading the file. so "tree" is the whole doc.  Similar to "root = xml.etree.ElementTree.fromstring". It also calls the parser variable above.
        root = tree.getroot()  #This gets us the very first tag in the "tree", or the entire file. We named it root
        #Now I will remove the <distinfo> so I can replace it with the correct information:
        for elem in tree.xpath( '//distinfo' ) :
            elem.getparent().remove(elem)
        distinfo = etree.SubElement(root, "distinfo") #This creates (in python memory, not the doc) a nested tag called "distinfo" inside the root tag (metadata)
        distrib = etree.SubElement(distinfo, "distrib")
        cntinfo = etree.SubElement(distrib, "cntinfo")
        cntorgp = etree.SubElement(cntinfo, "cntorgp")
        cntorg = etree.SubElement(cntorgp, "cntorg")
        cntorg.text = "U.S. Geological Survey - ScienceBase"
        cntaddr = etree.SubElement(cntinfo, "cntaddr")
        addrtype = etree.SubElement(cntaddr, "addrtype")
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
        distliab.text = "Unless otherwise stated, all data, metadata and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data on any other system or for general or scientific purposes, nor shall the act of distribution constitute any such warranty."


        root.insert(5, distinfo) #this inserts <distinfo> as the 6th child of "root"

#copy to here and paste into the "write_all" function between the comments in order to be able to use the "all" command

        print(etree.tostring(tree, pretty_print=True)) #.tostring makes the memory, prints it legibly(pretty) to the console
        print("I found this file: "+str(source)+" \n It matches your parameters.\n")
        print("""
            I have printed it above to show you how it would look if you were to write to it using this program.\n
            Does that look right? \n
            Type \'y\', then return (enter) if it looks right and you want to continue and permantently write the section(s) to the file. \n
            Type \'n\', then return (enter) to quite and exit the program. This will not write anything to the file.\n
            Type \'all\', then return (enter) if it looks good to you and you want to write the remaining """+ str(int(md_file_number) - int(total_examined_file_count)) +""" files that have not yet been passed over or written to.\n
            Type \'s\', then press return (enter) to skip writing to the current file, but continue to the next file.
            """)
        print("---------------------------------------------------------------")
        print("Files written so far: "+str(file_count) + " of " + str(md_file_number))
        print("Files examined so far: " + str(total_examined_file_count) + " of " + str(md_file_number))
        print("\n")
        print("You have changed "+str(file_count) +" files out of the "+ str(total_examined_file_count) + " examined so far.")
        print("There are "+ str(md_file_number) + " total files found that match your parameters.")
        print("---------------------------------------------------------------")
        #print done_files I used this for troubleshooting
        choice = input("> ")
        command(choice,tree,source) #this is how you pass tree and source to the next function (but must be in order, if mixed you just renamed them to the other's name)


def command(choice,tree,source): #must also pass here. Obviously.

    if choice == "y":
        tree.write(source, pretty_print=True) #This permanently writes the output to the file in a pretty (read: correctly-indented) way.
        global file_count
        global total_examined_file_count
        file_count += 1 #this adds each file you write together, so you know the total number of files written
        total_examined_file_count += 1 #This adds each file that has been examined by the program together, so you know the total number of files that have been examined at any particular point.
        global done_files
        done_files.append(source)
    elif "n" in choice:
        sys.exit()
    elif choice == "all":
        file_read_remaining()
    elif choice == "s":
        print("Onward!\n\n\n------------------\n\n\n")
        file_count += 0
        total_examined_file_count += 1
        global done_files
        done_files.append(source)
    else:
        print("That's not one of the choices. Please type either \'y,\' \'n,\' \'s,'\' or \'all.\'")
        choice = input("> ")
        command(choice,tree,source)

def write_all(md_files2):
    for source in md_files2:
#Below, replace the existing function code with the code from "grab_title" above.
        parser = etree.XMLParser(remove_blank_text=True) #this takes away all the previous indentation so we can reset it and print it prettily later.
        tree = etree.parse(source, parser) #reading the file. so "tree" is the whole doc.  Similar to "root = xml.etree.ElementTree.fromstring". It also calls the parser variable above.
        root = tree.getroot()  #This gets us the very first tag in the "tree", or the entire file. We named it root
        #Now I will remove the <distinfo> so I can replace it with the correct information:
        for elem in tree.xpath( '//distinfo' ) :
            elem.getparent().remove(elem)
        distinfo = etree.SubElement(root, "distinfo") #This creates (in python memory, not the doc) a nested tag called "distinfo" inside the root tag (metadata)
        distrib = etree.SubElement(distinfo, "distrib")
        cntinfo = etree.SubElement(distrib, "cntinfo")
        cntorgp = etree.SubElement(cntinfo, "cntorgp")
        cntorg = etree.SubElement(cntorgp, "cntorg")
        cntorg.text = "U.S. Geological Survey - ScienceBase"
        cntaddr = etree.SubElement(cntinfo, "cntaddr")
        addrtype = etree.SubElement(cntaddr, "addrtype")
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
        distliab.text = "Unless otherwise stated, all data, metadata and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data on any other system or for general or scientific purposes, nor shall the act of distribution constitute any such warranty."


        root.insert(5, distinfo) #this inserts <distinfo> as the 6th child of "root"
#Above, paste the function code from "grab_title"

        tree.write(source, pretty_print=True) #This permanently writes the output to the file in a pretty (read: correctly-indented) way without asking for input.
        #Therefore, it automatically writes to the files
        global file_count
        global total_examined_file_count
        file_count += 1 #this adds each file you write together, so you know the total number of files written
        total_examined_file_count += 1
        if int(total_examined_file_count) == int(md_file_number):
            closing_message()

def closing_message():
    print("\n \n \n \n ")
    print("That's all the files! Here's what we did:")
    print("---------------------------------------------------------------")
    print("Total number of files written: "+str(file_count) + " of " + str(md_file_number))
    print("Total number of files examined by the program: " + str(total_examined_file_count) + " of " + str(md_file_number))
    print("\n")
    print("We changed "+str(file_count) +" files out of the "+ str(total_examined_file_count) + " that matched the parameters you set forth.")
    print("There are "+ str(md_file_number) + " total files found that match your parameters.")
    print("---------------------------------------------------------------")
    sys.exit()



if __name__ == "__main__":
    file_read() #This starts the entire program.
    closing_message() #this will only run if the user manually goes through all files.
