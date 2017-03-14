import sys
import getopt
import os
import xml.etree.ElementTree as etree
from datetime import datetime


def main(argv):
    inputfolder = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'parse.py -i <inputfolder> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'parse.py -i <inputfolder> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfolder = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if outputfile == '' or inputfolder == '':
        print 'parse.py -i <inputfolder> -o <outputfile>'
        sys.exit(2)

    if not inputfolder.endswith('/'):
        inputfolder = inputfolder + '/'

    files = []
    for entry in os.listdir(inputfolder):
        if entry.endswith('.xml'):
            files.append(inputfolder + entry)

    f = open(outputfile, 'w')
    errorLog = open('./error.log', 'w')

    print 'Initializing csv file'
    f.write('Name;:;CompanyId;:;NACE')
    count = 0
    for inputfile in files:

        total_size = os.path.getsize(inputfile)
        file = open(inputfile, 'r')

        for event, elem in etree.iterparse(file):

            if event is 'end' and elem.tag.endswith('record'):
                try:
                    name = str(elem.getchildren()[0].text)
                    bvdid = str(elem.getchildren()[1].text)
                    nace = str(elem.getchildren()[2].text)

                    f.write('\n%s;:;%s;:;%s' % (name, bvdid, nace))
                except Exception as e:
                    print count
                    errorLog.write('Error parsing patent:\n')
                    errorLog.write(etree.tostring(
                        elem, encoding='utf8', method='xml'))
                    errorLog.write('\n')
                count += 1

            progress = float(file.tell()) / total_size
            sys.stdout.write('\rProcessed %s of file: %s' %
                             ("{:.0%}".format(progress), inputfile))
            sys.stdout.flush()

        print ''


if __name__ == "__main__":
    main(sys.argv[1:])
