package com.charitablenetwork.neorest;

import java.util.Collections;
import java.util.Iterator;
import java.util.Map;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.rest.graphdb.RestAPI;
import org.neo4j.rest.graphdb.RestAPIFacade;
import org.neo4j.rest.graphdb.RestGraphDatabase;
import org.neo4j.rest.graphdb.query.QueryEngine;
import org.neo4j.rest.graphdb.query.RestCypherQueryEngine;
import org.neo4j.rest.graphdb.util.QueryResult;
import static org.neo4j.helpers.collection.MapUtil.map;


import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.ClientResponse;

import java.io.File; 
import java.io.IOException; 
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;

import org.jsoup.Jsoup;
import org.jsoup.helper.Validate;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import static org.jsoup.Jsoup.parse;
import java.net.URL;

import com.gargoylesoftware.htmlunit.BrowserVersion;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.RefreshHandler;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlAnchor;
import com.gargoylesoftware.htmlunit.html.HtmlForm;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
import com.gargoylesoftware.htmlunit.html.HtmlTable;
import com.gargoylesoftware.htmlunit.html.HtmlTableRow;
import com.gargoylesoftware.htmlunit.util.WebConnectionWrapper;
import com.gargoylesoftware.htmlunit.WebResponse;
import com.gargoylesoftware.htmlunit.WebRequest;


/*
#---------------------------------------------------------------------
# neorest.java
#
# Desc  :  Test neo4j rest api.
#
# Author:  John Correa
# Date  :  Dec 2015 change
#---------------------------------------------------------------------
 */
public class neorest
{

    public static void main( String[] args ) throws Exception
    {   	
        WebResource resource = Client.create().resource( "http://104.43.162.60:7474/db/data/" );
        ClientResponse response = resource.get( ClientResponse.class );

        System.out.println( String.format( "GET on [%s], status code [%d]", "http://104.43.162.60:7474/db/data/", response.getStatus() ) );
        response.close();

        //QueryResult<Map<String,Object>> result = engine.query("MATCH (n:{label}) RETURN n", MapUtil.map("label", label));
        //System.out.println( "result" );
        //QueryResult<Map<String,Object>> result = engine.query("CREATE (n:Person { name : 'Andres', title : 'Developer' })", Collections.EMPTY_MAP);
        //System.out.println( "result" );

        
        //QueryResult<Map<String,Object>> result = engine.query("start n=node({id}) return n.name, id(n) as id", map("id", 0));


    	        RestAPI graphDb = new RestAPIFacade("http://104.43.162.60:7474/db/data/");

    	        QueryEngine<Map<String, Object>> engine=new RestCypherQueryEngine(graphDb);  
    	        QueryResult<Map<String,Object>> result = engine.query("start n=node(*) return count(n) as total", Collections.EMPTY_MAP);  

    	        Iterator<Map<String, Object>> iterator=result.iterator();  
    	        if(iterator.hasNext()) {  
    	          Map<String,Object> row= iterator.next();  
    	          System.out.println("Total nodes: " + row.get("total"));

    	        }
    	    	
    	        System.out.println( "Hello World!" );
    	}
}





