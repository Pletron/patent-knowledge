LOAD DATA INFILE '/var/lib/mysql-files/companies_p1.csv' 
INTO TABLE patents.Companies
FIELDS TERMINATED BY ';:;'
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Name, ID, @Industry)
SET Industry = IF(@Industry='None',NULL,@Industry);

LOAD DATA INFILE '/var/lib/mysql-files/companies_p2.csv' 
INTO TABLE patents.Companies
FIELDS TERMINATED BY ';:;'
LINES TERMINATED BY '\n' 
(Name, ID, @Industry)
SET Industry = IF(@Industry='None',NULL,@Industry);


LOAD DATA INFILE '/var/lib/mysql-files/companies_p3.csv'
INTO TABLE patents.Companies
FIELDS TERMINATED BY ';:;'
LINES TERMINATED BY '\n' 
(Name, ID, @Industry)
SET Industry = IF(@Industry='None',NULL,@Industry);