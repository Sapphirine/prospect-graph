//-----------------------------------------------------------------------------------------
// create_people.cypher
//
// Desc: creates nodes with label Person, and creates HAS_ROLE relationships
// Author:  Janet Prumachuk
// Date  :  Nov 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/merge_people.cypher > $BDA_DEV/DATA/people_results.txt
//-----------------------------------------------------------------------------------------
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_people.csv"

MATCH (p:Person)
DETACH DELETE p;

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
CREATE (p:Person {personID: row.personID,
                  Name: row.personName,
                  Bio: row.Bio,
                  followerCount: row.followerCount});

MATCH (p:Person)
RETURN count(p);
