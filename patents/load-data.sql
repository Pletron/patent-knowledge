LOAD DATA INFILE '/var/lib/mysql-files/patents.csv' 
INTO TABLE patents.patents
FIELDS TERMINATED BY ';:;'
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(PatId, PubYear, CompanyId, Firstname, Lastname, Country);