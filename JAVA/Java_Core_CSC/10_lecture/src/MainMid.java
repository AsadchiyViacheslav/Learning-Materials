import java.io.*;

public class MainMid {
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

        String text = in.readLine();

        String[] vars = in.readLine().split(" ");
        int a = Integer.parseInt(vars[0]);
        int b = Integer.parseInt(vars[1]);

        double c = Double.parseDouble((in.readLine()));

        // Вывод
        out.println(text + ": " + c);
        out.println(text + ": " + b + " " + a);

        out.flush();
    }
}
