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


### List<E>


### Queue<E>

