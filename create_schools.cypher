//---------------------------------------------------------------------------------------
// create_schools.cypher
//
// Desc: creates schools
// Author:  John Correa
// Date  :  Dec 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_schools.cypher > $BDA_DEV/DATA/school_results.txt
//---------------------------------------------------------------------------------------
export INFILE="file:/home/Columbia/DATA/all_schools.csv"

MATCH (s:School)
DETACH DELETE s;

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
CREATE (s:School {schoolID: row.schoolid,
                  Name: row.schoolname});

MATCH (s:School)
RETURN count(s);
