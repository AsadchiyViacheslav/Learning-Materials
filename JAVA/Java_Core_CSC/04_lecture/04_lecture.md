# Управляющие конструкции, объекты, классы

### Управляющие конструкции

1. if
2. switch
3. while
4. do ... while
5. for (;;)
6. for-each
7. break
8. continue
9. yield
10. return

---

#### Условный оператор if

```
if (x > 0) {
    System.out.println("X is positive");
} else if (x == 0) {
    System.out.println("X is zero");
} else {
    System.out.println("X is negative");
} 

// Допустимо
if (a) return;  
```

Тернарный оператор

`условие ? значение_если_true : значение_если_false`

```
System.out.println(x > 0 ? "positive" : "negative or zero");
```

#### Предложение-выбор switch statement

```
switch (x) {
    case 1 -> System.out.println("One");
    case 2 -> System.out.println("One or Two");
    default -> {
        System.out.print("Other x = ");
        System.out.println(x);
    }
}
```

#### Цикл while и do while

```
while(true) {
    System.out.println("endless");
}
```

```
do {
   System.out.println("one and end");
} while(false); 
```

#### Цикл for

```
for(int i = 0; i < args.length; i++){
    String arg = args[i];
}

//Бесконечный цикл
for (;;) {}
```

Расширенный for
```
for (String arg : args) {
    System.out.println(arg);
}
```

#### break и continue

Известно, что один отвечает за остановку цикла, другой за пропуск итерации.  
Из интересного в java есть break LABEL
```
int[][] matrix = getMatrix;
OUTER:
for(int[] row : matrix) {
    for (int el : row) {
        if (el == 0){
            break OUTER;
        }
    }
}
// В таком случае легче вынести в отдельный метод и делать return
```

### Объект (Object)

- Объект - область фиксированного размера в куче, обладающий фиксированной структурой и содержащий заголовок и полезную информаицю в виде набора значений.
- Значение - ссылка может ссылаться на объекты или на null (не может ссылаться на поле посреди объекта)
- Объект обладает идентичностью, свежесозданный объект не может быть равен (==) никакому ранее созданному
- Объект не может быть реинтерпретирован. Доступ к объекту в обход его структуры запрещён.
- Внутренний формат объекта не специфицирован.
- Заголовок содержит ссылку на класс или на описатель типа-массива.
- Объект любого типа (в том числе массив) также является объектом типа `java.lang.Object`.

### Класс

```java
public class Book {

    // Переменные
    private String title;            // обычная переменная (у каждого объекта своя)
    private final String author;     // final переменная (назначается в конструкторе, потом нельзя менять)
    private static int bookCount = 0; // static переменная (общая для всех объектов)

    // Конструктор
    public Book(String title, String author) {
        this.title = title;
        this.author = author;
        bookCount++; // увеличиваем счётчик при создании объекта
    }

    // Статический метод
    public static int getBookCount() {
        return bookCount;
    }

    // Final метод (нельзя переопределить при наследовании)
    public final void printInfo() {
        System.out.println("Book: " + title + " by " + author);
    }

    // Обычный метод
    public void setTitle(String title) {
        this.title = title;
    }

    // Перегрузка метода (overloading)
    public void read() {
        System.out.println("Reading \"" + title + "\"...");
    }

    public void read(int pages) {
        System.out.println("Reading " + pages + " pages of \"" + title + "\"...");
    }
}

public class Main {
    public static void main(String[] args) {
        Book book1 = new Book("1984", "George Orwell");
        Book book2 = new Book("Brave New World", "Aldous Huxley");

        book1.printInfo(); // final метод
        book2.printInfo();

        book1.read();          // вызов перегруженного метода без параметров
        book2.read(50);        // перегруженный метод с параметром

        System.out.println("Всего книг создано: " + Book.getBookCount()); // static метод
    }
}
```

#### Методы Object

- `toString()` -> Возвращает строковое представление объекта. По умолчанию: `ИмяКласса@ХэшКод`.
- `equals()` -> Сравнивает объекты на равенство. По умолчанию — сравнение ссылок.
- `hashCode()` -> Возвращает числовое значение для объекта
- `getClass()` -> Возвращает объект типа Class, описывающий структуру объекта (reflection API).
- `wait()` -> Многопоточность
- `notify()` -> Многопоточность
- `notifyAll()` -> Многопоточность
- `clone()` -> Создаёт копию объекта (поверхностное клонирование).
- `finalize()` -> Считается устаревшим (deprecated)