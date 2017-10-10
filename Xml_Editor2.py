import lxml
from lxml import etree
import readline
import os
from sys import exit
import sys


def getPath():

    print("Please type the relative or full path to the directory you want to work in...")
    file_path = input("Folder path: ")
    if os.path.isdir(file_path):
        return file_path
    else:
        print("That does not appear to be a valid path to a directory.")
        getPath(file_path)


def get_files_from_directory(file_path):
    file_list = []
    # this looks at every item at the filepath above and does the following:
    for root, dirs, files in os.walk(file_path):
        for filename in files:  # this looks at each files name for each item
            # if any file name ends with .xml, but not .aux.xml then...
            if filename.endswith(".fgdc.xml") and not filename.endswith(".aux.xml") and not filename.endswith(".tif.xml"):
                global md_file_number
                md_file_number += 1  # This adds 1 to the number of metadata files that the program has found for each file that it finds that matches the parameters set forth above
                print(
                    "Found a file that fits your parameters! {0}".format(filename))
                metadata_file = os.path.join(root, filename)
                file_list.append(metadata_file)
    print("The number of files that meet your requirements: {0}".format(
        md_file_number))
    return file_list


def add_DistInfo(file_list):
    global function
    function = "add_DistInfo"

    for item in file_list:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(item, parser)
        root = tree.getroot()
        distinfo = None
        if root.xpath("//distinfo"):
            print("distinfo already exists")
            distinfo = root.xpath("//distinfo")[0]
            print(etree.tostring(distinfo, pretty_print=True))
            root.remove(distinfo)
        else:
            print("distinfo does not already exist")

        # for elem in tree.xpath("//distinfo"):
        #     elem.getparent().remove(elem)
        distinfo = etree.SubElement(root, "distinfo")
        distrib = etree.SubElement(distinfo, "distrib")
        cntinfo = etree.SubElement(distrib, "cntinfo")
        cntorgp = etree.SubElement(cntinfo, "cntorgp")
        cntorg = etree.SubElement(cntorgp, "cntorg")
        cntorg.text = "U.S. Geological Survey - ScienceBase"
        cntaddr = etree.SubElement(cntinfo, "cntaddr")
        addrtype = etree.SubElement(cntaddr, "addrtype")
        addrtype.text = "Mailing and Physical"
        address = etree.SubElement(cntaddr, "address")
        address.text = "Denver Federal Center"
        address = etree.SubElement(cntaddr, "address")
        address.text = "Building 810"
        address = etree.SubElement(cntaddr, "address")
        address.text = "Mail Stop 302"
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
        stdorder = etree.SubElement(distinfo, "stdorder")
        digform = etree.SubElement(stdorder, "digform")
        digtinfo = etree.SubElement(digform, "digtinfo")
        formname = etree.SubElement(digtinfo, "formname")
        formname.text = "Tabular Digital Data"
        digtopt = etree.SubElement(digform, "digtopt")
        onlinopt = etree.SubElement(digtopt, 'onlinopt')
        computer = etree.SubElement(onlinopt, 'computer')
        networka = etree.SubElement(computer, 'networka')
        networkr = etree.SubElement(networka, 'networkr')
        networkr.text = "http://doi.org/10.5066/F7RX99V3"
        fees = etree.SubElement(stdorder, 'fees')
        fees.text = "None. No fees are applicable for obtaining the data set."

        root.insert(5, distinfo)
        print("Will change distinfo to: ")
        print(etree.tostring(distinfo, pretty_print=True))

        status()
        global all_2
        if all_2 is not True:
            write_ = write(item)
            if write_ is True:
                tree.write(item, pretty_print=True)
            else:
                pass
        elif all_2 is True:
            global file_count
            global total_examined_file_count
            file_count += 1
            total_examined_file_count += 1
            global done_files
            done_files.append(item)
            tree.write(item, pretty_print=True)


def add_DOI(file_list):
    global function
    function = "add_DOI"
    for item in file_list:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(item, parser)
        root = tree.getroot()
        print("Current item: {0}".format(item))
        # add doi and doi url to citeinfo's othercit and onlink tags
        citeinfo = root.find(".//citation//citeinfo")
        print(etree.tostring(citeinfo, pretty_print=True))
        # print(citeinfo.tag)
        geoformXPath = tree.xpath("//citation//citeinfo//geoform")
        geoform = geoformXPath[0]
        # print(geoform.tag)
        geo_index = citeinfo.index(geoform)
        # print(geo_index)
        if citeinfo.xpath("//othercit"):
            print("othercit already exists")
            othercit = citeinfo.xpath("//othercit")
            citeinfo.remove(othercit[0])
        else:
            print("othercit does not already exist")

        if citeinfo.xpath("//onlink"):
            print("onlink already exists")
            onlink = citeinfo.xpath("//onlink")
            citeinfo.remove(onlink[0])
        else:
            print("onlink does not already exist")
        othercit_index = geo_index + 1
        onlink_index = othercit_index + 1
        othercit = etree.Element("othercit")
        othercit.text = "doi: 10.5066/F7RX99V3"
        print("Adding: {0}".format(othercit.tag))
        print("Adding: {0}".format(othercit.text))
        onlink = etree.Element("onlink")
        onlink.text = "http://doi.org/10.5066/F7RX99V3"
        print("Adding: {0}".format(onlink.tag))
        print("Adding: {0}".format(onlink.text))
        citeinfo.insert(othercit_index, othercit)
        citeinfo.insert(onlink_index, onlink)
        print(etree.tostring(citeinfo, pretty_print=True))

        status()
        global all_1
        if all_1 is not True:
            write_ = write(item)
            if write_ is True:
                tree.write(item, pretty_print=True)
            else:
                pass
        elif all_1 is True:
            global file_count
            global total_examined_file_count
            file_count += 1
            total_examined_file_count += 1
            global done_files
            done_files.append(item)
            tree.write(item, pretty_print=True)


