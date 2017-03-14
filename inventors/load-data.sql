LOAD DATA INFILE '/var/lib/mysql-files/inventors.csv' 
INTO TABLE patents.inventors
FIELDS TERMINATED BY ','
ENCLOSED BY '\"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Firstname,Middlename,Lastname,Street,City,State,Country,Zipcode,Latitude,Longitude,InvSeq,Patent,@AppYear,@ApplyYear,PubYear,AppDate,Assignee,AsgNum,Class,Coauthor,Invnum,Invnum_N,Record_ID,Inventor_ID)
SET AppYear = IF(@AppYear='',2020,@AppYear), ApplyYear = IF(@ApplyYear='',2020,@ApplyYear);