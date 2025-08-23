# Коллекторы в Stream API

### collect()

Метод collect() — это терминальная операция стрима, которая превращает поток элементов в какую-то конечную форму:
- коллекцию (List, Set, Map),
- строку,
- число (сумму, среднее, статистику),
- или даже кастомный объект.  

Фактически, это "сборщик" результата из потока.

### Интерфейс Collector<T, A, R>

```
Collector<T, A, R>, где

T — тип элементов в стриме
A — тип аккумулятора (внутреннего контейнера для накопления результата)
R — конечный результат
```

Пример:  
```Collector<String, ?, List<String>>``` превращает поток String в ```List<String>```

### Collectors — фабричный класс

В Java есть утилитарный класс java.util.stream.Collectors, который предоставляет кучу готовых фабричных методов для создания популярных коллекторов.

**Сбор в список или множество**

```java
List<String> names = Stream.of("Java", "Python", "C++")
        .collect(Collectors.toList());

Set<String> langs = Stream.of("Java", "Python", "Java")
        .collect(Collectors.toSet());
```

**Сбор в Map**

```java
.collect(Collectors.toMap(
    String::length,  // ключ = длина строки
    s -> s,
    (s1, s2) -> s1   // правило при коллизии
));
```

**Объединение в строку**
```java
String langs = Stream.of("Java", "Python", "Go")
        .collect(Collectors.joining(", "));
// "Java, Python, Go"
```

**Подсчёт статистики**
```java
long count = Stream.of("Java", "Python", "Go")
        .collect(Collectors.counting());

double avg = Stream.of(1, 2, 3, 4)
        .collect(Collectors.averagingInt(i -> i));
// 2.5
```

**Группировка**

```java
Map<Integer, Set<String>> grouped = Stream.of("Java", "Go", "Python", "C")
        .collect(Collectors.groupingBy(
            String::length,
            Collectors.toSet()
        ));
```

**Разделение**

```java
Map<Boolean, List<Integer>> partitioned = Stream.of(1, 2, 3, 4, 5, 6)
        .collect(Collectors.partitioningBy(n -> n % 2 == 0));
// {false=[1, 3, 5], true=[2, 4, 6]}
```

**Свой Collector**

Пример — собираем стрим в StringBuilder:

```java
Collector<String, StringBuilder, String> customCollector =
    Collector.of(
        StringBuilder::new,           // supplier (создать аккумулятор)
        StringBuilder::append,        // accumulator (добавить элемент)
        StringBuilder::append,        // combiner (объединить аккумуляторы в параллельном стриме)
        StringBuilder::toString       // finisher (преобразовать результат)
    );

String result = Stream.of("Java", "Python", "Go")
        .collect(customCollector);
// "JavaPythonGo"
```

