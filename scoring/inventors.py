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
        "SELECT COUNT(ID) FROM Inventors")

    patentCount = int(db['cursor'].fetchone()[0])
    pages = 2000
    offset = patentCount / pages

    for page in range(pages + 1):

        db['cursor'].execute("SELECT ID FROM Inventors LIMIT %d,%d;" % (
            page * offset, offset))
        inventors = db['cursor'].fetchall()
        patentScore = []

        for inventor in inventors:
            query = "INSERT INTO "
            query += "InventorScoreV2 "
            query += "SELECT "
            query += "Inventor, "
            query += "PatentCount.Year, "
            query += "Patents, "
            query += "COUNT(DISTINCT Company) Companies, "
            query += "COUNT(DISTINCT Industry) Industries, "
            query += "COUNT(DISTINCT Class) Classifications, "
            query += "IFNULL(StarPatents,0) StarPatents "
            query += "FROM "
            query += "(SELECT  "
            query += "YEAR(AppDate) Year, "
            query += "Inventor, "
            query += "COUNT(DISTINCT p.ID) Patents "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "WHERE "
            query += "Inventor='%s' " % str(inventor[0])
            query += "GROUP BY "
            query += "Year) AS PatentCount "
            query += "LEFT JOIN "
            query += "(SELECT "
            query += "MIN(YEAR(AppDate)) Year, "
            query += "Company "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "WHERE "
            query += "Inventor='%s' " % str(inventor[0])
            query += "GROUP BY "
            query += "Company "
            query += "ORDER BY "
            query += "Year) AS CompanyCount ON PatentCount.Year=CompanyCount.Year "
            query += "LEFT JOIN "
            query += "(SELECT "
            query += "MIN(YEAR(AppDate)) Year, "
            query += "Industry "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "INNER JOIN "
            query += "Companies AS c ON c.ID=p.Company "
            query += "WHERE "
            query += "Inventor='%s' " % str(inventor[0])
            query += "GROUP BY "
            query += "Industry "
            query += "ORDER BY "
            query += "Year) AS IndustryCount ON PatentCount.Year=IndustryCount.Year "
            query += "LEFT JOIN "
            query += "(SELECT  "
            query += "MIN(YEAR(AppDate)) Year, "
            query += "Class "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "WHERE "
            query += "Inventor='%s' " % str(inventor[0])
            query += "GROUP BY "
            query += "Class) AS ClassificationCount ON PatentCount.Year=ClassificationCount.Year "
            query += "LEFT JOIN "
            query += "(SELECT  "
            query += "YEAR(AppDate) Year, "
            query += "COUNT(DISTINCT p.ID) StarPatents "
            query += "FROM "
            query += "PatentsInventors AS pi "
            query += "INNER JOIN "
            query += "Patents AS p ON p.ID=pi.Patent "
            query += "INNER JOIN "
            query += "PatentClassCiting AS pc ON pc.Class=p.Class AND pc.Year=p.PubYear "
            query += "WHERE "
            query += "Inventor='%s' " % str(inventor[0])
            query += "AND "
            query += "Citing>AvgCiting+(3*StdCiting) "
            query += "GROUP BY "
            query += "Year "
            query += "ORDER BY "
            query += "Year) AS StarPatentCount ON PatentCount.Year=StarPatentCount.Year "
            query += "GROUP BY "
            query += "PatentCount.Year;"

            db['cursor'].execute(query)
            db['database'].commit()

        progress = float(page + 1) / pages
        sys.stdout.write('\rProcessed %s' %
                         ("{:.0%}".format(progress)))
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
