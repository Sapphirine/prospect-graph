//---------------------------------------------------------------------------------
// update_profiles.cypher
//
// Desc: adds profileURL property to Person
// Author:  Janet Prumachuk
// Date  :  Dec 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/src/update_profiles.cypher 
//    > $BDA_DEV/DATA/profile_results.txt
//--------------------------------------------------------------------------------
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_links.csv"

LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
MATCH (p:Person {personID: TOINT(row.personID)})
SET p.profileURL = row.profileURL;

MATCH (p:Person)
RETURN p LIMIT 20;
