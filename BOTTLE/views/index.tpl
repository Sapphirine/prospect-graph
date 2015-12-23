<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; 
         any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Big Data Analytics Final Project</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/jumbotron.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
    <!-- Top navigation bar common to all pages -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" 
                  data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <span class="navbar-brand"><p>Mission Match</p></span>
        </div><!--/navbar-header -->
        <div id="navbar" class="navbar-collapse collapse">
          <!-- <form class="navbar-form navbar-right"> -->
          <ul class="nav navbar-nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="http://mission-match.mine.nu">Graph</a></li>
            <li><a href="#project">Project</a></li>
            <li><a href="#team">Team</a></li>
          </ul>
        </div><!-- end of navbar-collapse -->
      </div><!-- end of navbar container -->
    </nav>

    <!-- Graphical area at top of home page, includes the input form -->
    <div class="jumbotron">
      <div class="container">
        <div class="page-header"> 
          <div id="tagline">
            Find angels who care about your organization's mission.
          </div>
          <form class="search" action="/" role="form" id="get_org_form" method="post">
            <div class="input-group input-group-lg">
              <span class="input-group-addon">http://www.</span>
              <input type="text" name="orgname" class="form-control input-lg" 
                     placeholder="orgname" autofocus value={{orgname}} >
              <span class="input-group-addon">.org</span>
            </div> <!-- end of input group -->
            <br class="clear" />
            <button type="submit" class="btn btn-info btn-lg center-block">Search</button>&nbsp;
          </form>
        </div><!-- end of page-header -->
        <div id="keywords">
          %keys = ', '.join(str(k) for k in keywords)
          %if len(keywords) > 12:
              <p> Keywords: <br class="clear" />{{keys}} </p>
          %elif len(keywords) > 1:
              <p> Keywords: {{keys}} </p>
          %else:
              <p> {{keys}} </p>
          %end
        </div>
      </div><!-- end of jumbotron container -->
    </div><!-- end of jumbotron -->

    <!-- Data output area -->
    <!-- Load elements into a 2 dimenstional list -->
    %matrix = ([])
    %if data != '' and data[0:6] != 'Please' and data[0:5] != 'Sorry':
        %for row in data:
            %matrix.append(row)
        %end
    %end

    <div class="container">
    <!-- Each row will display 3 people -->
    %j = 0
    <div class="row">
    %for row in matrix:
        %if j % 3  == 0 : 
            </div> <!-- end of row -->
            <div class="row">
        %end
        <div class="col-md-4">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <b>{{row[0]}} <br class="clear" /></b>
                </div>
                <div class="panel-body">
                    <p>{{row[1]}}</p>
                    <p><a href={{row[8]}} target="_blank">LinkedIn Profile</a></p>
                </div>
                <div class="table-responsive">
                    <table class="table table-bordered table-condensed">
                        <tr>
                          <td>{{row[2]}} at <a href={{row[6]}} target="_blank">{{row[3]}}</a></td>
                        </tr>
                        <tr>
                          <th>Company Size</th>
                          <td>{{row[5]}}</td>
                        </tr>
                          <th>Funds Raised</th>
                          %raised = "$" + str( format(row[4], ',d') )
                          <td>{{raised}}</td>
                        </tr>
                    </table>
                </div>
            </div> <!-- end of panel -->
            <!-- <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p> -->
        </div> <!-- end of column -->
        %j += 1
    %end
    </div> <!-- end of last row -->
    </div> <!-- end of data output area container -->
    <hr>

    <!-- Static footer -->
    <div class="container">
      <footer><p>&copy; 2015 Corlefnet</p></footer>
    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript
      ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script>
      window.jQuery || document.write('<script src="js/vendor/jquery.min.js"><\/script>')
    </script>
    <script src="js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="http://github.com/twbs/bootstrap/blob/master/docs/assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
