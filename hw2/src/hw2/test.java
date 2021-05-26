package hw2;

public class test {
	private final static String SEED_PATTERN = "^(https://|http://)?(www.)?wsj.com/.*";
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.print("http://www.wsj.com/asdasd".matches(SEED_PATTERN));
	}

}
