CREATE TABLE companies (
  Name varchar(255) NOT NULL,
  CompanyId varchar(255) NOT NULL,
  NACE varchar(255) NULL,
  PRIMARY KEY(CompanyId)
) ENGINE=InnoDB CHARSET=utf8;