import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;

public class URLRead {
    public static void main(String[] args) throws Exception {
        URL url = new URL("https://example.com");
        try (BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
        }
    }
}
