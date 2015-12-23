package com.charitablenetwork.BuildFile;

import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

import java.io.File; 
import java.io.IOException; 
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;

/*
#---------------------------------------------------------------------
# BuildFile.java
#
# Desc  :  Reads 'all_companies.csv' and 'all_people.csv' and writes 'linkedin#.txt' files
#          for each 200 names to search 'person company' with get_school.js. 
#          Drops middle initials and munges names to get better google search results.
#
# Author:  John Correa
# Date  :  Dec 2015
#---------------------------------------------------------------------
 */
public class BuildFile
{

    public static void main( String[] args ) throws Exception
    {   	
     	//build hash map of company ids-names
    	/************************************************************************************/
       	Map<String, String> companies = new HashMap<String, String>();

    	String csvFile = "C:/temp/all_companies.csv";
    	BufferedReader br = null;
    	String line = "";
    	String cvsSplitBy = "\\|";

    	String csvWriteFile = "C:/users/jcorrea/linkedin0.txt";
    	BufferedWriter output = null;
    	
    	try {
            File file = new File(csvWriteFile);
            output = new BufferedWriter(new FileWriter(file));
   	
    	try {

    		br = new BufferedReader(new FileReader(csvFile));
    		line = br.readLine(); // ignore first line;
    		while ((line = br.readLine()) != null) {
    			//System.out.println(line);
    			
    		    // use '|' as separator
    			String[] tokens = line.split(cvsSplitBy);

    			System.out.println("Company id= " + strip(tokens[0])+ " , name=" + strip(tokens[1])); 	
    			companies.put(strip(tokens[0]), strip(tokens[1]));

    		}

    	} catch (FileNotFoundException e) {
    		e.printStackTrace();
    	} catch (IOException e) {
    		e.printStackTrace();
    	} finally {
    		if (br != null) {
    			try {
    				br.close();
    			} catch (IOException e) {
    				e.printStackTrace();
    			}
    		}
    	}

    	System.out.println("Done");
    	
    	//get list of people and company names
    	/**********************************************************************************************/
    	ArrayList<String[]> PeopleCompany = new ArrayList<String[]>() ;
 
    	csvFile = "C:/temp/all_people.csv";

    	try {

    		br = new BufferedReader(new FileReader(csvFile));
    		line = br.readLine(); // ignore first line;
    		while ((line = br.readLine()) != null) {
    			
    		    // use '|' as separator
    			String[] tokens = line.split(cvsSplitBy);

    			String[] PersonCompany = new String[3];
    			PersonCompany[0] = strip(tokens[2]);
    			PersonCompany[1] = companies.get(strip(tokens[0]));
    			PersonCompany[2] = strip(tokens[1]);
    			PeopleCompany.add(PersonCompany);
    			
    			System.out.println("Person = " + PersonCompany[0] + " , Company = " + PersonCompany[1]); 			   			
    		}

    	} catch (FileNotFoundException e) {
    		e.printStackTrace();
    	} catch (IOException e) {
    		e.printStackTrace();
    	} finally {
    		if (br != null) {
    			try {
    				br.close();
    			} catch (IOException e) {
    				e.printStackTrace();
    			}
    		}
    	}
   	
    	//for each person company
    	/***************************************************************************************************/
    	int count = 0;
    	int lastcount = 0;
    	cvsSplitBy = " ";
    	for (String temp[] : PeopleCompany) {
		    String searchString;
		    
		    // use ' ' as separator, remove middle initial
    		
			String[] names = temp[0].split(cvsSplitBy);
			String company = temp[1]; 
			
			//skip middle name, gives better search results
            searchString = "";
    		if (names.length == 1) {
    			searchString = names[0] + " " + company;
    		}
        	else if (names.length == 2) {
    			searchString = names[0] + " " + names[1] + " " + company;
        	}
        	else if (names.length == 3) {
        		//skip middle initial
    			searchString = names[0] + " " + names[2] + " " + company;
        	}
    		else 
    			searchString = temp[0] + " " + company;
    		
    	
            output.write(temp[2]);
    		output.write("|");
            output.write(searchString);
            output.newLine();

        	count++;

    		System.out.println(temp[2] + " " + searchString);
    		
    		if (count/200 != lastcount/200) {
    			if ( output != null ) output.close();
        		System.out.println("***************************************** " + count + " " + lastcount + " " + csvWriteFile);
            	csvWriteFile = "C:/users/jcorrea/linkedin" + count/200 + ".txt";
                file = new File(csvWriteFile);
                output = new BufferedWriter(new FileWriter(file));
                lastcount = count;
    		}
    	}
   	
        } catch ( IOException e ) {
            e.printStackTrace();
        } finally {
            if ( output != null ) output.close();
        }
    	
    	}

    private static void print(String msg, Object... args) {
        System.out.println(String.format(msg, args));
    }

    private static String trim(String s, int width) {
        if (s.length() > width)
            return s.substring(0, width-1) + ".";
        else
            return s;
    }

    private static String strip(String str)
    {
        if (str.startsWith("\""))
        {
            str = str.substring(1, str.length());
        }
        if (str.endsWith("\""))
        {
            str = str.substring(0, str.length() - 1);
        }
        return str;
    }

}





