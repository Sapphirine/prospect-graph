//---------------------------------------------------------------------------------------
// create_GeoLocationData.cypher
//
// Desc: creates relationships from People to Twitter Follower Bucket Nodes 
// Author:  Sam Guleff
// Date  :  Dec 2015
//
// To run this from the bash shell go to $NEO4J_HOME:
// ./bin/neo4j-shell -file $BDA_DEV/create_roles.cypher > $BDA_DEV/DATA/all_GeoLocation.txt
//---------------------------------------------------------------------------------------
//'file:///C:/Users/Sam/Desktop/Data/All_GeoLocation,txt'

export INFILE="file:/Users/janetprumachuk/dev/Python/Columbia/bda-dev/all_GeoLocation.txt"

LOAD CSV WITH HEADERS 
FROM "https://raw.githubusercontent.com/jcp1016/bda-team-project/master/UI_Graph_Work/test_GEOLOCATION.txt" AS row
FIELDTERMINATOR "|"
MATCH (p:Company {Name: row.Name})
SET p.LAT = toFloat(row.LAT)
SET p.LON = toFloat(row.LON)

MATCH (p:Person)-[r:TWITTER_FOLLOWERS]->(f:FollowerCount)
RETURN p.Name, r, f.Name LIMIT 500;
