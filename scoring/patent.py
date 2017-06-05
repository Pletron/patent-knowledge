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
    db = connectToDB("patent_research_dev")
    db['cursor'].execute("SET sql_mode=''")
    db['cursor'].execute(
        "SELECT COUNT(ID) FROM Patents WHERE AppDate != 'None'")

    patentCount = int(db['cursor'].fetchone()[0])
    pages = 2000
    offset = patentCount / pages

    for page in range(pages + 1):

        db['cursor'].execute("SELECT ID, AppDate FROM Patents WHERE AppDate != 'None' LIMIT %d,%d;" % (
            page * offset, offset))
        patents = db['cursor'].fetchall()
        patentScore = []

        for patent in patents:
            query = "SELECT "
            query += "IFNULL(PatentScore.Inventors,0) InventorsWithExp, "
            query += "IFNULL(PatentScore.Patents,0) UniquePatents, "
            query += "IFNULL(PatentScore.Companies,0) UniqueCompanies, "
            query += "IFNULL(PatentScore.Industries,0) UniqueIndustries, "
            query += "IFNULL(PatentScore.Classifications,0) UniquePatentClasses, "
            query += "IFNULL(Collaborations.Collaborations,0) Collaborations, "
            query += "IFNULL(StarInventors.StarInventors,0) StarInventors, "
            query += "IFNULL(InventorScore.Patents,0) InventorPatents, "
            query += "IFNULL(InventorScore.Companies,0) InventorCompanies, "
            query += "IFNULL(InventorScore.Industries,0) InventorIndustries, "
            query += "IFNULL(InventorScore.Classifications,0) InventorPatentClasses "
            query += "FROM "
            query += "(SELECT "
            query += "COUNT(DISTINCT Inventor) Inventors, "
            query += "SUM(Patents) Patents, "
            query += "SUM(Companies) Companies, "
            query += "SUM(Industries) Industries, "
            query += "SUM(Classifications) Classifications "
            query += "FROM "
            query += "(SELECT "
            query += "Inventor, "
            query += "COUNT(DISTINCT p.ID) Patents, "
            query += "COUNT(DISTINCT p.Company) Companies, "
            query += "COUNT(DISTINCT Industry) Industries, "
            query += "COUNT(DISTINCT Class) Classifications "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "INNER JOIN "
            query += "Companies AS c ON c.ID=p.Company "
            query += "JOIN "
            query += "(SELECT AppDate FROM Patents WHERE ID='%s') AS t1 " % str(
                patent[0])
            query += "WHERE "
            query += "pi.Inventor IN (SELECT Inventor FROM PatentsInventors WHERE Patent='%s') " % str(
                patent[0])
            query += "AND "
            query += "p.AppDate<t1.AppDate "
            query += "GROUP BY "
            query += "Inventor) AS t1) AS InventorScore "
            query += "JOIN "
            query += "(SELECT "
            query += "COUNT(DISTINCT pi.Inventor) Inventors, "
            query += "COUNT(DISTINCT c.ID) Companies, "
            query += "COUNT(DISTINCT p.ID) Patents, "
            query += "COUNT(DISTINCT c.Industry) Industries, "
            query += "COUNT(DISTINCT p.Class) Classifications "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "INNER JOIN "
            query += "Companies AS c ON c.ID=p.Company "
            query += "JOIN "
            query += "(SELECT AppDate FROM Patents WHERE ID='%s') AS pInfo " % str(
                patent[0])
            query += "WHERE "
            query += "Inventor IN (SELECT Inventor FROM PatentsInventors WHERE Patent='%s') " % str(
                patent[0])
            query += "AND "
            query += "p.AppDate<pInfo.AppDate) AS PatentScore "
            query += "JOIN "
            query += "(SELECT COUNT(*) AS Collaborations "
            query += "FROM ( "
            query += "SELECT Inventor "
            query += ",Patent "
            query += "FROM PatentsInventors AS pi "
            query += "INNER JOIN Patents AS p ON pi.Patent = p.ID "
            query += "INNER JOIN ( "
            query += "SELECT AppDate "
            query += "FROM Patents "
            query += "WHERE ID = '%s' " % str(patent[0])
            query += ") AS t1 "
            query += "WHERE Inventor IN ( "
            query += "SELECT Inventor "
            query += "FROM PatentsInventors "
            query += "WHERE Patent = '%s' " % str(patent[0])
            query += ") "
            query += "AND p.AppDate < t1.AppDate "
            query += ") AS x "
            query += "INNER JOIN ( "
            query += "SELECT Inventor "
            query += ",Patent "
            query += "FROM PatentsInventors AS pi "
            query += "INNER JOIN Patents AS p ON pi.Patent = p.ID "
            query += "INNER JOIN ( "
            query += "SELECT AppDate "
            query += "FROM Patents "
            query += "WHERE ID = '%s' " % str(patent[0])
            query += ") AS t1 "
            query += "WHERE Inventor IN ( "
            query += "SELECT Inventor "
            query += "FROM PatentsInventors "
            query += "WHERE Patent = '%s' " % str(patent[0])
            query += ") "
            query += "AND p.AppDate < t1.AppDate "
            query += ") AS y ON x.Patent = y.Patent "
            query += "AND x.Inventor < y.Inventor) AS Collaborations "
            query += "JOIN "
            query += "(SELECT "
            query += "COUNT(DISTINCT Inventor) StarInventors "
            query += "FROM "
            query += "StarInventors AS si "
            query += "JOIN "
            query += "(SELECT AppDate FROM Patents WHERE ID='%s') AS pInfo " % str(
                patent[0])
            query += "WHERE "
            query += "Inventor IN (SELECT Inventor FROM PatentsInventors WHERE Patent='%s') " % str(
                patent[0])
            query += "AND "
            query += "si.AppDate<pInfo.AppDate) AS StarInventors;"

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
                                    "collaborations": 0,
                                    "starInventors": 0,
                                    "invPatents": 0,
                                    "invCompanies": 0,
                                    "invIndustries": 0,
                                    "invPatentClasses": 0})
            else:
                patentScore.append({"patentID": str(patent[0]),
                                    "applicationDate": str(patent[1]),
                                    "invWithExp": int(result[0]),
                                    "uniPatents": int(result[1]),
                                    "uniCompanies": int(result[2]),
                                    "uniIndustries": int(result[3]),
                                    "uniPatentClasses": int(result[4]),
                                    "collaborations": int(result[5]),
                                    "starInventors": int(result[6]),
                                    "invPatents": int(result[7]),
                                    "invCompanies": int(result[8]),
                                    "invIndustries": int(result[9]),
                                    "invPatentClasses": int(result[10])})

        query = "INSERT IGNORE INTO "
        query += "PatentScoresV4 "
        query += "(Patent, "
        query += "InventorsWithExp, "
        query += "UniquePatents, "
        query += "UniqueCompanies, "
        query += "UniqueIndustries, "
        query += "UniquePatentClasses, "
        query += "Collaborations, "
        query += "StarInventors, "
        query += "InventorPatents, "
        query += "InventorCompanies, "
        query += "InventorIndustries, "
        query += "InventorPatentClasses) "
        query += "VALUES "

        for score in patentScore:
            query += "('%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d),\n" % (score['patentID'], score['invWithExp'], score[
                'uniPatents'], score['uniCompanies'], score['uniIndustries'], score['uniPatentClasses'], score['collaborations'], score['starInventors'], score['invPatents'], score['invCompanies'], score['invIndustries'], score['invPatentClasses'])

        query = query[:-2] + ";"

        try:
            db['cursor'].execute(query)
            db['database'].commit()
        except:
            print query
            sys.exit(0)

        progress = float(page + 1) / pages
        sys.stdout.write('\rProcessed %s' %
                         ("{:.0%}".format(progress)))
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
