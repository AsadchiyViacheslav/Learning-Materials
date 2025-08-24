import java.io.*;
import java.util.StringTokenizer;

public class MainFast {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

        // Читаем строку
        String text = br.readLine();

        // Читаем два числа
        StringTokenizer st = new StringTokenizer(br.readLine());
        int a = Integer.parseInt(st.nextToken());
        int b = Integer.parseInt(st.nextToken());

        // Читаем вещественное число
        double d = Double.parseDouble(br.readLine());

        // Вывод (через PrintWriter — быстро и буферизованно)
        out.println(text + ": " + d);
        out.println(text + ": " + b + " " + a);

        out.flush();
    }
}