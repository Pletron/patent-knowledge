import sys
import getopt
import os
import shutil
import re
import MySQLdb
import xml.etree.ElementTree as etree


def findpatent(patent, db):
    cur = db.cursor()
    base_query = "SELECT DISTINCT Patent FROM inventors WHERE "
    found = False
    for inventor in patent['Inventors']:
        query = []

        query.append("Firstname LIKE '%s'" % inventor['Firstname'])
        query.append("Lastname LIKE '%s'" % inventor['Lastname'])
        query.append("(Country LIKE '%s' OR Country LIKE '')" %
                     inventor['Country'])
        if len(patent['Patent_ID']) > 1:
            query.append("PubYear=%d AND (Patent LIKE '%s' OR Patent LIKE '%s')" % (patent['PubYear'],
                                                                                    patent['Patent_ID'][0], patent['Patent_ID'][1]))
        else:
            query.append("PubYear=%d AND Patent LIKE '%s'" % (patent['PubYear'],
                                                              patent['Patent_ID'][0]))

        for x in xrange(0, len(query)):
            exec_query = base_query + ' AND '.join(query)
            cur.execute(exec_query)
            result = cur.fetchall()

            if len(result) == 1:
                update_query = "UPDATE inventors SET Company_ID='%s', Match_Level='%d', Citing='%d', Cited='%d', Classification='%s' WHERE Patent='%s'" % (
                    patent['Company_ID'], (x + 1), patent['Citing'], patent['Cited'], patent['Classification'], result[0][0])
                cur.execute(update_query)
                db.commit()
                found = True
                found_level = (x + 1)
                break
            del query[0]

        if found:
            break

    if not found:
        if not patent['Inventors']:
            fail_query = "INSERT INTO failed_matches (PubYear, Company_ID, Pat_ID) VALUES('%s', '%s', '%s')" % (
                patent['PubYear'], patent['Company_ID'], patent['Pat_ID'])
        else:
            fail_query = "INSERT INTO failed_matches (Firstname, Lastname, Country, PubYear, Company_ID, Pat_ID) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (patent['Inventors'][0][
                'Firstname'], patent['Inventors'][0]['Lastname'], patent['Inventors'][0]['Country'], patent['PubYear'], patent['Company_ID'], patent['Pat_ID'])
        cur.execute(fail_query)
        db.commit()

    return found


def splitinventors(inventors, country):
    inventorlist = []
    for i, inventor in enumerate(inventors):
        try:
            fname = fullname = inventor.text.encode(
                'ascii', 'ignore').replace('.', '').replace('\'', '%').replace('-', '%')
        except:
            fname = fullname = ''

        namelength = len(fullname.split(', ')) - 1
        if not namelength:
            namelength = len(fullname.split('; ')) - 1
        if not namelength:
            namelength = len(fullname.split(' ')) - 1

        if ', ' in fullname:
            fullname = fullname.split(', ')
        elif '; ' in fullname:
            fullname = fullname.split('; ')
        else:
            fullname = fullname.split(' ')

        namelength = len(fullname) - 1

        lastname = fullname[0].split(' ')
        lastname = lastname[0] + "%"
        firstname = fullname[namelength].split(' ')
        firstname = firstname[0] + "%"

        inv_country = country[i].text

        if len(lastname.split('%')) > 2:
            if len(lastname.split('%')[0]) > 1:
                lastname = lastname.split('%')[0] + '%'
            else:
                lastname = lastname.split(
                    '%')[0] + '%' + lastname.split('%')[1] + '%'

        inventorlist.append(
            {'Fullname': fname, 'Firstname': firstname, 'Lastname': lastname, 'Country': inv_country})
    return inventorlist


def capturepatid(patent_id):
    patent_id = patent_id.replace('US', '')
    patent_ids = []
    p_in = '(P)' in patent_id
    paranthesis_pos = patent_id.index('(')
    patent_id = patent_id[:paranthesis_pos]
    digit_pos = re.search('\d', patent_id).start()

    if p_in:
        if digit_pos is 0:
            patent_id = "PP" + patent_id
        if len(patent_id) < 8:
            patent_id += '%'
        patent_ids.append(patent_id)
    else:

        patent_ids.append(patent_id + "%")
        patent_id = patent_id[
            : digit_pos] + '%' + patent_id[digit_pos:]
        patent_ids.append(patent_id)
    return patent_ids


def main(argv):
    inputfolder = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print 'parse.py -i <inputfolder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'parse.py -i <inputfolder>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfolder = arg

    if inputfolder == '':
        print 'parse.py -i <inputfolder>'
        sys.exit(2)

    if not inputfolder.endswith('/'):
        inputfolder = inputfolder + '/'

    files = []
    for entry in os.listdir(inputfolder):
        if entry.endswith('.xml'):
            files.append(inputfolder + entry)

    db = MySQLdb.connect(host="127.0.0.1",
                         user="root",
                         passwd="",
                         db="patents")
    cur = db.cursor()
    company_id = ''
    print '\n\n### Running matches ###\n'
    for inputfile in files:
        ignorecount = failcount = successcount = 0
        total_size = os.path.getsize(inputfile)
        file = open(inputfile, 'r')
        for event, elem in etree.iterparse(file):

            if event is 'end' and elem.tag.endswith('record'):
                pubyear = int(elem.getchildren()[8].text.split('/')[0])
                if (pubyear <= 2012 and pubyear >= 1982):

                    pat_id = str(elem.getchildren()[1].text)
                    check_query = "SELECT EXISTS(SELECT 1 FROM processed_patents WHERE patent_id='%s')" % (
                        pat_id)
                    cur.execute(check_query)
                    if cur.fetchone()[0] != 1:
                        patent_id = capturepatid(pat_id)
                        inventors = splitinventors(
                            elem.getchildren()[6], elem.getchildren()[7])

                        for owner in elem.getchildren()[2]:
                            if owner.text:
                                company_id = owner.text

                        try:
                            citing = int(elem.getchildren()[3].text)
                        except:
                            citing = 0

                        try:
                            cited = int(elem.getchildren()[4].text)
                        except:
                            cited = 0
                        classification = str(elem.getchildren()[5].text)

                        patent = {
                            'PubYear': pubyear,
                            'Pat_ID': pat_id,
                            'Patent_ID': patent_id,
                            'Inventors': inventors,
                            'Company_ID': company_id,
                            'Citing': citing,
                            'Cited': cited,
                            'Classification': classification
                        }

                        result = findpatent(patent, db)
                        if not result:
                            failcount += 1
                        else:
                            successcount += 1

                        update_query = "INSERT INTO processed_patents (patent_id) VALUES('%s')" % (
                            pat_id)
                        cur.execute(update_query)
                        db.commit()
                    else:
                        ignorecount += 1
                else:
                    ignorecount += 1

                progress = float(file.tell()) / total_size
                sys.stdout.write('\rFilename: %s - Processed: %s\t| Failed: %d Success: %d Ignored: %d' %
                                 (inputfile, "{:.0%}".format(progress), failcount, successcount, ignorecount))
                sys.stdout.flush()

        move_destination = "./processed/" + \
            inputfile.split('/')[len(inputfile.split('/')) - 1]
        shutil.move(inputfile, move_destination)
        print ''


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main(sys.argv[1:])
