//---------------------------------------------------------------------
// get_school.js
//
// Desc  :  Takes a command line argument which is the filename prefix. File contains plain text lines of the following format:
// 70897|Jim Bledsoe Jackson Electronics
// personID|name company
// then does a goolge search on the 'person company' and extracts school names from LinkedIn search results
// personID and school names are written to schools.txt
// schools.txt is opened and closed each time a write occurs so if this code fails schools.txt is appended to.
// Requires headless browser PhantomJS and CasperJS to be installed.
// For more than 150 searches should be called from a shell script with multiple split input file to reinitialize PhantomJS/CasperJS as they have a memory leak 
// which causes a heap overflow after a certain number of web page openings.
// of the form containing IDs and LinkedIn URLs.  Captures
//
// Author:  John Correa
// Date  :  Dec 2015
//---------------------------------------------------------------------

// Initializations and Setup
//-------------------------------------------------------------------------

var fs = require('fs');
var step = 0;
var retry = 0;
var idcount = 0;
var lastschool = "";
var school = "";
var file_id;
var url = ""

var casper = require("casper").create ({
    waitTimeout: 25000,
    stepTimeout: 50000,
    verbose: false,
//    verbose: true,
//    logLevel: 'debug',
    viewportSize: {
        width: 1400,
        height: 768
    },
    onWaitTimeout: function() {
        logConsole('Wait TimeOut Occured');
        //this.capture('xWait_timeout.png');
        this.exit();
    },
    onStepTimeout: function(self,m) {
        this.echo('Step TimeOut: ' + step + ", " + idcount + ", " + m);

        if (step == 5) {
            this.echo('Skip');
        }
        else {
      	    this.exit();
        }
    }
});

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4');

// Evaluating Command Line Arguments
if(casper.cli.has(0)) {
  file_id = casper.cli.get(0);
  console.log("command arg " + file_id);
}

// Error Handling
//-------------------------------------------------------------------------

// http://docs.casperjs.org/en/latest/events-filters.html#page-error
casper.on("page.error", function(msg, trace) {
  //this.echo("Error: " + msg);
  });

// http://docs.casperjs.org/en/latest/events-filters.html#page-initialized
casper.on("page.initialized", function(page) {
    // CasperJS doesn't provide `onResourceTimeout`, so it must be set through 
    // the PhantomJS means. This is only possible when the page is initialized
    page.onResourceTimeout = function(request) {
      console.log('Response Timeout (#' + request.id + '): ' + JSON.stringify(request));
    };
  });

casper.on('remote.message', function(msg) {
    //this.echo('***remote message caught***: ' + msg);
});

// Starting Casper Actions
//-------------------------------------------------------------------------

casper.start();

//urls to read
var file_h = fs.open(file_id + '.txt', 'r');
//var file_h = fs.open('C:/temp/linktest.txt', 'r');

//read urls to search
var maxlines = 20000;
var skip = 0;
var count=0;
var LineArray=new Array();
line = file_h.readLine(); 
console.log("reading " + skip + " to " + maxlines + "...");   

while(line && count<maxlines) {
    count = count + 1;
    if (count > skip) {
       LineArray.push(line);
    }
    line = file_h.readLine(); 
}
file_h.close();

//for each line in the input file  
    LineArray.forEach(function(LineArrayValue){

    console.log(LineArrayValue.split("|")[0].trim());

    step = 1;
    casper.thenOpen('http://www.google.com', function() {
            this.echo("searching...");
    });

    // fill in search form with person and company
    casper.then(function() {
    step = 2;
    this.echo(this.getCurrentUrl()); 

    this.waitUntilVisible("form[id='tsf']", 
        function sucess() {
        this.echo('google loaded...');
        this.fill("form[id='tsf']", {'q': LineArrayValue.split("|")[1].trim()}, true);
        },
        function failure() {
        this.echo("google didn't load...");
        },
        10000
    );

    });

    // get linked in search result
    casper.then(function() {
    step = 3;
    this.echo(this.getCurrentUrl()); 

    this.waitUntilVisible('a[href^="https://www.linkedin.com"]', 
        function sucess() {
        this.echo('found person...');
        url = this.getCurrentUrl();
        var element = this.getElementInfo('a[href^="https://www.linkedin.com"]');
        this.echo(element.text);
        this.clickLabel(element.text, 'a');
        },
        function failure() {
        this.echo("didn't find person...");
        url = "";
        },
        10000
    );
    });

    // check if the school exists
    casper.then(function() {
    //this.echo(this.getCurrentUrl()); 
    step = 4;

    if (this.exists(('a[href^="https://www.linkedin.com/edu"]'))) {
        this.echo('found school...');

           lastschool = "";
           casper.each(this.getElementsInfo('a[href^="https://www.linkedin.com/edu"]'), function(casper, element, j) {
               school = element.text;
               if ((school.length > 0) && (school != lastschool)) {
                  this.echo(school);
                  var f = fs.open("schools.txt", "a+");
                  f.write(LineArrayValue.split("|")[0].trim());
                  f.write("| ");
                  f.write(school);
                  f.write("\r\n");
                  f.close();
                  lastschool=school;
               }
           });
        }
    });

});

casper.run();

console.log('loop complete');








