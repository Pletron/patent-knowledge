import sys
import MySQLdb


def pretty(d, indent=0):
    for key, value in d.iteritems():
        print '\t' * indent + str(key)
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print '\t' * (indent + 1) + str(value)


def connectToDB(db):
    db = MySQLdb.connect(host="127.0.0.1",
                         user="root",
                         passwd="",
                         db=db)
    return {'database': db, 'cursor': db.cursor()}


def main(argv):
    db = connectToDB("patent_research")
    db['cursor'].execute("SET sql_mode=''")
    db['cursor'].execute(
        "SELECT COUNT(ID) FROM Patents WHERE ApplicationDate != 'None'")

    patentCount = int(db['cursor'].fetchone()[0])
    pages = 200
    offset = patentCount / pages

    for page in range(pages + 1):

        db['cursor'].execute("SELECT ID, ApplicationDate FROM Patents WHERE ApplicationDate != 'None' ORDER BY ApplicationDate LIMIT %d,%d;" % (
            page, offset))
        patents = db['cursor'].fetchall()

        patentScore = []

        for patent in patents:
            query = "SELECT a.ID, InventorsWithExp, UniquePatents, UniqueCompanies, "
            query += "UniqueIndustries, UniquePatentClasses, c.Collaborations FROM (SELECT ppi.Patent "
            query += "AS ID, Count(pi.Inventor) AS ColabCount, p.ApplicationDate, pi.Patent FROM "
            query += "PatentsInventors AS pi INNER JOIN (SELECT Inventor, Patent, ApplicationDate "
            query += "FROM PatentsInventors AS pi INNER JOIN Patents AS p ON p.ID = pi.Patent "
            query += "WHERE Patent = '%s' AND ApplicationDate IS NOT NULL) AS ppi ON ppi.Inventor " % patent[
                0]
            query += "= pi.Inventor INNER JOIN Patents AS p ON p.ID = pi.Patent INNER JOIN "
            query += "Inventors AS i ON i.ID = pi.Inventor INNER JOIN Companies AS c ON c.ID = p.Company "
            query += "WHERE p.ID != ppi.Patent AND p.ApplicationDate <= ppi.ApplicationDate GROUP "
            query += "BY pi.Patent HAVING ColabCount > 1 ORDER BY ApplicationDate) AS a INNER JOIN "
            query += "(SELECT ppi.Patent AS ID, Count(DISTINCT i.ID) AS InventorsWithExp, Count( "
            query += "DISTINCT p.ID) AS UniquePatents, Count(DISTINCT c.ID) AS UniqueCompanies, "
            query += "Count(DISTINCT c.Industry) AS UniqueIndustries, Count(DISTINCT p.Class) AS "
            query += "UniquePatentClasses FROM PatentsInventors AS pi INNER JOIN (SELECT Inventor, "
            query += "Patent, ApplicationDate FROM PatentsInventors AS pi INNER JOIN Patents AS p "
            query += "ON p.ID = pi.Patent WHERE Patent = '%s' AND ApplicationDate IS NOT NULL) " % patent[
                0]
            query += "AS ppi ON ppi.Inventor = pi.Inventor INNER JOIN Patents AS p ON p.ID = pi.Patent "
            query += "INNER JOIN Inventors AS i ON i.ID = pi.Inventor INNER JOIN Companies AS c "
            query += "ON c.ID = p.Company WHERE p.ID != ppi.Patent AND p.ApplicationDate <= ppi.ApplicationDate) "
            query += "AS b ON a.ID = b.ID INNER JOIN (SELECT a.ID, Count(*) Collaborations FROM ( "
            query += "SELECT ppi.ID, pi.Patent, pi.Inventor FROM PatentsInventors AS pi INNER JOIN "
            query += "(SELECT p.ID, Inventor, Patent, ApplicationDate FROM PatentsInventors AS pi "
            query += "INNER JOIN Patents AS p ON p.ID = pi.Patent WHERE Patent = '%s' AND " % patent[
                0]
            query += "ApplicationDate IS NOT NULL) AS ppi ON ppi.Inventor = pi.Inventor INNER JOIN "
            query += "Patents AS p ON p.ID = pi.Patent WHERE p.ID != ppi.Patent AND p.ApplicationDate "
            query += "<= ppi.ApplicationDate) AS a JOIN (SELECT pi.Patent, pi.Inventor FROM "
            query += "PatentsInventors AS pi INNER JOIN (SELECT Inventor, Patent, ApplicationDate "
            query += "FROM PatentsInventors AS pi INNER JOIN Patents AS p ON p.ID = pi.Patent "
            query += "WHERE Patent = '%s' AND ApplicationDate IS NOT NULL) AS ppi ON ppi.Inventor " % patent[
                0]
            query += "= pi.Inventor INNER JOIN Patents AS p ON p.ID = pi.Patent WHERE p.ID != ppi.Patent "
            query += "AND p.ApplicationDate <= ppi.ApplicationDate) AS b ON a.Patent = b.Patent "
            query += "AND a.Inventor < b.Inventor) AS c ON c.ID = a.ID GROUP BY a.ID;"

            db['cursor'].execute(query)
            result = db['cursor'].fetchone()
            if result is None:
                patentScore.append({"patentID": str(patent[0]),
                                    "applicationDate": str(patent[1]),
                                    "invWithExp": 0,
                                    "uniPatents": 0,
                                    "uniCompanies": 0,
                                    "uniIndustries": 0,
                                    "uniPatentClasses": 0,
                                    "collaborations": 0})
            else:
                patentScore.append({"patentID": str(patent[0]),
                                    "applicationDate": str(patent[1]),
                                    "invWithExp": int(result[1]),
                                    "uniPatents": int(result[2]),
                                    "uniCompanies": int(result[3]),
                                    "uniIndustries": int(result[4]),
                                    "uniPatentClasses": int(result[5]),
                                    "collaborations": int(result[6])})

        query = "INSERT INTO "
        query += "PatentScore "
        query += "(Patent, "
        query += "InventorsWithExp, "
        query += "UniquePatents, "
        query += "UniqueCompanies, "
        query += "UniqueIndustries, "
        query += "UniquePatentClasses, "
        query += "Collaborations) "
        query += "VALUES "

        for score in patentScore:
            query += "('%s', %d, %d, %d, %d, %d, %d)," % (score['patentID'], score['invWithExp'], score[
                'uniPatents'], score['uniCompanies'], score['uniIndustries'], score['uniPatentClasses'], score['collaborations'])

        query = query[:-1] + ";"

        try:
            db['cursor'].execute(query)
            db['database'].commit()
        except:
            print query
            exit(0)

        progress = float(page + 1) / pages
        sys.stdout.write('\rProcessed %s' %
                         ("{:.0%}".format(progress)))
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
