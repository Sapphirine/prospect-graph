//----------------------------------------------------------------------------------------------
// create_companies.cypher
//
// Desc: creates nodes with label Company
// Author:  Janet Prumachuk
// Date  :  Nov 2015
// 
// To run this from the bash shell go to $NEO4J_HOME:        
// ./bin/neo4j-shell -file $BDA_DEV/create_companies.cypher > $BDA_DEV/DATA/company_results.txt 
//----------------------------------------------------------------------------------------------
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_companies.csv"

MATCH (p:People)  DETACH DELETE p;
MATCH (c:Company) DETACH DELETE c;

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
CREATE (:Company {companyID: TOINT(row.ID),
                  Name: row.Name,
                  logoURL: row.logoURL,
                  thumbURL: row.thumbURL,
                  dataQuality: TOINT(row.dataQuality),
                  highConcept: row.highConcept,
                  companyURL: row.companyURL,
                  crunchbaseURL: row.crunchbaseURL,
                  twitterURL: row.twitterURL,
                  linkedinURL: row.linkedinURL,
                  primaryLocation: row.primaryLocation,
                  companySize: row.companySize,
                  raisingAmount: TOINT(row.raisingAmount),
                  preMoneyValuation: TOINT(row.preMoneyValuation),
                  raisedAmount: TOINT(row.raisedAmount)});

DROP CONSTRAINT ON (c:Company) ASSERT c.companyID IS UNIQUE;

MATCH (c:Company)
RETURN c LIMIT 2;
