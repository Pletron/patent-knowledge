CREATE TABLE patents (
  PatId varchar(255) NOT NULL,
  PubYear varchar(255) NULL,
  CompanyId varchar(255) NULL,
  Firstname varchar(255) NULL,
  Lastname varchar(255) NULL,
  Country varchar(255) NULL,
  PRIMARY KEY(PatId),
  FOREIGN KEY(CompanyId),
  FOREIGN KEY(Firstname, Country)
) ENGINE=InnoDB CHARSET=utf8;