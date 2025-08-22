import java.util.*;

public class CollectionsLecture {
    public static void main(String[] args){

        // Iterable и Iterator
        Iterable<String> iterable = List.of("x", "y", "z");  // Iterable
        Iterator<String> iterator = iterable.iterator();      // получаем Iterator

        while (iterator.hasNext()) {
            String item = iterator.next();
            System.out.println(item);
        }


        // Set и реализации
        HashSet<String> set = new HashSet<>();
        set.add("Apple");
        set.add("Banana");
        set.add("Apple"); // дубликат не добавится
        System.out.println(set);

        LinkedHashSet<String> linkedSet = new LinkedHashSet<>();
        linkedSet.add("Apple");
        linkedSet.add("Banana");
        linkedSet.add("Cherry");
        System.out.println(linkedSet); // [Apple, Banana, Cherry] — порядок вставки сохраняется

        TreeSet<Integer> treeSet = new TreeSet<>();
        treeSet.add(5);
        treeSet.add(1);
        treeSet.add(3);
        treeSet.add(3); // дубликат не добавится
        System.out.println(treeSet); // [1, 3, 5] — автоматически сортируется


        // List и реализации
        ArrayList<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add(1, "C"); // вставка по индексу
        System.out.println(list); // [A, C, B]

        LinkedList<Integer> list2 = new LinkedList<>();
        list2.add(10);
        list2.add(20);
        list2.addFirst(5); // метод LinkedList
        System.out.println(list2); // [5, 10, 20]

        Stack<Integer> stack = new Stack<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);

        System.out.println(stack.pop());  // 3
        System.out.println(stack.peek()); // 2
        System.out.println(stack);        // [1, 2]


        // Queue и реализации
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.add(5);
        pq.add(1);
        pq.add(10);

        System.out.println(pq.poll()); // 1
        System.out.println(pq.poll()); // 5
        System.out.println(pq.poll()); // 10

        // Как очередь
        ArrayDeque<String> deque = new ArrayDeque<>();
        deque.addLast("A");
        deque.addLast("B");
        deque.addLast("C");
        System.out.println(deque.pollFirst()); // A
        System.out.println(deque.pollFirst()); // B


        // Как стек
        Deque<Integer> stack2 = new ArrayDeque<>();
        stack2.push(1);
        stack2.push(2);
        stack2.push(3);
        System.out.println(stack2.pop()); // 3
        System.out.println(stack2.pop()); // 2


        // Map и реализации
        Map<String, Integer> map = new HashMap<>();
        map.put("Alice", 25);
        map.put("Bob", 30);
        map.put("Charlie", 35);
        System.out.println(map.get("Bob")); // 30

        Map<String, Integer> map2 = new LinkedHashMap<>();
        map2.put("Alice", 25);
        map2.put("Bob", 30);
        map2.put("Charlie", 35);
        for (String key : map2.keySet()) {
            System.out.println(key);
        }
        // Alice, Bob, Charlie — порядок вставки сохранён

        TreeMap<String, Integer> treemap = new TreeMap<>();
        treemap.put("Charlie", 35);
        treemap.put("Alice", 25);
        treemap.put("Bob", 30);
        for (Map.Entry<String, Integer> entry : treemap.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        // Output: Alice: 25, Bob: 30, Charlie: 35 — отсортировано по ключу
    }

}
