<?php

$raw = $_GET['term'];

$formatted = htmlspecialchars($raw, ENT_QUOTES, 'utf-8'); # Probably not necessary


# Only suggest based on last word
$as_array = explode(" ", trim($formatted)); 

$recent = "";

if(count($as_array) == 1){
	$recent = $as_array[0];
}
else{
	$prev = $as_array[0];
	$recent = $as_array[1];
}

$lookup = "http://localhost:8983/solr/myexample/suggest?q=".$recent;

$results = file_get_contents($lookup);

# Fix format
$decode = json_decode($results);

$recs = array();

$suggestions = $decode->suggest->suggest->$recent->suggestions;

foreach ($suggestions as $key => $value) {
	array_push($recs, $prev . " " . $suggestions[$key]->term);
	
}

echo json_encode($recs);
?>