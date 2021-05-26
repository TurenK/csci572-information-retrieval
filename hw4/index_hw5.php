<html>

	<head>

<?php ini_set('memory_limit', -1); ?>

<?php



// make sure browsers see this page as utf-8 encoded HTML

header('Content-Type: text/html; charset=utf-8');



$limit = 10;

$query = isset($_REQUEST['search']) ? trim($_REQUEST['search']) : false;



$results = false;



$f_to_u = array();

$lines = file("URLtoHTML_nytimes_news.csv");	



foreach ($lines as $line) {

	$key_and_val = explode(",", $line);

	$f_to_u[$key_and_val[0]] = $key_and_val[1];

}



if ($query){

	

	// The Apache Solr Client library should be on the include path

	// which is usually most easily accomplished by placing in the

	// same directory as this script ( . or current directory is a default

	// php include path entry in the php.ini)

	require_once('./solr-php-client/Apache/Solr/Service.php');



	// create a new solr service instance - host, port, and corename

	// path (all defaults in this example)

	$solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample/');



	// if magic quotes is enabled then stripslashes will be needed

	// if (get_magic_quotes_gpc() == 1){

	//	$query = stripslashes($query);

	// }



	// in production code you'll always want to use a try /catch for any

	// possible exceptions emitted by searching (i.e. connection

	// problems or a query parsing error)

	try{	
		$select = isset($_REQUEST['order'])? $_REQUEST['order'] : "default";

		if($select == "default")
		{
			$results = $solr->search($query, 0, $limit);
		}
		else
		{
			$results = $solr->search($query, 0, $limit, array('sort' => 'pageRankFile desc'));
		}
	}

	catch (Exception $e){

		// in production you'd probably log or email this error to an admin

		// and then show a special message to the user but for this example

		// we're going to show the full exception

		die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");

	}

}

?>

	<meta charset = "utf-8">

	<title>HW5 - PHP naive search</title>

	<link href = "https://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css" rel = "stylesheet">

	<script src = "https://code.jquery.com/jquery-1.10.2.js"></script>

	<script src = "https://code.jquery.com/ui/1.10.4/jquery-ui.js"></script>

	<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css">

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

	<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>



	<script>

		$(function(){

            $( "#search" ).autocomplete({

               source: "autocomplete.php"

            });

		});

	</script>

	</head>

	<body>

		<div class = "ui-widget">

		<form accept-charset="utf-8" method="get">

			<label for="search">Search:</label>

			<input type="text" id="search" name="search" placeholder="please enter query" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>

			<input type="submit" value="SEARCH"/>
			<label for="order">Whether use pagerank ordering:</label>
    		<input type="checkbox" id="order" name="order" value="pagerank" <?php if(isset($_REQUEST['order']) && $select == "pagerank") { echo 'checked="checked"';} ?>/>

		</form>

		</div>

<?php



// Display results

if ($results){

	$total = (int) $results->response->numFound;

	$output = "";
	if($total < 1){
		include 'SpellCorrector.php';

		$splitted =  explode(" ", $query);

		foreach($splitted as $word){

			$corrected .= SpellCorrector::correct($word);

			if($word !== end($splitted)) {
				$corrected .= " ";
			}
		}
	}

	if(isset($corrected) & $corrected != $query){
		if($select == "default")
		{
			$results = $solr->search($corrected, 0, $limit);
		}
		else
		{
			$results = $solr->search($corrected, 0, $limit, array('sort' => 'pageRankFile desc'));
		}
		$total = (int) $results->response->numFound;
		$output .= "<div> Showing results for: <a href=http://localhost/index_hw5.php?search=" . $corrected .">" .$corrected."</a></div>";
		
		$output .= "<br>";
		
		$output .= "<div> Search instead for: <a href=http://localhost/index_hw5.php?search=" . $query .">" . $query ."</a></div>";

		$output .= "<br>";

	}

	if(isset($total) & $total == 0){

		$output .= "<div>No Results Found!</div>";

	}else{

		$start = min(1, $total);

		$end = min($limit, $total);



		$output .= "<div> Results ".$start." - ".$end." of ".$total.":</div>";

		$output .= "<ol>";





		// Iterate through documents

		foreach ($results->response->docs as $doc){

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



			$output .=  "<li>";

			$output .=  "Title: <a href=".$url." target='_blank'>".$title."</a></br>";

			$output .= 	"URL: <a href=".$url." target='_blank'>".$url."</a></br>";

			$output .= 	"Description: ".$desc."</br>";

			$output .= 	"ID: ".$id."</br>";

		}

		$output .= "</ol>";

	}

}

?>

<?php 
if (isset($output)){
	print("$output");
}?>

	</body>

</html>

