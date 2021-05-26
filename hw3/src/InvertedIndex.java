import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashMap;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndex {

	public static class Unigrams_Mapper extends Mapper<Object, Text, Text, Text> {
		/*
		 * Mapper do map calculations on each document
		 * It will write two columns to context for reducer to use
		 * Word  -  Doc-id
		 * There will be reputation
		 */
		
		private Text word = new Text(); // each word
		private Text docid = new Text(); // doc id

		// Key - not use in unigrams
		// Value - <word, doc id>
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

			// Get the id of the document -- first is the id, then others are contents
			String[] splitted = value.toString().split("\t", 2);

			// Each map utilizes one document, add the id to doc id
			docid.set(splitted[0]);

			/*
			 * Clean text:
			 * 1. Lower case
			 * 2. Turn all special chars to white space
			 * 3. Make all continuous white spaces to one
			 */
			String filtered = splitted[1].toLowerCase();
			filtered = filtered.replaceAll("[^a-z]", " ");
			filtered = filtered.replaceAll("\\s+", " ");

			StringTokenizer tokenizer = new StringTokenizer(filtered);

			// iteration
			while (tokenizer.hasMoreTokens()) {
				word.set(tokenizer.nextToken());
				context.write(word, docid);
			}
		}
	}

	public static class Hash_Reducer extends Reducer<Text, Text, Text, Text> {
		/*
		 * Use a hash map to calculate the appearance times of each word in each doc
		 * Input: key - word
		 * 		  values - all doc-ids that the word occurred
		 * Output: write <word, <doc-id:occurrence>>
		 */
		
		// Result string
		private Text result = new Text(); 

		// Key - Word
		// Values - Doc-id
		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

			// Counts the occurrence of each word
			HashMap<String, Integer> counts = new HashMap<String, Integer>();

			for (Text value : values) {
				// if exists, get the previous counts, if not, set default 0
				// +1 count
				counts.put(value.toString(), counts.getOrDefault(value.toString(), 0) + 1);
			}

			String allOccurrence = "";

			// Convert to string
			for (String i : counts.keySet()) {
				allOccurrence += i + ":" + String.valueOf(counts.get(i)) + "\t";
			}

			// Remove the last "\t"
			result.set(allOccurrence.substring(0, allOccurrence.length() - 1));
			context.write(key, result);
		}
	}

	public static void main(String[] args) throws Exception {
		if (args.length != 2) {
		      System.err.println("Usage: wordcount <in> <out>");
		      System.exit(-1);
		}
		Configuration conf = new Configuration();

		Job job = Job.getInstance(conf, "Inverted Index");

		job.setJarByClass(InvertedIndex.class);
		job.setMapperClass(Unigrams_Mapper.class);
		job.setReducerClass(Hash_Reducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}