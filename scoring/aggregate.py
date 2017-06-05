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

    db['cursor'].execute('SELECT DISTINCT Company FROM CompanyScoreV6;')
    companies = db['cursor'].fetchall()
    y = 5  # If year is 2005. Patents are worth something until 2010
    years = y + 1

    for company in companies:
        db['cursor'].execute(
            "SELECT * FROM CompanyScoreV7 WHERE Company='%s' ORDER BY Year;" % str(company[0]))
        companyScores = db['cursor'].fetchall()

        startYear = int(companyScores[0][1])
        endYear = int(companyScores[len(companyScores) - 1][1])

        companyID = companyScores[0][0]
        newScores = []

        for i, year in enumerate(range(startYear, endYear + 1)):
            newScores.append({
                'Company': companyID,
                'Year': year,
                'CompanyPatents': 0,
                'CompanyStarPatents': 0,
                'Inventors': 0,
                'StarInventors': 0,
                'Patents': 0,
                'Companies': 0,
                'Industries': 0,
                'StarPatents': 0,
                'PatentClasses': 0,
                'Included': '',
                'PrevCompanyPatents': 0,
                'PrevCompanyStarPatents': 0,
                'PrevInventors': 0,
                'PrevStarInventors': 0,
                'PrevPatents': 0,
                'PrevCompanies': 0,
                'PrevIndustries': 0,
                'PrevStarPatents': 0,
                'PrevPatentClasses': 0
            })

        for i, year in enumerate(range(startYear, endYear + 1)):

            included = ""
            CompanyPatents = 0
            CompanyStarPatents = 0
            Inventors = 0
            StarInventors = 0
            Patents = 0
            Companies = 0
            Industries = 0
            StarPatents = 0
            PatentClasses = 0

            if int(companyScores[0][1]) == year:
                CompanyPatents = companyScores[0][2]
                CompanyStarPatents = companyScores[0][3]
                Inventors = companyScores[0][4]
                StarInventors = companyScores[0][5]
                Patents = companyScores[0][6]
                Companies = companyScores[0][7]
                Industries = companyScores[0][8]
                StarPatents = companyScores[0][9]
                PatentClasses = companyScores[0][10]
                companyScores = companyScores[1:]

            newScores[i]['CompanyPatents'] = CompanyPatents
            newScores[i]['CompanyStarPatents'] = CompanyStarPatents
            newScores[i]['Inventors'] = Inventors
            newScores[i]['StarInventors'] = StarInventors
            newScores[i]['Patents'] = Patents
            newScores[i]['Companies'] = Companies
            newScores[i]['Industries'] = Industries
            newScores[i]['StarPatents'] = StarPatents
            newScores[i]['PatentClasses'] = PatentClasses

            for j in range(1, years):
                if (i + j) < len(newScores):
                    newScores[i + j]['PrevCompanyPatents'] += CompanyPatents
                    newScores[i + j]['PrevCompanyStarPatents'] += CompanyStarPatents
                    newScores[i + j]['PrevInventors'] += Inventors
                    newScores[i + j]['PrevStarInventors'] += StarInventors
                    newScores[i + j]['PrevPatents'] += Patents
                    newScores[i + j]['PrevCompanies'] += Companies
                    newScores[i + j]['PrevIndustries'] += Industries
                    newScores[i + j]['PrevStarPatents'] += StarPatents
                    newScores[i + j]['PrevPatentClasses'] += PatentClasses
                    newScores[i + j]['Included'] += str(year) + ' '

        finalScores = []
        print "\n\n####%s####\n" % companyID
        for newScore in newScores:
            finalScores.append({
                'Company': companyID,
                'Year': newScore['Year'],
                'Included': newScore['Included'],
                'CompanyPatents': newScore['CompanyPatents'] + newScore['PrevCompanyPatents'],
                'CompanyStarPatents': newScore['CompanyStarPatents'] + newScore['PrevCompanyStarPatents'],
                'Inventors': newScore['Inventors'] + newScore['PrevInventors'],
                'StarInventors': newScore['StarInventors'] + newScore['PrevStarInventors'],
                'Patents': newScore['Patents'] + newScore['PrevPatents'],
                'Companies': newScore['Companies'] + newScore['PrevCompanies'],
                'Industries': newScore['Industries'] + newScore['PrevIndustries'],
                'StarPatents': newScore['StarPatents'] + newScore['PrevStarPatents'],
                'PatentClasses': newScore['PatentClasses'] + newScore['PrevPatentClasses']
            })

        insertQuery = "INSERT IGNORE INTO "
        insertQuery += "AggregateScore%dyV5 " % y
        insertQuery += "(Company, "
        insertQuery += "Year, "
        insertQuery += "Included, "
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

        for finalScore in finalScores:
            insertQuery += "('%s',%d,'%s',%d,%d,%d,%d,%d,%d,%d,%d,%d),\n" % (finalScore['Company'], finalScore['Year'], finalScore['Included'], finalScore['CompanyPatents'], finalScore['CompanyStarPatents'], finalScore[
                'Inventors'], finalScore['StarInventors'], finalScore['Patents'], finalScore['Companies'], finalScore['Industries'], finalScore['StarPatents'], finalScore['PatentClasses'])

        insertQuery = insertQuery[:-2] + ";"
        try:
            db['cursor'].execute(insertQuery)
            db['database'].commit()
        except:
            print insertQuery
            sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
