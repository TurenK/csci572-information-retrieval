package hw2;

import java.io.PrintWriter;
import java.util.logging.Level;
import java.util.logging.Logger;

import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class Controller {

	public static void main(String[] args) throws Exception {
		String crawlStorageFolder = "/data/crawl";
		int numberOfCrawlers = 7;
		int maxDepthOfCrawlong = 16;
		int maxPagesToFetch = 20000;
		int politenessDelay = 220;
		int maxOutgoingLinksToFollow = 100;
		String userAgentString = "Chrome/17.0.963.56 Safari/535.11";
		String seed = "https://www.wsj.com/";
		CrawlConfig config = new CrawlConfig();
		config.setCrawlStorageFolder(crawlStorageFolder);
		config.setMaxDepthOfCrawling(maxDepthOfCrawlong);
		config.setMaxPagesToFetch(maxPagesToFetch);
		config.setPolitenessDelay(politenessDelay); 
		config.setUserAgentString(userAgentString);
		config.setIncludeBinaryContentInCrawling(true);
		config.setMaxOutgoingLinksToFollow(maxOutgoingLinksToFollow);
		/*
		* Instantiate the controller for this crawl.
		*/
		PageFetcher pageFetcher = new PageFetcher(config);
		RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
		RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
		CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);
		/*
		* For each crawl, you need to add some seed urls. These are the first
		* URLs that are fetched and then the crawler starts following links
		* which are found in these pages
		*/
		controller.addSeed(seed);
		/*
		* Start the crawl. This is a blocking operation, meaning that your code
		* will reach the line after this only when crawling is finished.
		*/
		controller.start(MyCrawler.class, numberOfCrawlers);
		
		// Read threads data and output to file
		String task1 = "";
		String task2 = "";
		String task3 = "";
		
		for(Object t: controller.getCrawlersLocalData()) {
			String[] temp = (String []) t;
			task1 +=  temp[0];
			task2 +=  temp[1];
			task3 +=  temp[2];
		}
		
		PrintWriter p1 = new PrintWriter("fetch_wsj.csv");
		PrintWriter p2 = new PrintWriter("visit_wsj.csv");
		PrintWriter p3 = new PrintWriter("urls_wsj.csv");
		
		p1.println("URLs,HTTP/HTTPS Status Code");
		p1.println(task1.trim());
		p1.close();
		
		p2.println("URLs,File Size(Bytes),Number of Outlinks,Content Type");
		p2.println(task2.trim());
		p2.close();
		
		p3.println("URLs,Indicator");
		p3.println(task3.trim());
		p3.close();
	}
}
