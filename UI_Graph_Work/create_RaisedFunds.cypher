//---------------------------------------------------------------------------------------
// create_PeopleRoles.cypher
//
// Desc: creates relationships from Companies to RaisedFunds
// Author:  Sam Guleff
// Date  :  Dec 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_roles.cypher > $BDA_DEV/DATA/all_CompanyRaisedFunds.txt
//---------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/all_CompanyRaisedFunds.txt'
export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_CompanyRaisedFunds.txt

LOAD CSV WITH HEADERS 
FROM 'https://raw.githubusercontent.com/jcp1016/bda-team-project/master/UI_Graph_Work/all_CompanyRaisedFunds.txt' AS row 
FIELDTERMINATOR "|"
MATCH (p:Company {Name: row.Name}), (r:RaisedFunds {Name: row.RaisedFunds})
MERGE (p)-[:FUNDS_RAISED]->(r);

MATCH (p:Company)-[r:FUNDS_RAISED]->(c:RaisedFunds)
RETURN p.Name, r, c.Name LIMIT 5;
