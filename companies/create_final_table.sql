DROP TABLE `FinalTableV13`;
CREATE TABLE `FinalTableV13` (
	`Company` varchar(55) NOT NULL DEFAULT '0',
	`Year` year(4) NOT NULL DEFAULT '2000',
	`Industry` varchar(55) DEFAULT NULL,
	`Country` varchar(55) DEFAULT NULL,
	`Market_Age` int(11) DEFAULT NULL,
	`Company_Age` int(11) DEFAULT NULL,
	`Company_Patents` int(11) DEFAULT '0',
	`Company_Star_Patents` int(11) DEFAULT '0',
	`Inventors` int(11) DEFAULT '0',
	`Star_Inventors` int(11) DEFAULT '0',
	`Experience` int(11) DEFAULT '0',
	`Company_Diversity` int(11) DEFAULT '0',
	`Industry_Diversity` int(11) DEFAULT '0',
	`Experience_Quality` int(11) DEFAULT '0',
	`Technological_Diversity` int(11) DEFAULT '0',
	`Total_Assets` decimal(55,4) DEFAULT NULL,
	`Number_of_Employees` bigint(55) DEFAULT NULL,
	`Operating_Revenue` decimal(55,4) DEFAULT NULL,
	`Research_and_Development_Intensity` decimal(55,4) DEFAULT NULL,
	`Research_and_Development_Expenses` decimal(55,4) DEFAULT NULL,
	`EBITDA` decimal(55,4) DEFAULT NULL,
	`Profit_Margin` decimal(20,4) DEFAULT NULL,
	`Market_Capital` decimal(20,2) DEFAULT NULL,
	`Included` varchar(55) DEFAULT NULL,
	PRIMARY KEY (`Company`,`Year`),
	CONSTRAINT `finaltablev13_ibfk_1` FOREIGN KEY (`Company`) REFERENCES `Companies` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO
	FinalTableV13
SELECT
	cs.Company,
	cs.Year,
	Industry,
	Country,
	IF(cs.Year<IPOYear,NULL,cs.Year-IPOYear) AS Market_Age,
	IF(cs.Year<IncorporationYear,NULL,cs.Year-IncorporationYear) AS Company_Age,
	CompanyPatents,
	CompanyStarPatents,
	Inventors,
	StarInventors,
	Patents,
	Companies,
	Industries,
	StarPatents,
	PatentClasses,
	Total_assets/1000,
	Number_of_employees,
	Operating_revenue/1000,
	(Research_and_Development_Expenses*-1)/Operating_revenue,
	(Research_and_Development_Expenses*-1)/1000,
	EBITDA/1000,
	Profit_margin,
	Market_capitalisation_m_USD,
	Included
FROM
	AggregateScore5yV5 AS cs
JOIN
	Companies AS c ON c.ID=cs.Company
INNER JOIN
	CompanyPerformanceV2 AS cp ON cs.Company=cp.Company AND cs.Year=cp.Year;