INSERT INTO
	StarInventorsV2
SELECT
	Inventor,
	p.Class,
	MIN(AppDate) AppDate,
	COUNT(DISTINCT Patent) AS Patents
FROM
	Patents AS p
INNER JOIN
	PatentsInventors AS pi ON p.ID=pi.Patent
LEFT JOIN
	PatentClassCiting AS pcc ON p.Class=pcc.Class AND p.PubYear=pcc.Year
WHERE
	p.Citing>(pcc.AvgCiting+pcc.StdCiting*3)
GROUP BY
	Inventor,p.Class
ORDER BY
	Inventor, AppDate