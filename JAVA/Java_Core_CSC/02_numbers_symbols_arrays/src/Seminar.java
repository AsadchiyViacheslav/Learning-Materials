import java.math.BigDecimal;
import java.util.Arrays;

public class Seminar {
    public static void main(String[] args)
    {
        // Логические значения
        boolean a = true;
        boolean b = false;

        System.out.println(a && b);
        System.out.println(a || b);
        System.out.println(a ^ b);

        // Целые числа
        byte var1 = Byte.MAX_VALUE;
        short var2 = Short.MAX_VALUE;
        int var3 = Integer.MIN_VALUE;
        long var4 = Long.MAX_VALUE;

        System.out.println(var1 + " " + var2 + " " + var3 + " " + var4);

        System.out.println((var1 + 1) + " " + (var3 - 1));

        // Символы
        char c = 'a';
        System.out.println(c + 1);
        System.out.println(Character.toUpperCase(c));
        System.out.println(Character.getNumericValue(c));

        // Числа с плавающей точкой
        float x = 0.1F;
        double y = 0.1;
        y += 0.1;
        y += 0.1;

        System.out.println(y + " " + (y == 0.3));

        BigDecimal y1 = BigDecimal.ZERO;

        y1 = y1.add(BigDecimal.valueOf(0.1));
        y1 = y1.add(BigDecimal.valueOf(0.1));
        y1 = y1.add(BigDecimal.valueOf(0.1));

        System.out.println(y1 + " " + (y1.compareTo(BigDecimal.valueOf(0.3)) == 0));

        // Массивы

        int[] arr = {1,2,3,4,5,4,3,2,1};
        System.out.println(arr[0]);
        System.out.println(Arrays.toString(arr));

        boolean[][] arr2 = {{true, true}, {false}};

        boolean[][] arr3 = arr2.clone();

        System.out.println((arr2 == arr3) + " " + Arrays.deepEquals(arr2, arr3));

        int[] numbers = {1,2,3,4,5,6,7,8,9,10};

        for (int i = 0; i < 10; i++)
        {
            if (i % 2 == 0)
            {
                numbers[i] = 100;
            }

        }
        System.out.println(Arrays.toString(numbers));
    }
}
