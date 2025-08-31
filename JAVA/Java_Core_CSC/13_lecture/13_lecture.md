# Java: Параллельные стримы, Аннотации и Рефлекшн

### Параллельные стримы (Parallel Streams)

Обычный Stream в Java выполняет операции последовательно — один за другим, в одном потоке.

Параллельный Stream (parallelStream() или stream().parallel()) разбивает коллекцию на части и обрабатывает их одновременно в нескольких потоках с помощью ForkJoinPool (по умолчанию использует Runtime.getRuntime().availableProcessors() потоков, т.е. число ядер CPU).

```java
// 1. У коллекции
List<Integer> list = List.of(1,2,3,4,5);
list.parallelStream().forEach(System.out::println);

// 2. У обычного стрима вызвать .parallel()
list.stream().parallel().forEach(System.out::println);

// 3. Принудительно обратно в последовательный
list.parallelStream().sequential().forEach(System.out::println);
```

```java
List<String> words = List.of("java", "parallel", "stream", "example");
words.stream()
     .map(String::toUpperCase)
     .forEach(System.out::println);



List<String> words = List.of("java", "parallel", "stream", "example");
words.stream()
     .map(String::toUpperCase)
     .forEach(System.out::println); // порядок не гарантирован
```

### Аннотации
Аннотация (Annotation) — это метаданные в Java.  
Они не меняют поведение программы напрямую, но дают дополнительную информацию компилятору, инструментам или рантайму.

```java
@Override
public String toString() {
    return "Example";
}

@SuppressWarnings("unchecked")
public void method() { }

@Deprecated
public void oldMethod() { }
```

Аннотации можно ставить на:

- Классы

- Методы

- Поля

- Параметры

- Локальные переменные

- Пакеты

- Generic-параметры

- Другие аннотации

#### Мета-аннотации (аннотации для аннотаций)

Эти аннотации задают правила работы собственных аннотаций.

`@Target` — где можно применять аннотацию (класс, метод, поле и т.д.).

```
@Target(ElementType.METHOD)
@interface MyAnnotation {}
```

`@Retention` — как долго хранится аннотация:

- `SOURCE` — только в коде (удаляется компилятором).

- `CLASS` — в .class-файле, но недоступна в рантайме.

- `RUNTIME` — доступна через Reflection.

```
@Retention(RetentionPolicy.RUNTIME)
@interface MyAnnotation {}
```

- `@Documented` — попадает в Javadoc.

- `@Inherited` — аннотация наследуется подклассами.

#### Пользовательские аннотации

```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyAnnotation {
    String value();
    int version() default 1;
}

class Test {
    @MyAnnotation(value = "example", version = 2)
    public void run() {}
}

public class Main {
    public static void main(String[] args) throws Exception {
        Method m = Test.class.getMethod("run");
        MyAnnotation ann = m.getAnnotation(MyAnnotation.class);
        System.out.println(ann.value()); // demo
    }
}
```

#### Reflection

Reflection (Рефлексия) — это механизм в Java, который позволяет изучать и изменять программу во время выполнения.

Через Reflection можно:

- Узнать структуру класса: его поля, методы, конструкторы.

- Вызывать методы и работать с полями даже если их имя известно только в рантайме.

- Читать аннотации и их параметры.

```java
class User {
    private String name = "Alice";

    public void sayHello() {
        System.out.println("Hello, " + name);
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = User.class;

        // Получаем метод
        var method = clazz.getMethod("sayHello");

        // Создаём объект
        Object user = clazz.getDeclaredConstructor().newInstance();

        // Вызываем метод через Reflection
        method.invoke(user); // Hello, Alice
    }
}
```