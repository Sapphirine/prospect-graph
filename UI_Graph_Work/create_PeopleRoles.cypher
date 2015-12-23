//---------------------------------------------------------------------------------------
// create_PeopleRoles.cypher
//
// Desc: creates relationships from People to Roles Nodes 
// Author:  Sam Guleff
// Date  :  Nov 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_roles.cypher > $BDA_DEV/DATA/All_PeopleRoles.txt
//---------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/All_PeopleRoles_Test.txt'
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/All_PeopleRoles.txt"

LOAD CSV WITH HEADERS 
FROM 'https://raw.githubusercontent.com/jcp1016/bda-team-project/master/UI_Graph_Work/All_PeopleRoles.txt' AS row 
FIELDTERMINATOR "|"
MATCH (p:Person {personID: row.personID}), (r:Role {Name: row.Name})
MERGE (p)-[:EMPLOYEE_TYPE]->(r);

MATCH (p:Person)-[r:WORKS_AT]->(c:Company)
RETURN p.Name, r, c.Name LIMIT 5;
