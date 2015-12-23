//---------------------------------------------------------------------------------------
// create_roles.cypher
//
// Desc: creates relationships from People to Company 
// Author:  Janet Prumachuk
// Date  :  Nov 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_roles.cypher > $BDA_DEV/DATA/role_results.txt
//---------------------------------------------------------------------------------------
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_roles.csv"

LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
MATCH (p:Person {personID: row.personID}), (c:Company {companyID: TOINT(row.companyID)})
MERGE (p)-[:HAS_ROLE {roleType: row.Role}]->(c);

MATCH (p:Person)-[r:HAS_ROLE]->(c:Company)
RETURN p.Name, r, c.Name LIMIT 5;
