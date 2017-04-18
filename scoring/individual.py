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


def getInventorScore(pHist, pcHist, iHist, cHist):
    startYear = int(min(pHist[0][1], pcHist[0][1], iHist[0][1], cHist[0][1]))
    endYear = int(max(pHist[-1][1], pcHist[-1][1], iHist[-1][1], cHist[-1][1]))

    inventorScore = {}
    for year in range(startYear, endYear + 1):
        inventorScore.update({
            str(year): {
                'Patents': 0,
                'Industries': 0,
                'Companies': 0,
                'PatentClassifications': 0
            }
        })

    for score in pHist:
        inventorScore[str(score[1])]['Patents'] = int(score[-1])
    for score in pcHist:
        inventorScore[str(score[1])]['PatentClassifications'] = int(score[-1])
    for score in iHist:
        inventorScore[str(score[1])]['Industries'] = int(score[-1])
    for score in cHist:
        inventorScore[str(score[1])]['Companies'] = int(score[-1])

    return inventorScore


def main(argv):
    db = connectToDB("patent_research")
    db['cursor'].execute("SET sql_mode=''")
    db['cursor'].execute("SELECT ID FROM Inventors")

    inventors = db['cursor'].fetchall()
    for i, inventor in enumerate(inventors):

        inventorID = inventor[0]

        db['cursor'].execute(
            "SELECT * " +
            "FROM InventorPatentsHist " +
            "WHERE Inventor='" + inventorID + "' " +
            "ORDER BY Year")
        pHist = db['cursor'].fetchall()
        db['cursor'].execute(
            "SELECT *, COUNT(PatentClass) as Classes " +
            "FROM InventorClassHist " +
            "WHERE Inventor='" + inventorID + "' " +
            "GROUP BY Year " +
            "ORDER BY Year ASC")
        pcHist = db['cursor'].fetchall()
        db['cursor'].execute(
            "SELECT Inventor, Year, " +
            "COUNT(Industry) as Industries FROM " +
            "(SELECT * " +
            "FROM InventorIndustryHist " +
            "WHERE Inventor='" + inventorID + "' " +
            "GROUP BY Industry " +
            "ORDER BY Year ASC) as a " +
            "GROUP BY Year ")
        iHist = db['cursor'].fetchall()
        db['cursor'].execute(
            "SELECT Inventor, Year, " +
            "COUNT(Company) as Companies FROM " +
            "(SELECT * " +
            "FROM InventorCompanyHist " +
            "WHERE Inventor='" + inventorID + "' " +
            "GROUP BY Company " +
            "ORDER BY Year ASC) as a " +
            "GROUP BY Year ")
        cHist = db['cursor'].fetchall()

        isEmpty = (len(pHist) + len(pcHist) + len(iHist) + len(cHist)) is 0
        scores = {}
        if not isEmpty:
            scores = getInventorScore(pHist, pcHist, iHist, cHist)

            query = "INSERT INTO InventorScore "
            query += "VALUES"
            for j, year in enumerate(scores):
                industries = scores[str(year)]['Industries']
                patents = scores[str(year)]['Patents']
                companies = scores[str(year)]['Companies']
                patentClassifications = scores[
                    str(year)]['PatentClassifications']

                query += "('" + inventorID + "',"
                query += str(year) + ","
                query += str(industries) + ","
                query += str(companies) + ","
                query += str(patentClassifications) + ","
                if j is not len(scores) - 1:
                    query += str(patents) + "),"
                else:
                    query += str(patents) + ");"

            db['cursor'].execute(query)
            db['database'].commit()

        progress = float(i) / len(inventors)
        sys.stdout.write('\rProgress: %s\tProcessed: %d' %
                         ("{:.0%}".format(progress), i))
        sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
