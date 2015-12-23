//----------------------------------------------------------------------------------------------
// create_QueryNodes.cypher
//
// Desc: creates nodes which will add interconnectivity to the graph based on the following parameters
//         
// Author:  Sam Guleff
// Date  :  Nov 2015
// 
// To run this from the bash shell go to $NEO4J_HOME:        
// ./bin/neo4j-shell -file $BDA_DEV/create_companies.cypher  > $BDA_DEV/DATA/
//----------------------------------------------------------------------------------------------

export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_Roles.txt"

//----------------------------------------------------------------------------------------------
//Section for Roles connections
//----------------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/all_Roles.txt'
MATCH (r:Role)  DETACH DELETE r;

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM {INFILE + 'all_Roles.txt'} AS row 
FIELDTERMINATOR "|"
CREATE (:Role {RoleId: TOINT(row.RoleId),
                  Name: row.Name});

DROP CONSTRAINT ON (r:Role) ASSERT r.RoleID IS UNIQUE;


//----------------------------------------------------------------------------------------------
//Section for Twitter FollowerCount
//----------------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/all_Twitter.txt'
MATCH (f:FollowerCount) DETACH DELETE f;

USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS 
FROM {INFILE + 'all_Twitter.txt'} AS row 
FIELDTERMINATOR "|"
CREATE (:FollowerCount {twitterId: TOINT(row.twitterId),
                  Name: row.all_TwitterFollowers});
				  
DROP CONSTRAINT ON (r:FollowerCount) ASSERT r.twitterId IS UNIQUE;
				  		  