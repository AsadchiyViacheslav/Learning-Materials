# Исключения, try-catch, обобщенные типы

### Исключения  

- Выбрасываются явно оператором throw
- Выбрасываются вызванным методом или конструктором
- Выбрасываются виртуальной машиной

**Иерархия исключений Java**

![Иерархия изображние]([https://clipof.ru/wp-content/uploads/f/8/f/f8f67c45a9ca61e25f25d2aa26f0ca47.jpeg](https://avatars.mds.yandex.net/i?id=1be2c0783b1baad2926ac715d744042e_l-10780278-images-thumbs&n=13))

**Конструирование исключений**

- Throwable()
- Throwable(message)
- Throwable(cause)
- Throwable(message, cause)
- protected Throwable(message, cause, suppression, stackTrace)

**Что есть у исключения?**

- Сообщение `getMessage()`
- Стек `getStackTrace`
- Причина `getCause`
- Подавленные исключения `addSuppressed()/getSeppressed()`
    
#### Обработка исключений

- Логирование, вывод пользователю: редко, в специальных точках программы.
- Восстановление после исключения (например, вторая попытка подключения после обрыва связи).
- Исключение для управления потоком (ненормальная ситуация)
- Перебрасывание, завернув в исключение другого типа. Всегда сохраняйте исходное исключение в виде причины.

Важно перебрасывать исключения, чтобы не терять причину, пример в `Test2.java`

Конструкция обработки
```
try {;}
catch () {;}
finally {;}
```
#### Логирование

- Фреймворки: Log4j, Logback, Slf4j, Java Logging API
- Уровни: ERROR, WARN, INFO, DEBUG
- Форматтеры: как логировать?
- Аппендеры: куда логировать?

### Обобщенные типы (Generic, Дженерики)

Идея: описываем класс/интерфейс/метод с параметрами-типами (type parameters), чтобы компилятор проверял типы и не было cast’ов.

Generics — это способ сказать компилятору: "этот код работает с каким-то типом данных, но ты заранее проследи, чтобы мы не перепутали типы".

#### Простыми словами

Без generics все объекты хранились как Object, и программист сам отвечал за правильное приведение типов.  
С generics тип указывается явно, и компилятор проверяет всё на этапе компиляции → меньше багов, меньше кастов.

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List list = new ArrayList();   // тут нет <T>
        list.add("Hello");
        list.add(123);  // ошибка? Нет! Компилятор пропустит

        String s = (String) list.get(0); // нужен каст (String)
        System.out.println(s);

        // Но тут вылетит ClassCastException во время выполнения!
        String wrong = (String) list.get(1);
    }
}
```

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();  // generics <String>
        list.add("Hello");
        // list.add(123);  // ошибка на этапе компиляции!

        String s = list.get(0);  // каст не нужен
        System.out.println(s);
    }
}
```
#### Параметризация типов

```java
class Box<T> {
    private T value;
    public Box(T value) { this.value = value; }
    public T get() { return value; }
}

Box<String> b = new Box<>("hi");
String s = b.get(); // без кастов
```

```java
class MathBox<T extends Number> {
    private final T n;
    MathBox(T n) { this.n = n; }
    double twice() { return n.doubleValue() * 2; }
}

MathBox<Integer> mi = new MathBox<>(21);
System.out.println(mi.twice()); // 42.0
```

#### Маскировочный символ (wildcard) ? и иерархия типов

Wildcard ? — «какой-то тип, неизвестный нам». С границами:
- ? extends X — верхняя граница: «любой подтип X». Коллекция — producer (мы читаем). Добавлять элементы нельзя (кроме null).
- ? super X — нижняя граница: «любой надтип X». Коллекция — consumer (мы пишем). Читать элементы как X нельзя (только как Object).  

Мнемоника PECS: Producer Extends, Consumer Super.

```java
static double sum(List<? extends Number> xs) {
    double s = 0;
    for (Number n : xs) s += n.doubleValue();
    return s;
}

System.out.println(sum(List.of(1, 2, 3)));     // List<Integer>
System.out.println(sum(List.of(1.5, 2.5, 3.0))); // List<Double>
```

```java
static void addAllIntegers(List<? super Integer> dst, List<Integer> src) {
    for (Integer x : src) dst.add(x); // можно добавлять Integer
    // Integer -> подходит для ? super Integer
}

List<Number> numbers = new ArrayList<>();
addAllIntegers(numbers, List.of(1, 2, 3));
```

Надтипы и подтипы + wildcard в иерархии

Классическая иерархия: Integer <: Number <: Object

Но инвариантность: из Integer <: Number не следует
List<Integer> <: List<Number>. Для гибкости — wildcard.

```java
// copy(src -> dst): читаем из producer (extends), пишем в consumer (super)
static <T> void copy(List<? extends T> src, List<? super T> dst) {
    for (T x : src) dst.add(x);
}

List<Integer> src = List.of(1, 2, 3);
List<Number>  dst = new ArrayList<>();
copy(src, dst); // ОК
```

#### Параметризованные методы (generic methods)

Это когда метод сам вводит собственный параметр типа — независимый от класса.

```java
static <T> T first(List<T> xs) { return xs.get(0); }

Integer x = first(List.of(10, 20));
String  y = first(List.of("a", "b"));
```

#### «Две ссылки в сигнатуре» (самоссылочные/рекурсивные ограничения)

```java
class SelfComparable<T extends SelfComparable<T>> implements Comparable<T> {
    private final int rank;
    SelfComparable(int rank) { this.rank = rank; }

    @Override public int compareTo(T o) {
        return Integer.compare(this.rank, ((SelfComparable<?>) o).rank);
    }
}
```

#### Raw type (сырой тип)

Использование обобщённого типа без параметра: List вместо List<T>. Это сохраняется ради обратной совместимости, но ломает типобезопасность.

```java
List raw = new ArrayList();  // raw type
raw.add("str");
raw.add(123);                // компилируется, но опасно
```

#### Дженерики и массивы

- Массивы ковариантны: Integer[] <: Number[]. Это опасно (ArrayStoreException).

- Дженерики инвариантны и проверяются на этапе компиляции ⇒ безопаснее.

```java
Number[] a = new Integer[1];
a[0] = 3.14; // ArrayStoreException (рантайм), но компилируется
```

```java
class Bag<T> {
    // T[] data = new T[10]; // так нельзя
    List<T> data = new ArrayList<>(); // используем List вместо массива
}
```

#### Varargs и generics

- Varargs = «переменное число аргументов»: void f(String... xs).

- Комбинация с generics может привести к heap pollution (несовместимость реального массива аргументов и параметров типов).

- Для безопасных varargs-методов с generics используется @SafeVarargs (метод/конструктор final, static или private), если вы гарантируете отсутствие небезопасных операций.

```java
static <T> List<T> listOf(T... xs) {
    return Arrays.asList(xs);
}
System.out.println(listOf(1, 2, 3));
```

```java
class Utils {
    @SafeVarargs
    public static <T> List<T> concat(List<T>... lists) {
        List<T> out = new ArrayList<>();
        for (List<T> l : lists) out.addAll(l);
        return out;
    }
}

List<Integer> a = List.of(1,2);
List<Integer> b = List.of(3,4);
System.out.println(Utils.concat(a, b)); // [1, 2, 3, 4]
```
