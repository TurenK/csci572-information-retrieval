<?php

// make sure browsers see this page as utf-8 encoded HTML
header('Content-Type: text/html; charset=utf-8');

$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;

$f_to_u = array();
$lines = file("URLtoHTML_nytimes_news.csv");	// Get rid of the header

foreach ($lines as $line) {
	$key_and_val = explode(",", $line);
	$f_to_u[$key_and_val[0]] = $key_and_val[1];
}

if ($query)
{

	// The Apache Solr Client library should be on the include path
	// which is usually most easily accomplished by placing in the
	// same directory as this script ( . or current directory is a default
	// php include path entry in the php.ini)
	require_once('./solr-php-client/Apache/Solr/Service.php');

	// create a new solr service instance - host, port, and corename
	// path (all defaults in this example)
	$solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample/');

	// if magic quotes is enabled then stripslashes will be needed
	// if (get_magic_quotes_gpc() == 1)
	// {
	// 	$query = stripslashes($query);
	// }

	// Select order to sort (Default: Lucene)
	$select = isset($_REQUEST['order'])? $_REQUEST['order'] : "default";

	// in production code you'll always want to use a try /catch for any
	// possible exceptions emitted by searching (i.e. connection
	// problems or a query parsing error)
	try
	{	
		if($select == "default")
		{
			$results = $solr->search($query, 0, $limit);
		}
		else
		{
			$results = $solr->search($query, 0, $limit, array('sort' => 'pageRankFile desc'));
		}
	
	}
	catch (Exception $e)
	{
		// in production you'd probably log or email this error to an admin
		// and then show a special message to the user but for this example
		// we're going to show the full exception
		die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
	}
}
?>

<html>
	<head>
	<title>HW4 - PHP Index</title>
	</head>
	<body>
		<form accept-charset="utf-8" method="get">
			<label for="q">Search:</label>
			<input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>
			<input type="submit"/>
			<label for="order">Whether use pagerank ordering:</label>
    		<input type="checkbox" id="order" name="order" value="pagerank" <?php if(isset($_REQUEST['order']) && $select == "pagerank") { echo 'checked="checked"';} ?>/>
		</form>

<?php
// display results
if ($results)
{
	$total = (int) $results->response->numFound;
	$start = min(1, $total);
	$end = min($limit, $total);
?>

<div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>
<ol>

<?php
	// iterate result documents
	foreach ($results->response->docs as $doc)
	{
		$title = $doc->title;
		$url = $doc->og_url;
		$id = $doc->id;
		$desc = $doc->og_description;

		if($desc == "" || $desc == null){
			$desc = "NA";
		}
		if($url == "" || $url == null){
			$url = $f_to_u[end(explode("/",$id))];
		}

	echo "<li>";
	echo "Title: <a href='$url' target='_blank'>$title</a></br>";
	echo "URL: <a href='$url' target='_blank'>$url</a></br>";
	echo "ID: $id</br>";
	echo "Description: $desc</br>";
	echo "</li>";

	}
?>

	</ol>

<?php
}
?>

	</body>
</html>