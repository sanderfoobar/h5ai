<?
include("config.php");
include("functions.php");
?>
<!DOCTYPE html><!--[if lt IE 9]><html class="no-js oldie" lang="en"><![endif]--><!--[if gt IE 8]><!--><html lang="en"><!--<![endif]-->
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<title>Search Repository</title>
	<meta name="description" content="w00t"><meta name="viewport" content="width=device-width">
	<link rel="shortcut icon" href="/_h5ai/client/images/app-16x16.ico">
	<link rel="stylesheet" href="//fonts.googleapis.com/css?family=Ubuntu+Mono:400,700,400italic,700italic|Ubuntu:400,700,400italic,700italic">
	<link rel="stylesheet" href="searchstyles.css">
	<script src="/_h5ai/client/js/scripts.js" data-mode="php"></script>
	<body bgcolor="#0c0c0c">
</head>
</style>
<body id="h5ai-main"><div id="topbar" class="clearfix"><ul id="navbar"></ul></div><div id="content"><pre><center><br><form action="<?=$rootpath?>" method="get"><input name="q" type="text" style="outline:0; border: 3px solid  #00bb00; border-radius: 5px;-moz-border-radius:5px; border-color: #00bb00; background-color: #00bb00; padding-left: 5px" value="Do _NOT_ share :) Type here to search..." size="55" size="12" maxlength="120" onfocus="if(!this._haschanged){this.value=''};this._haschanged=true;"></pre></center>
</form><form method="get"><input type="hidden" value="True" name="time">
<select name="q" id="datetime" onchange="this.form.submit()">
<option value="">Select date</option>
</select>
</form>
<script>
var select = document.getElementById("datetime");
var curDate = Math.round(+new Date() / 1000);
select.options[select.options.length] = new Option('1 day ago', curDate - 86400);
select.options[select.options.length] = new Option('7 days ago', curDate - (7*86400)); 
</script>
<?php 

function startsWith($haystack, $needle)
{
    return !strncmp($haystack, $needle, strlen($needle));
}

$search = $_GET['q'];

if(isset($search)){
	//limit
	$ip=$_SERVER['REMOTE_ADDR'];
	$whitelisted = False;
	$output = null;

	foreach($whitelist as $white){
		if(startsWith($ip, $white)){
			$whitelisted = True;
		}
	}

	if($whitelisted){
		if ($_GET['time']) exec('/usr/bin/python py/searcher.py -a -j -t ' . escapeshellarg($search), $output);
		else exec('/usr/bin/python py/searcher.py -a -j ' . escapeshellarg($search), $output);
	}
	else{
		exec('/usr/bin/python py/searcher.py -l -j ' . escapeshellarg($search), $output);
	}
    $output = implode('',$output);
    $json = json_decode($output);

	echo '<div id="extended" class="clearfix view-details" style="display:block;">';
	echo '<ul>';
	echo '<li class="header"><a class="icon"></a>';
	echo '<a class="label ascending" href="#">';
	echo '<span class="l10n-name">Name</span>';
	echo '</a>';
	echo '<a class="date" href="#">';
	echo '<img src="/_h5ai/client/images/descending.png" class="sort descending" alt="descending" />';
	echo '<img src="/_h5ai/client/images/ascending.png" class="sort ascending" alt="ascending" />';
	echo '<span class="l10n-lastModified">Section</span>';
	echo '</a>';
	echo '<a class="size" href="#">';
	echo '<img src="/_h5ai/client/images/descending.png" class="sort descending" alt="descending" />';
	echo '<img src="/_h5ai/client/images/ascending.png" class="sort ascending" alt="ascending" />';
	echo '<span class="l10n-size">URL</span>';
	echo '</a>';

    if (sizeof($json) == 0) die("<center><h4>No results or malformed input.</h4></center>");

	    foreach($json as $data){
		    $name = $data->name;
		    $host = replace_url($data->host);
		    $section = $data->section;
		    $url = replace_url($data->url);
		    $imdb = $data->imdb;
		    echo '</a><li class="entry folder"><a class="" href="'.$url.'"><span class="icon small"><img src="/_h5ai/client/icons/16x16/folder.png" /></span></span><span class="label">'. $name .'</span><span class="date">'.$section.'</span><span class="size">'.$host.'</span></a></li>';
	    }
    }
    else{
	    echo "<center>Try searching something.</center>";
    }
?>
</ul>
</font>
</body>
