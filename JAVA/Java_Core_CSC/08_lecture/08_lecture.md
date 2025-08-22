# Элементы функционального программирования. Stream API

### Функциональный интерфейс

Функциональный интерфейс ― это интерфейс, у которого ровно один абстрактный метод.
(Может быть сколько угодно default и static методов, но только один "чистый" абстрактный).

Зачем это нужно?

- В Java лямбда-выражения и ссылки на методы можно присвоить только переменной типа функционального интерфейса.

- Таким образом, функциональный интерфейс ― это контейнер для функции.

Аннотация `@FunctionalInterface`

Хотя необязательно, но обычно интерфейс помечают аннотацией `@FunctionalInterface.`
Это гарантия на уровне компилятора, что в интерфейсе только один абстрактный метод.

```java
@FunctionalInterface
public interface MyFunction {
    int apply(int x); // один абстрактный метод
}

public class Main {
    public static void main(String[] args) {
        MyFunction square = x -> x * x;   // лямбда вместо класса
        System.out.println(square.apply(5)); // 25
    }
}
```

**Встроенные функциональные интерфейсы в `Java (java.util.function)`**

| Интерфейс           | Сигнатура             | Пример использования                          |
| ------------------- | --------------------- | --------------------------------------------- |
| `Predicate<T>`      | `boolean test(T t)`   | проверка условия (`x -> x > 10`)              |
| `Function<T,R>`     | `R apply(T t)`        | преобразование (`s -> s.length()`)            |
| `Consumer<T>`       | `void accept(T t)`    | действие без возврата (`System.out::println`) |
| `Supplier<T>`       | `T get()`             | генерация значения (`() -> Math.random()`)    |
| `UnaryOperator<T>`  | `T apply(T t)`        | функция `T -> T` (`x -> x*x`)                 |
| `BinaryOperator<T>` | `T apply(T t1, T t2)` | объединение двух значений (`(a,b)->a+b`)      |


### Функциональные выражения в Java

В Java под этим обычно понимают:
- ямбда-выражения
- ссылки на методы
- ссылки на конструкторы
- использование их вместе с функциональными интерфейсами

Именно они позволяют писать короткий, декларативный код (особенно со Stream API).

Лямбды и ссылки на методы работают только через функциональные интерфейсы.
То есть Java должна знать в какой метод передать лямбду.

#### Лямбда-выражения

Лямбда-выражение — это компактная форма записи анонимного класса, реализующего функциональный интерфейс.

```
(параметры) -> выражение
или
(параметры) -> { блок кода }
```

```java
Function<Integer, Integer> square = x -> x * x;
System.out.println(square.apply(5)); // 25
```

#### Ссылки на методы (Method References)

Когда лямбда просто вызывает существующий метод, можно заменить её на ссылку на метод.

```java
Function<String, Integer> parser = Integer::parseInt;
System.out.println(parser.apply("123")); // 123


Consumer<String> printer = System.out::println;
printer.accept("Hello"); // Hello


Function<String, String> upper = String::toUpperCase;
System.out.println(upper.apply("java")); // JAVA


Supplier<List<String>> listCreator = ArrayList::new;
List<String> list = listCreator.get();
list.add("Hi");
System.out.println(list); // [Hi]
```
#### Лямбды и захват переменных (closure)

Лямбда может использовать переменные из внешней области, но только если они effectively final (не изменяются после инициализации).

```java
public static void main(String[] args) {
    int factor = 2;
    Function<Integer, Integer> multiplier = x -> x * factor;
    System.out.println(multiplier.apply(5)); // 10

    // factor = 3; // ошибка: переменная должна быть "effectively final"
}
```

### Optional<T>

Optional<T> — это контейнер, который может:
- хранить объект типа T, либо
- быть пустым (означает "значение отсутствует").

То есть вместо того, чтобы возвращать null из метода, можно вернуть Optional<T>.
Тогда вызывающий код вынужден явно обработать ситуацию "значения нет".

```java
// Пустой Optional
Optional<String> empty = Optional.empty();

// Optional с ненулевым значением
Optional<String> opt1 = Optional.of("Hello");

// Optional, который может быть null
Optional<String> opt2 = Optional.ofNullable(null);
```

```java
Optional<String> empty = Optional.empty();

System.out.println(empty.orElse("Default"));            // Default
System.out.println(empty.orElseGet(() -> "Generated")); // Generated
```

