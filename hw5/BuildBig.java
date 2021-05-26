import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.html.HtmlParser;
import org.apache.tika.sax.BodyContentHandler;

import org.xml.sax.SAXException;

public class BuildBig {	
	
	public void saveOutput(String out) {
		try{
			FileWriter layer_0 = new FileWriter("big.txt", true); 
			BufferedWriter layer_1 = new BufferedWriter(layer_0);
			PrintWriter layer_2 = new PrintWriter(layer_1);
			layer_2.println(out+"\n");
			layer_2.close();
		} catch (IOException e) {
			
		}
		
	}
	
	public String parseFile(File f) throws IOException,SAXException, TikaException {
	      BodyContentHandler handler = new BodyContentHandler();
	      Metadata metadata = new Metadata();
	      FileInputStream inputstream = new FileInputStream(f); //Was initially new File("/home/pradeep/Desktop/work.html")
	      ParseContext pcontext = new ParseContext();
	      
	      HtmlParser htmlparser = new HtmlParser();
	      htmlparser.parse(inputstream, handler, metadata, pcontext);
	      
	      return handler.toString();    
	}
	
	// Iterate thru the files
	public void runOnAll(String loc) throws IOException,SAXException, TikaException{
		File dir = new File(loc);
		
		File[] files = dir.listFiles();
		
		int count = 0;
		for(File f: files) {
			String toOut = parseFile(f);
			saveOutput(toOut);
			count += 1;
			System.out.println(count);
		}
	}
	
	public static void main(String [] args) throws IOException, SAXException, TikaException {
		BuildBig obj = new BuildBig();
		obj.runOnAll("/home/pradeep/Desktop/mercurynews");
   }
	
}