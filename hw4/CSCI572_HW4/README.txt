index.php is the file to create the web page that accepts the query, send the query to Solr and processes the Solr results to display. The PHP file uses 'solr-php-client' that the tutorial provided, so I did not include these files.

**Since I do not calculate overlaps by hand, cal_overlap.py is the file to connect Solr, run several queries and calculate overlaps.