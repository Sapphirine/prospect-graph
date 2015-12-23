//---------------------------------------------------------------------------------------
// create_grads.cypher
//
// Desc: creates grads relationships
// Author:  John Correa
// Date  :  Dec 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_grads.cypher > $BDA_DEV/DATA/grad_results.txt
//---------------------------------------------------------------------------------------
export INFILE="file:/home/Columbia/DATA/all_grads.csv"

LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
MATCH (p:Person {personID: TOINT(row.personID)}), (s:School {schoolID: TOINT(row.schoolid)})
MERGE (p)-[:GRAD]-(s);