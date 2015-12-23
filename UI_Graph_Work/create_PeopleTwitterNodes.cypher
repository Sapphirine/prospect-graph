//---------------------------------------------------------------------------------------
// create_PeopleTwitterNodes.cypher
//
// Desc: creates relationships from People to Twitter Follower Bucket Nodes 
// Author:  Sam Guleff
// Date  :  Nov 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_roles.cypher > $BDA_DEV/DATA/All_PeopleTwitter.txt
//---------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/All_PeopleTwitter.txt'

export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/All_PeopleTwitter.txt"

LOAD CSV WITH HEADERS 
FROM {INFILE} AS row
FIELDTERMINATOR "|"
MATCH (p:Person {personID: row.personID}), (r:FollowerCount {Name: row.Twitter_Followers})
MERGE (p)-[:TWITTER_FOLLOWERS {roleType: row.Twitter_Followers}]->(r);

MATCH (p:Person)-[r:TWITTER_FOLLOWERS]->(f:FollowerCount)
RETURN p.Name, r, f.Name LIMIT 500;
