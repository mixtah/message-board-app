%import Topics,Messages
%setdefault('page','home')
%setdefault('alert','')
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="A Simple Message Board">
	<meta name="author" content="Michael Bauer">
	<title>Message Board</title>
	<!-- CSS Styles -->
	<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<link href="https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.3/summernote.css" rel="stylesheet">
	<!-- Theme -->
	<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
	<link rel="stylesheet" type="text/css" href="/styles/style.css">
	<!-- JS Scripts -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
	<script src="/js/jquery.bootpag.min.js" type="text/javascript"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.3/summernote.js"></script>
	<script src="/js/general.js" type="text/javascript"></script>
</head>
<body>
<nav class="navbar navbar-default">
	<div class="container-fluid">
		<div class="navbar-header">
			<a class="navbar-brand" href="/">Message Board</a>
		</div>
		<ul class="nav navbar-nav">
			<li {{'class="active"' if page=='home' else ''}}><a href="/recent">Recent Topics</a></li>
			<li {{'class="active"' if page=='popular' else ''}}><a href="/popular">Popular</a></li>
			<li {{'class="active"' if page=='liked' else ''}}><a href="/liked">Most Liked</a></li>
			<li {{'class="active"' if page=='disliked' else ''}}><a href="/disliked">Most Disliked</a></li>
		</ul>
	</div>
</nav>

	<div class="container" style="margin-top:0px">
		
		%if len(alert)>0:
			<div class="alert alert-warning" role="alert">
			    <p align="center"><b>{{!alert}}</b></p>
			</div>
		%end
		
    	{{!base}}
    </div>

	<div class="container">
	    <footer>
	    	<br><br>
	        <h4 style="color:#656565;text-align: center;">Totals: {{Topics.getCount()}} Topics, {{Messages.getCount()}} Replies</h4>
	    </footer>
	</div>
</body>

</html>