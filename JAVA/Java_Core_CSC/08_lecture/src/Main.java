import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args){

        // Функциональные интерфейсы
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

        Function<String, Integer> lengthFunc = s -> s.length();
        Consumer<Integer> print = len -> System.out.println("Длина: " + len);

        for (String name : names) {
            Integer len = lengthFunc.apply(name); // преобразуем
            print.accept(len); // выводим
        }

        Function<String, String> upper = String::toUpperCase;
        System.out.println(upper.apply("java"));


        // Optional
        Optional<String> empty = Optional.empty();

        System.out.println(empty.orElse("Default"));            // Default
        System.out.println(empty.orElseGet(() -> "Generated")); // Generated

        Optional<String> opt = Optional.of("java");
        Optional<String> upper2 = opt.map(String::toUpperCase);

        System.out.println(upper2.get()); // JAVA


        // Stream API
        List<String> names2 = List.of("Ivan", "Anna", "Petr", "Oleg");

        List<String> result = names2.stream()
                .filter(s -> s.length() == 4)
                .map(String::toUpperCase)
                .sorted()
                .toList();

        System.out.println(result); // [ANNA, IVAN, OLEG]


        List<String> words = List.of("apple", "banana", "apricot", "cherry", "avocado");

        Map<Character, List<String>> grouped = words.stream()
                .filter(w -> w.startsWith("a"))
                .collect(Collectors.groupingBy(w -> w.charAt(0)));

        System.out.println(grouped);
        // {a=[apple, apricot, avocado]}


    }
}
