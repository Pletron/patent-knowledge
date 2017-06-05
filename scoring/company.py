import sys
import MySQLdb


def connectToDB(db):
    db = MySQLdb.connect(host="127.0.0.1",
                         user="root",
                         passwd="",
                         db=db)
    return {'database': db, 'cursor': db.cursor()}


def main(argv):
    db = connectToDB("patent_research_dev")
    db['cursor'].execute(
        'SET sql_mode="";')
    db['cursor'].execute(
        'SELECT COUNT(ID) FROM Companies;')
    compcount = int(db['cursor'].fetchone()[0])

    pages = 100
    limit = compcount / pages
    print limit

    for page in range(0, pages + 1):

        db['cursor'].execute(
            'SELECT * FROM Companies LIMIT %d OFFSET %d;' % (limit, (limit * page)))
        companies = db['cursor'].fetchall()

        for company in companies:

            yearQuery = "SELECT "
            yearQuery += "MIN(YEAR(AppDate)) Start, "
            yearQuery += "MAX(YEAR(AppDate)) End "
            yearQuery += "FROM "
            yearQuery += "Patents AS p "
            yearQuery += "WHERE "
            yearQuery += "Company='%s';" % str(company[0])

            db['cursor'].execute(yearQuery)
            yearSpan = db['cursor'].fetchone()

            totalScore = []

            for i, year in enumerate(range(yearSpan[0], yearSpan[1] + 1)):
                inventorQuery = "SELECT DISTINCT "
                inventorQuery += "Inventor "
                inventorQuery += "FROM "
                inventorQuery += "Patents AS p "
                inventorQuery += "INNER JOIN "
                inventorQuery += "PatentsInventors AS pi ON p.ID=pi.Patent "
                inventorQuery += "WHERE "
                inventorQuery += "Company='%s' " % str(company[0])
                inventorQuery += "AND "
                inventorQuery += "AppYear=%d;" % int(year)

                db['cursor'].execute(inventorQuery)
                inventors = db['cursor'].fetchall()

                Patents = 0
                Companies = 0
                Industries = 0
                StarPatents = 0
                PatentClassifications = 0

                for inventor in inventors:
                    scoreQuery = "SELECT "
                    scoreQuery += "IFNULL(SUM(Patents),0) AS Patents, "
                    scoreQuery += "IFNULL(SUM(Companies),0) AS Companies, "
                    scoreQuery += "IFNULL(SUM(Industries),0) AS Industries, "
                    scoreQuery += "IFNULL(SUM(StarPatents),0) AS StarPatents, "
                    scoreQuery += "IFNULL(SUM(PatentClassifications),0) AS PatentClassifications  "
                    scoreQuery += "FROM "
                    scoreQuery += "InventorScoreV2 AS inv "
                    scoreQuery += "WHERE "
                    scoreQuery += "Inventor='%s' " % str(inventor[0])
                    scoreQuery += "AND "
                    scoreQuery += "Year<%d " % year
                    scoreQuery += "ORDER BY "
                    scoreQuery += "Year;"

                    db['cursor'].execute(scoreQuery)
                    inventorScore = db['cursor'].fetchone()

                    Patents += int(inventorScore[0])
                    Companies += int(inventorScore[1])
                    Industries += int(inventorScore[2])
                    StarPatents += int(inventorScore[3])
                    PatentClassifications += int(inventorScore[4])

                companyQuery = "SELECT "
                companyQuery += "IFNULL(YEAR(p.AppDate),0) Year, "
                companyQuery += "IFNULL(COUNT(DISTINCT p.ID),0) Patents, "
                companyQuery += "SUM(case when p.Citing>(pcc.AvgCiting+pcc.StdCiting*3) then 1 else 0 end) CompanyStarPatents, "
                companyQuery += "IFNULL(COUNT(DISTINCT pi.Inventor),0) Inventors, "
                companyQuery += "IFNULL(COUNT(DISTINCT si.Inventor),0) StarInventors "
                companyQuery += "FROM "
                companyQuery += "Patents AS p "
                companyQuery += "INNER JOIN "
                companyQuery += "PatentsInventors AS pi ON pi.Patent=p.ID "
                companyQuery += "JOIN "
                companyQuery += "PatentClassCiting AS pcc ON pcc.Class=p.Class AND pcc.Year=p.AppYear "
                companyQuery += "LEFT JOIN "
                companyQuery += "StarInventorsV2 AS si ON si.Inventor=pi.Inventor AND si.AppDate<p.AppDate "
                companyQuery += "WHERE "
                companyQuery += "Company='%s' " % str(company[0])
                companyQuery += "AND "
                companyQuery += "AppYear=%d " % year
                companyQuery += "GROUP BY "
                companyQuery += "p.AppYear;"
                db['cursor'].execute(companyQuery)
                companyInfo = db['cursor'].fetchone()
                if companyInfo is None:
                    companyInfo = [0, 0, 0, 0, 0]

                totalScore.append({
                    'Year': year,
                    'CompanyPatents': int(companyInfo[1]),
                    'CompanyStarPatents': int(companyInfo[2]),
                    'Inventors': int(companyInfo[3]),
                    'StarInventors': int(companyInfo[4]),
                    'Patents': Patents,
                    'Companies': Companies,
                    'Industries': Industries,
                    'StarPatents': StarPatents,
                    'PatentClassifications': PatentClassifications
                })

            insertQuery = "INSERT IGNORE INTO "
            insertQuery += "CompanyScoreV7 "
            insertQuery += "(Company, "
            insertQuery += "Year, "
            insertQuery += "CompanyPatents, "
            insertQuery += "CompanyStarPatents, "
            insertQuery += "Inventors, "
            insertQuery += "StarInventors, "
            insertQuery += "Patents, "
            insertQuery += "Companies, "
            insertQuery += "Industries, "
            insertQuery += "StarPatents, "
            insertQuery += "PatentClasses) "
            insertQuery += "VALUES "

            for score in totalScore:
                insertQuery += "('%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d),\n" % (str(company[0]), score['Year'], score['CompanyPatents'], score['CompanyStarPatents'], score['Inventors'], score[
                    'StarInventors'], score['Patents'], score['Companies'], score['Industries'], score['StarPatents'], score['PatentClassifications'])

            insertQuery = insertQuery[:-2] + ";"

            try:
                db['cursor'].execute(insertQuery)
                db['database'].commit()
            except:
                print insertQuery
                sys.exit(0)

        progress = float(page + 1) / pages
        sys.stdout.write('\rProcessed %s' %
                         ("{:.0%}".format(progress)))
        sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
