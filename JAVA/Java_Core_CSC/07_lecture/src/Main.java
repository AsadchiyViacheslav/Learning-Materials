import java.util.*;

public class Main {
    public static void main(String[] args){

        // Comparable
        List<Student> students = new ArrayList<>();
        students.add(new Student("Alice", 22));
        students.add(new Student("Bob", 20));
        students.add(new Student("Charlie", 25));

        Collections.sort(students);
        System.out.println(students);
        // Output: [Bob (20), Alice (22), Charlie (25)]



        // Comparator
        Comparator<Student> byName = new Comparator<Student>() {
            @Override
            public int compare(Student s1, Student s2) {
                return s1.name.compareTo(s2.name);
            }
        };
        //students.sort((s1, s2) -> Integer.compare(s1.age, s2.age));

        students.sort(byName);
        System.out.println(students);
    }
}
