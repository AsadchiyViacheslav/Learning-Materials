import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args){
        Map<Integer, Set<String>> grouped = Stream.of("Java", "Go", "Python", "C")
                .collect(Collectors.groupingBy(
                        String::length,
                        Collectors.toSet()
                ));
        System.out.println(grouped.toString());


        Map<Boolean, List<Integer>> partitioned = Stream.of(1, 2, 3, 4, 5, 6)
                .collect(Collectors.partitioningBy(n -> n % 2 == 0));

        System.out.println(partitioned.toString());
    }
}
