import java.util.Locale;
import java.util.Scanner;

public class MainBasic {
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);


        scanner.useLocale(Locale.US); // теперь Scanner тоже ждёт "3.14"


        // Читаем строку
        String text = scanner.nextLine();

        // Читаем два целых числа
        int a = scanner.nextInt();
        int b = scanner.nextInt();

        scanner.nextLine(); // убрать перенос строки, но работает и без него

        // Читаем вещественное число
        double c = scanner.nextDouble();

        // Вывод
        System.out.println(text + ": " + c);
        System.out.println(text + ": " + b + " " + a);
    }
}