def status():
    print("---------------------------------------------------------------")
    print("Files written so far: " + str(file_count) +
          " of " + str(md_file_number))
    print("Files examined so far: " +
          str(total_examined_file_count) + " of " + str(md_file_number))
    print("\n")
    print("You have changed " + str(file_count) + " files out of the " +
          str(total_examined_file_count) + " examined so far.")
    print("There are " + str(md_file_number) +
          " total files found that match your parameters.")
    print("---------------------------------------------------------------")


def write(item):
    print('Write changes to file? (Y/N)')
    print("Type 'all' to apply changes to all files.")
    answer = input('> ').lower()
    global function
    global file_count
    global total_examined_file_count
    global done_files
    if 'all' in answer:

        if function == 'add_DOI':
            global all_1
            all_1 = True
            print("all_1: {0}".format(all_1))
            file_count += 1
            total_examined_file_count += 1
            done_files.append(item)
            return True
        elif function == 'add_DistInfo':
            global all_2
            all_2 = True
            print("all_2: {0}".format(all_1))
            file_count += 1
            total_examined_file_count += 1
            done_files.append(item)
            return True
        else:
            print('Something wrong in write()')
    elif 'y' in answer:
        file_count += 1
        total_examined_file_count += 1
        done_files.append(item)
        return True
    elif 'n' in answer:
        file_count += 0
        total_examined_file_count += 1
        done_files.append(item)
        return False
    else:
        print("Please type 'y' or 'n'")
        write(item)


def clear_count():
    global file_count
    file_count = 0
    global md_file_number
    global function
    function = None
    global total_examined_file_count
    total_examined_file_count = 0
    global done_files
    done_files.clear()
    global all_1
    all_1 = False
    global all_2
    all_2 = False


file_count = 0  # this is so we can keep track of how many files the program fully runs through. Print at the end so we know if it missed any
global md_file_number
md_file_number = 0  # this creates a variable that represents how many files the program found that match the parameters below. Obviously, we start at zero
# This creates a variable to represent every file we've looked at, whether or not we've changed it.
global function
total_examined_file_count = 0
remaining_files = int(md_file_number) - int(file_count)
done_files = []
global all_1
all_1 = False
global all_2
all_2 = False


def getFile():
    print(
        '''
    Please type the relative or full path to the file you want to edit...
    ''')
    metadata_file = input("> ")
    if os.path.exists(metadata_file):
        if metadata_file.endswith(".xml"):
            global md_file_number
            md_file_number += 1
            return metadata_file
        else:
            print("That does not appear to be a valid .xml file.")
            getFile()

    else:
        print("That does not appear to be a valid path to a file.")
        getFile()


def closing_message():
    print("\n \n \n \n ")
    print("That's all the files! Here's what we did:")
    print("---------------------------------------------------------------")
    print("Total number of files written: " +
          str(file_count) + " of " + str(md_file_number))
    print("Total number of files examined by the program: " +
          str(total_examined_file_count) + " of " + str(md_file_number))
    print("\n")
    print("We changed " + str(file_count) + " files out of the " +
          str(total_examined_file_count) + " that matched the parameters you set forth.")
    print("There are " + str(md_file_number) +
          " total files found that match your parameters.")
    print("---------------------------------------------------------------")


def main():
    print('''
    Are we editing a single file or multiple .xml files?
    ('one'/'many') 
    ''')
    answer = input('> ').lower()
    file_list = []
    if 'one' in answer or 'o' in answer:
        metadata_file = getFile()
        file_list.append(metadata_file)
    elif 'many' in answer or 'm' in answer:
        file_path = getPath()
        file_list = get_files_from_directory(file_path)
    # file_list = ["data/trial3.xml"] #Debugging
    add_DOI(file_list)
    clear_count()
    add_DistInfo(file_list)


if __name__ == "__main__":
    print("Welcome! Starting program...")
    main()  # This starts the entire program.
    # this will only run if the user manually goes through all files.
    closing_message()
