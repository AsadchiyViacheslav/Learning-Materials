# Коллекции

**Иерархия коллекций в Java**
![Иерархия](https://i2.wp.com/data-flair.training/blogs/wp-content/uploads/sites/2/2018/03/hierarchy-of-collection-framework-in-java.webp)

### Iterable<E> и Iterator<E>

`Iterable<E>` — это интерфейс, который говорит: «Этот объект можно перебрать в цикле for-each».

Основные моменты:

- Любая коллекция в Java (List, Set, Queue, …) реализует Iterable<E>.

- Метод iterator() возвращает объект типа Iterator<E>.

- Благодаря этому можно использовать расширенный for:

`Iterator<E>` — интерфейс для пошагового перебора элементов коллекции.

| Метод               | Что делает                              |
| ------------------- | --------------------------------------- |
| `boolean hasNext()` | Проверяет, есть ли следующий элемент    |
| `E next()`          | Возвращает следующий элемент            |
| `void remove()`     | Удаляет текущий элемент (необязательно) |

Iterable объект может выдать итератор
```java
Iterable<String> iterable = List.of("x", "y", "z");  // Iterable
Iterator<String> iterator = iterable.iterator();      // получаем Iterator

while (iterator.hasNext()) {                          
    String item = iterator.next();
    System.out.println(item);
}
```

### Collection<E>

`Collection<E>` — это базовый интерфейс в Java для всех коллекций элементов.

Сигнатура интерфейса
```java
public interface Collection<E> extends Iterable<E> {
    // методы добавления, удаления, поиска и перебора элементов
}
```

**Основные методы Collection**

| Метод                               | Что делает                                                 |
| ----------------------------------- | ---------------------------------------------------------- |
| `add(E e)`                          | Добавляет элемент в коллекцию                              |
| `remove(Object o)`                  | Удаляет элемент                                            |
| `size()`                            | Возвращает количество элементов                            |
| `isEmpty()`                         | Проверяет, пустая ли коллекция                             |
| `contains(Object o)`                | Проверяет, есть ли элемент                                 |
| `clear()`                           | Очищает коллекцию                                          |
| `iterator()`                        | Возвращает `Iterator<E>` для перебора                      |
| `toArray()`                         | Преобразует коллекцию в массив                             |
| `addAll(Collection<? extends E> c)` | Добавляет все элементы из другой коллекции                 |
| `removeAll(Collection<?> c)`        | Удаляет элементы, которые есть в другой коллекции          |
| `retainAll(Collection<?> c)`        | Сохраняет только элементы, которые есть в другой коллекции |

### Set<E>

`Set<E>` — это коллекция уникальных элементов, то есть дубликаты запрещены.

Set<E> наследуется от Collection<E>, значит все базовые методы коллекций (add, remove, size, contains, iterator) тоже доступны.

---

#### HashSet<E>

Основные моменты
- Основан на хеш-таблице (HashMap).
- Уникальные элементы, порядок не гарантируется.
- Допускается null (только один элемент null).
- Время основных операций: O(1) для add, remove, contains.
- Эффективен при быстром поиске и удалении.

```java
Set<String> set = new HashSet<>();
set.add("Apple");
set.add("Banana");
set.add("Apple"); // дубликат не добавится

System.out.println(set);
```

---

#### LinkedHashSet<E>

Основные моменты
- Расширяет HashSet и хранит связный список для элементов.
- Сохраняет порядок вставки.
- Уникальные элементы, допускается null (один).
- Время операций O(1), чуть медленнее HashSet из-за дополнительной структуры.

```java
Set<String> linkedSet = new LinkedHashSet<>();
linkedSet.add("Apple");
linkedSet.add("Banana");
linkedSet.add("Cherry");

System.out.println(linkedSet); // [Apple, Banana, Cherry] — порядок вставки сохраняется
```

---

#### TreeSet<E>

Основные моменты
- Основан на красно-чёрном дереве (Red-Black Tree).
- Элементы автоматически сортируются по естественному порядку (Comparable) или по предоставленному Comparator.
- Не допускает null, если используется естественный порядок (NullPointerException).
- Время операций O(log n) для add, remove, contains.

```java
Set<Integer> treeSet = new TreeSet<>();
treeSet.add(5);
treeSet.add(1);
treeSet.add(3);
treeSet.add(3); // дубликат не добавится

System.out.println(treeSet); // [1, 3, 5] — автоматически сортируется
```

### List<E>

`List<E>` — это упорядоченная коллекция элементов (имеет индексы)

Есть методы работающие с индексами: `get(int index)`, `set(int index, E element)`, `add(int index, E element)`,` `remove(int index)`.

---

#### ArrayList<E>

Основные моменты
- Основан на динамическом массиве.
- Быстрый доступ по индексу: O(1) для get(i).
- Добавление в конец: O(1) амортизированное, иногда O(n), когда массив увеличивается.
- Вставка/удаление в середине: O(n), т.к. элементы нужно сдвигать.

```java
List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
list.add(1, "C"); // вставка по индексу
System.out.println(list); // [A, C, B]
```
---

#### LinkedList<E>

Основные моменты
- Основан на двусвязном списке.
- Доступ по индексу: O(n), т.к. нужно пройти по элементам.
- Добавление/удаление в начале или середине: O(1) если есть ссылка на узел.

```java
List<Integer> list = new LinkedList<>();
list.add(10);
list.add(20);
list.addFirst(5); // метод LinkedList
System.out.println(list); // [5, 10, 20]
```
---

#### Vector<E>

Основные моменты
- Основан на динамическом массиве, как ArrayList.
- Синхронизирован → потокобезопасный, но медленнее ArrayList.
- Редко используется в современном коде (лучше ArrayList + синхронизация при необходимости).

В современных проектах лучше ArrayList + Collections.synchronizedList(...)

---

#### Stack<E>

Основные моменты
- Наследует Vector<E> → потокобезопасный.
- Реализует стек (LIFO): last-in-first-out.   
- 
Основные методы:  
`push(E e)` — положить на стек  
`pop()` — достать верхний элемент  
`peek()` — посмотреть верхний элемент без удаления  
`empty()` — проверить пустой ли стек  

```java
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.push(2);
stack.push(3);

System.out.println(stack.pop());  // 3
System.out.println(stack.peek()); // 2
System.out.println(stack);        // [1, 2]
```

В современных проектах лучше использовать Deque<E> (ArrayDeque) для стека, т.к. Stack устаревший.

### Queue<E>

`Queue<E>` — это интерфейс коллекции, представляющий структуру данных "очередь" (FIFO — first in, first out).

Элементы добавляются в конец (tail) и извлекаются из начала (head).

| Метод        | Описание                                                           |
| ------------ | ------------------------------------------------------------------ |
| `add(E e)`   | Добавляет элемент в конец, выбрасывает исключение, если не удалось |
| `offer(E e)` | Добавляет элемент в конец, возвращает false при неудаче            |
| `remove()`   | Удаляет и возвращает элемент с начала, исключение, если пусто      |
| `poll()`     | Удаляет и возвращает элемент с начала, возвращает null, если пусто |
| `element()`  | Возвращает элемент с начала без удаления, исключение, если пусто   |
| `peek()`     | Возвращает элемент с начала без удаления, null если пусто          |

---

#### PriorityQueue<E>

Основные моменты
- Очередь с приоритетом — элементы извлекаются не по порядку вставки, а в порядке естественного сравнения (Comparable) или по заданному Comparator.
- Не допускает null.
- Не потокобезопасна (для многопоточности используйте PriorityBlockingQueue).
- Реализована на бинарной куче (heap) → add, poll, peek работают за O(log n).
- Позволяет хранить дубликаты.

```java
Queue<Integer> pq = new PriorityQueue<>();
pq.add(5);
pq.add(1);
pq.add(10);

System.out.println(pq.poll()); // 1
System.out.println(pq.poll()); // 5
System.out.println(pq.poll()); // 10
```
---

#### ArrayDeque<E>

Основные моменты
- Двусторонняя очередь (Deque), основанная на динамическом массиве.
- Позволяет добавлять/удалять элементы с начала и конца за O(1) амортизированное.
- Не допускает null.
- Быстрее LinkedList для очередей и стеков.
- Поддерживает как FIFO, так и LIFO (стек).

**Основные методы**

| Метод                               | Описание                     |
| ----------------------------------- | ---------------------------- |
| `addFirst(E e)` / `offerFirst(E e)` | Добавляет элемент в начало   |
| `addLast(E e)` / `offerLast(E e)`   | Добавляет элемент в конец    |
| `removeFirst()` / `pollFirst()`     | Удаляет элемент с начала     |
| `removeLast()` / `pollLast()`       | Удаляет элемент с конца      |
| `peekFirst()` / `peekLast()`        | Смотрит элемент без удаления |


```java
// Как очередь
Deque<String> deque = new ArrayDeque<>();
deque.addLast("A");
deque.addLast("B");
deque.addLast("C");

System.out.println(deque.pollFirst()); // A
System.out.println(deque.pollFirst()); // B


// Как стек
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.push(3);

System.out.println(stack.pop()); // 3
        System.out.println(stack.pop()); // 2
```
### Map<E>




---

####



---

####



---

####



---

####