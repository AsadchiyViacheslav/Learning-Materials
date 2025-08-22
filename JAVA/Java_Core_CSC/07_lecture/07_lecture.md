# Сравнение объектов в Java

В Java часто нужно сортировать объекты. Например: список студентов по возрасту, список книг по названию и т.д.

Для этого есть два подхода:
1. Встроенное сравнение объекта → Comparable<T>
2. Внешнее сравнение объекта → Comparator<T>

### Comparable<T>

Интерфейс, который определяет "естественный порядок" объектов.

Объект сам знает, как себя сравнить с другими.

Содержит один метод:
```
int compareTo(T other)
```

Возвращает:
- < 0, если текущий объект меньше other
- 0, если объекты равны
- \> 0, если текущий объект больше other

### Comparator<T>

Интерфейс для внешнего сравнения объектов.  
Используется, когда:
- Нельзя или не хочется менять класс объекта
- Нужно сортировать по разным критериям

Основной метод
```
int compare(T o1, T o2)
```

Возвращает:
- < 0, если o1 меньше o2
- 0, если равны
- \> 0, если o1 больше o2

### Comparator combinators (Java 8+)

Java 8 добавила удобные методы для комбинирования Comparator:

| Метод                          | Описание                               |
| ------------------------------ | -------------------------------------- |
| `Comparator.comparing(...)`    | Создаёт Comparator по ключу            |
| `thenComparing(...)`           | Добавляет вторичный критерий сравнения |
| `reversed()`                   | Переворачивает порядок                 |
| `nullsFirst()` / `nullsLast()` | Обрабатывает null значения             |

```java
Comparator<Student> cmp = Comparator
        .comparing((Student s) -> s.age)       // по возрасту
        .thenComparing(s -> s.name);           // если возраст равен, по имени

students.sort(cmp);
```

```java
Comparator<Student> cmp2 = Comparator
        .comparing(Student::getAge, Comparator.nullsFirst(Comparator.naturalOrder()))
        .reversed();

students.sort(cmp2);
```