LOAD DATA INFILE '/var/lib/mysql-files/companies.csv' 
INTO TABLE patents.companies
FIELDS TERMINATED BY ';:;'
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Name, CompanyId, @NACE)
SET NACE = IF(@NACE='None',NULL,@NACE);