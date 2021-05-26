package hw2;

import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpHead;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class MyCrawler extends WebCrawler {
	private final static String SEED_START = "^(https://|http://)?(www.)?(wsj.com|wsj.com/.*)$";
	private final static String SEED_END = ".*(\\.pdf|\\.doc.*|\\.htm(l)?|\\.jpg|\\.jpeg|\\.png|\\.gif)$";
	private String task1 = "";
	private String task2 = "";
	private String task3 = "";
//	private int attendNum = 0;
	private int visitNum = 0;
	
	public MyCrawler() {
		
	}
	
	// This is the method to get the data of threads
	@Override
	public Object getMyLocalData(){
		return new String[] {task1, task2, task3};
	}

	// This method contains task 3
	@Override
	public boolean shouldVisit(Page referringPage, WebURL url) {
//		attendNum++;
//		MyCrawler.logger.error("attend to visit: " + String.valueOf(attendNum));
		String urlStr = url.getURL();
		String href = urlStr.toLowerCase();
        
		// If not reside in the website
		if(!href.matches(SEED_START)){
			task3 += urlStr.replaceAll(",", "_") + ",N_OK\n";
			return false;
		}
		
		// else
		task3 += urlStr.replaceAll(",", "_") + ",OK\n";
		
		// get page type
		String typeStr = "";
		HttpHead head = null;
		try (CloseableHttpClient httpClient = HttpClientBuilder.create().build()) {
			 head = new HttpHead(urlStr);
			 HttpResponse response = httpClient.execute(head);
			 String contentType = response.containsHeader("Content-Type") ? response.getFirstHeader("Content-Type").getValue() : null;
			 typeStr = (contentType != null) ? contentType.toLowerCase() : "";
		} 
		catch (Exception e) {
			e.printStackTrace();
		}
		
		// check page type
		boolean typeCheck = typeStr.contains("html") | typeStr.contains("pdf") | typeStr.contains("doc") | typeStr.contains("gif") | typeStr.contains("jpeg") 
				| typeStr.contains("png") | typeStr.contains("jpg") | typeStr.contains("tif") | typeStr.contains("psd") | typeStr.contains("dng")
				| typeStr.contains("cr2") | typeStr.contains("nef") | href.matches(SEED_END);
//		if(typeCheck) {
//			MyCrawler.logger.error("should visit: " + url);
//		}else {
//			MyCrawler.logger.error("should not visit: " + url);
//		}
		return typeCheck;
	}
	
	// This method contains task 2
	@Override
	public void visit(Page page) {
		String url = page.getWebURL().getURL();
		visitNum++;
		MyCrawler.logger.error("visit num: " + String.valueOf(visitNum));
		MyCrawler.logger.error("visit page: " + url);
		int outGoingNum = 0;

		if (page.getParseData() instanceof HtmlParseData){ // Imagea may not have parse data
			HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
			Set<WebURL> links = htmlParseData.getOutgoingUrls();
			outGoingNum += links.size();
		}
		
		String contentType = page.getContentType().replace("; charset=utf-8", "").replace(";charset=utf-8", "").replace("; charset=UTF-8", "").replace(";charset=UTF-8", "");
		// Task 2 
		String temp = url.replace(",", "_") + "," + String.valueOf(page.getContentData().length) + "," + String.valueOf(outGoingNum) + "," + contentType + "\n";
		task2 += temp;
		MyCrawler.logger.error("task2: " + temp);
	}
	
	// This method contains task 1
	@Override
	protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
		task1 += webUrl.getURL().replace(",", "_") + "," + String.valueOf(statusCode) + "\n";
    }
}
