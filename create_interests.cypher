//----------------------------------------------------------------------------------------------
// create_interests.cypher
//
// Desc:  Creates LIKES relationship from a Person to an Interest and inserts Interest node if
//        it does not already exist
//
// Author:  Janet Prumachuk
// Date  :  Nov 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_interests.cypher > $BDA_DEV/DATA/interest_results.txt
//----------------------------------------------------------------------------------------------
export NODE_FILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/interest_nodes.csv"
export EDGE_FILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_likes.csv"

MATCH (i:Interest)
DETACH DELETE i;

LOAD CSV WITH HEADERS
FROM {NODE_FILE} AS row
FIELDTERMINATOR "|"
CREATE (i:Interest {interestType: row.Interest})
RETURN i.interestType;

CREATE INDEX ON :Interest(interestType);

LOAD CSV WITH HEADERS 
FROM {EDGE_FILE} AS row
FIELDTERMINATOR "|"
MATCH (p:Person {personID: TOINT(row.personID)}), (i:Interest {interestType: row.Interest})
MERGE (p)-[:LIKES]->(i);

MATCH (p:Person)-[:LIKES]->(i:Interest)
RETURN p.Name, i.interestType LIMIT 20;