Работа в функциональном стиле

`map` — применяет функцию к значению, если оно есть:
```java
Optional<String> opt = Optional.of("java");
Optional<String> upper = opt.map(String::toUpperCase);

System.out.println(upper.get()); // JAVA
```

`filter` — оставить значение только если выполняется условие:
```java
Optional<String> opt = Optional.of("Java");
Optional<String> filtered = opt.filter(s -> s.length() > 5);

System.out.println(filtered.isPresent()); // false
```

`ifPresent` — выполнить действие, если значение есть:
```java
Optional<String> opt = Optional.of("Hello");
opt.ifPresent(s -> System.out.println("Value: " + s));
// Value: Hello
```

### Stream API

Stream API — это инструмент для работы с коллекциями и данными в функциональном стиле.
Он позволяет обрабатывать последовательности элементов (потоки данных) декларативно: вместо циклов и if писать цепочки операций.  
*Данные в коллекции остаются нетронутыми, Stream возвращает новые значения.*

**Основные свойства Stream**
- Поток обрабатывается последовательно (по умолчанию) или параллельно (parallelStream()).
- Потоки одноразовые: после вызова terminal operation (конечного метода) они закрываются.
- Делятся на:
  - промежуточные (intermediate operations) — возвращают новый Stream;
  - конечные (terminal operations) — завершают обработку и возвращают результат (коллекцию, число, Optional и т. д.).

**Как получить Stream**

```java
// Из коллекции
List<Integer> list = List.of(1, 2, 3, 4, 5);
Stream<Integer> stream = list.stream();

// Из массива
int[] arr = {1, 2, 3};
IntStream intStream = Arrays.stream(arr);

// Из значений
Stream<String> stream = Stream.of("a", "b", "c");

// Бесконечные потоки
Stream<Integer> infinite = Stream.iterate(0, n -> n + 1);
```

#### Основные промежуточные операции

Эти методы не изменяют данные и возвращают новый Stream.


```
List<String> names = List.of("Alice", "Bob", "Charlie", "David");
```

`filter(Predicate)`  
Оставляет только элементы, удовлетворяющие условию.
```
names.stream()
.filter(s -> s.startsWith("A"))
.forEach(System.out::println); // Alice
```
`map(Function)`  
Преобразует элементы.
```
names.stream()
.map(String::toUpperCase)
.forEach(System.out::println); // ALICE, BOB...
```
`flatMap(Function)`  
Разворачивает вложенные потоки.

```
List<List<String>> nested = List.of(List.of("a", "b"), List.of("c", "d"));

nested.stream()
.flatMap(Collection::stream)
.forEach(System.out::println); // a, b, c, d
```
`sorted(Comparator)`  
Сортировка.
```
names.stream()
.sorted()
.forEach(System.out::println); // Alice, Bob, Charlie, David
```
`distinct()`  
Удаляет дубликаты.
```
List.of(1, 2, 2, 3, 3).stream()
.distinct()
.forEach(System.out::println); // 1, 2, 3
```

`limit(n) и skip(n)`  
limit(n) — первые n элементов.  
skip(n) — пропустить первые n элементов.
```
Stream.iterate(1, n -> n + 1)
.limit(5)
.forEach(System.out::println); // 1 2 3 4 5
```

#### Конечные операции (terminal)

`forEach`
```
names.stream().forEach(System.out::println);
```

`collect`

Собирает результат в коллекцию.
```
List<String> upper = names.stream()
.map(String::toUpperCase)
.toList();  // Java 16+
```
`reduce`

Свертка — объединение элементов в одно значение.
```
int sum = List.of(1, 2, 3, 4).stream()
.reduce(0, (a, b) -> a + b);
System.out.println(sum); // 10
```
`count`
```
long count = names.stream().count(); // 4
```
`min / max`
```
Optional<String> min = names.stream().min(String::compareTo);
System.out.println(min.get()); // Alice
```
`anyMatch / allMatch / noneMatch`
```
boolean hasA = names.stream().anyMatch(s -> s.startsWith("A")); // true
boolean allLong = names.stream().allMatch(s -> s.length() > 2); // true
```

#### Параллельные потоки

Stream API умеет распараллеливать обработку:
```java
int sum = IntStream.range(1, 1_000_000)
                   .parallel()
                   .sum();
```