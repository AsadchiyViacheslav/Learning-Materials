# Java: примитивы синхронизации, конкурентные коллекции

### Проблемы многопоточности

#### Deadlock (взаимная блокировка)

Суть: два (или больше) потока ждут друг друга бесконечно, потому что у каждого есть ресурс, который нужен другому.

Например: Поток A захватил lock1, ждёт lock2. Поток B захватил lock2, ждёт lock1.

Решение:

- Стараться всегда блокировать ресурсы в одном порядке.

- Использовать tryLock (в ReentrantLock) с тайм-аутом.

#### LiveLock (живой тупик)

Суть: потоки не блокируются, но постоянно уступают друг другу → и никто не делает полезной работы.

Например: Поток A уступает B. Поток B уступает A. В коде это выглядит так, если оба потока проверяют состояние друг друга и всё время меняют своё поведение.

Решение: добавить случайность (например sleep(random)), чтобы один всё-таки сделал шаг.

#### Race Condition (состояние гонки)

Суть: результат программы зависит от того, какой поток успел первым.
- Общая переменная обновляется несинхронизированно.
- Итоговое значение может быть неправильным.

Решение: Использовать блокирующий доступ и атомарные операции.

#### Starvation (голодание)

Суть: поток не получает ресурсов для выполнения, потому что:
- ресурсы постоянно забирают другие потоки,
- или приоритет у него слишком низкий.

Решение: Давать потокам "честный" доступ (ReentrantLock(true) — fair mode).
Избегать бесконечных монополий.


### Высокоуровневые механизмы синхронизации (java.util.concurrent)

#### ReentrantLock

Это альтернатива synchronized, но с расширенными возможностями:

- tryLock() — можно попытаться захватить lock без блокировки или с таймаутом.

- lockInterruptibly() — поток можно прервать во время ожидания.

- Возможность сделать "справедливую блокировку" (fair mode): new ReentrantLock(true) — потоки обслуживаются в порядке очереди.

- Поддерживает рекурсивный захват (как и synchronized).

```java
import java.util.concurrent.locks.ReentrantLock;

class SharedResource {
    private final ReentrantLock lock = new ReentrantLock();
    private int counter = 0;

    public void increment() {
        lock.lock(); // блокировка
        try {
            counter++;
        } finally {
            lock.unlock(); // обязательно освобождать!
        }
    }

    public int getCounter() {
        return counter;
    }
}
```

#### ReentrantReadWriteLock

Более тонкая альтернатива ReentrantLock.

- readLock() — несколько потоков могут читать одновременно.

- writeLock() — только один поток может писать, блокирует читателей.

```java
import java.util.concurrent.locks.ReentrantReadWriteLock;

class DataStore {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private String data = "init";

    public void write(String newData) {
        rwLock.writeLock().lock();
        try {
            data = newData;
        } finally {
            rwLock.writeLock().unlock();
        }
    }

    public String read() {
        rwLock.readLock().lock();
        try {
            return data;
        } finally {
            rwLock.readLock().unlock();
        }
    }
}
```

#### Semaphore

Ограничивает количество потоков, которые могут одновременно использовать ресурс.

Пример: пускаем только 3 потока в "критическую секцию":

```java
import java.util.concurrent.Semaphore;

class Printer {
    private final Semaphore semaphore = new Semaphore(3);

    public void print(String job) {
        try {
            semaphore.acquire(); // ждём свободный "разрешитель"
            System.out.println("Печатаю: " + job);
            Thread.sleep(500);
        } catch (InterruptedException ignored) {
        } finally {
            semaphore.release(); // освобождаем
        }
    }
}
```

#### CountDownLatch

Механизм одноразового обратного отсчёта: поток ждёт, пока счётчик не дойдёт до нуля.

Пример: главный поток ждёт завершения 3 потоков:

```java
import java.util.concurrent.CountDownLatch;

class Task implements Runnable {
    private final CountDownLatch latch;

    Task(CountDownLatch latch) {
        this.latch = latch;
    }

    public void run() {
        System.out.println(Thread.currentThread().getName() + " работает");
        try { Thread.sleep(500); } catch (InterruptedException ignored) {}
        latch.countDown(); // уменьшаем счётчик
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(3);
        for (int i = 0; i < 3; i++) {
            new Thread(new Task(latch)).start();
        }
        latch.await(); // ждём нуля
        System.out.println("Все задачи завершены!");
    }
}
```

#### CyclicBarrier, Phaser, Exchanger

CyclicBarrier - Похож на CountDownLatch, но многоразовый: потоки ждут друг друга, пока все не соберутся.

Phaser - Похож на CyclicBarrier, но более гибкий: поддерживает несколько фаз.

Exchanger - Позволяет двум потокам обменяться данными.

| Механизм                   | Для чего нужен                                                 |
| -------------------------- | -------------------------------------------------------------- |
| **ReentrantLock**          | Альтернатива synchronized, поддержка tryLock, таймаутов        |
| **ReentrantReadWriteLock** | Оптимизация чтения/записи (несколько читателей, один писатель) |
| **Semaphore**              | Ограничение количества потоков, доступ к ресурсу               |
| **CountDownLatch**         | Одноразовый обратный отсчёт                                    |
| **CyclicBarrier**          | Многоразовый барьер для синхронизации группы потоков           |
| **Phaser**                 | Более гибкий барьер с фазами                                   |
| **Exchanger**              | Обмен данными между двумя потоками                             |

### Пул потоков (Executors)

- **Пул потоков** — это набор заранее созданных потоков, которые многократно используются для выполнения задач.
- Вместо создания нового `Thread` под каждую задачу → задачи передаются пулу, и он распределяет их по имеющимся потокам.
- Позволяет:
    - уменьшить накладные расходы (создание/уничтожение потоков дорого),
    - контролировать количество параллельных потоков,
    - управлять временем жизни потоков.

#### Интерфейсы

**`Executor`**
- Базовый интерфейс для запуска задач.
- Один метод:
```java
void execute(Runnable command);
```

**`ExecutorService`**

Расширяет Executor, добавляет методы для управления пулом:

- submit() — передать задачу, получить Future.

- invokeAll() — выполнить список задач, вернуть список Future.

- invokeAny() — выполнить список задач, вернуть результат первой завершённой задачи.

- Методы завершения: shutdown(), awaitTermination().

#### Фабричные методы Executors

`newFixedThreadPool(int n)`

Пул фиксированного размера. Используется для равномерной загрузки.
```java
ExecutorService pool = Executors.newFixedThreadPool(4);
```

`newCachedThreadPool()`

Пул с неограниченным количеством потоков, но простаивающие потоки удаляются. Хорош для множества мелких кратковременных задач.
```java
ExecutorService pool = Executors.newCachedThreadPool();
```

`newSingleThreadExecutor()`

Всегда один поток. Задачи выполняются последовательно.
```java
ExecutorService pool = Executors.newSingleThreadExecutor();
```

`newScheduledThreadPool(int n)`

Позволяет планировать задачи с задержкой или по расписанию.

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
```

#### Методы работы

`submit()`

Принимает Runnable или Callable, возвращает Future.
```java
Future<Integer> f = pool.submit(() -> 42);
System.out.println(f.get()); // 42
```
`invokeAll()`

Выполняет список Callable, возвращает список Future.
```java
List<Callable<Integer>> tasks = Arrays.asList(
() -> 1, () -> 2, () -> 3
);
List<Future<Integer>> results = pool.invokeAll(tasks);
```
`invokeAny()`

Выполняет список Callable, возвращает результат первой успешно завершившейся задачи.
```java
Integer result = pool.invokeAny(tasks);
```

#### Callable и Future

`Callable<T>` — аналог `Runnable`, но возвращает результат и может кидать исключения:
```java
Callable<Integer> task = () -> 42;
```

`Future<T>` — объект для получения результата асинхронной задачи:

- get() — получить результат (блокирует поток).

- cancel() — отменить задачу.

- isDone() — проверка завершения.

`FutureTask<T>` — класс, который одновременно реализует Runnable и Future.

#### Завершение пула

`shutdown()` — больше не принимает новые задачи, выполняет уже принятые.

`shutdownNow()` — пытается прервать все текущие задачи.

`awaitTermination(timeout, unit)` — ждёт завершения задач в течение времени.

```java
pool.shutdown();
if (!pool.awaitTermination(5, TimeUnit.SECONDS)) {
    pool.shutdownNow();
}
```

### Атомарные операции и неблокирующие структуры

#### Атомарные операции

Пакет `java.util.concurrent.atomic`.

Предоставляет классы для **атомарных переменных**, которые работают без блокировок.

**Основные классы**
- `AtomicInteger`, `AtomicLong`, `AtomicBoolean` — атомарные примитивы.
- `AtomicReference<T>` — атомарная работа с объектом.
- `AtomicStampedReference<T>` — атомарная работа с объектом + версия (решает проблему **ABA**).
- `AtomicMarkableReference<T>` — атомарная работа с объектом + флаг.

**Методы**
- `get()` / `set()` — получить/установить значение.
- `incrementAndGet()`, `decrementAndGet()` — инкремент/декремент.
- `compareAndSet(expected, new)` — атомарно сравнить и заменить.

---

#### CAS (Compare-And-Set)

**CAS (Compare-And-Swap/Set)** — низкоуровневый механизм синхронизации.

Принцип:
1. Поток читает текущее значение `v`.
2. Сравнивает с ожидаемым `expected`.
3. Если совпадает → записывает новое `newValue`.
4. Если нет → повторяет попытку.

```java
AtomicInteger counter = new AtomicInteger(0);

// атомарный инкремент через CAS
while (true) {
    int oldValue = counter.get();
    int newValue = oldValue + 1;
    if (counter.compareAndSet(oldValue, newValue)) {
        break; // успешно обновили
    }
}
```
Преимущество: нет блокировок.

Недостаток: возможен "спин" (много повторов при высокой конкуренции).

---

#### Concurrent-коллекции

`Пакет java.util.concurrent` предоставляет коллекции, работающие без полного блокирования.

Основные:

**ConcurrentHashMap<K,V>** 
- Потокобезопасный аналог HashMap.

- Делит хранилище на сегменты → уменьшает конкуренцию.

- Методы: putIfAbsent, computeIfAbsent, merge, forEach, reduce.

**CopyOnWriteArrayList<E>** 
- Потокобезопасный список.

- При изменении создаётся копия массива.

- Эффективен при много чтений, мало записей.

**CopyOnWriteArraySet<E>** 
- На основе CopyOnWriteArrayList.

**ConcurrentLinkedQueue<E>** 
- Неблокирующая очередь (на CAS).

- Подходит для очередей с высокой конкуренцией.

**ConcurrentSkipListMap<K,V>** и **ConcurrentSkipListSet<E>** 
- На основе skip list (сбалансированные структуры, упорядоченные).

**BlockingQueue<E>** и её реализации:

- `ArrayBlockingQueue` — фиксированный размер, блокирующая.

- `LinkedBlockingQueue` — на связках.

- `PriorityBlockingQueue` — с приоритетом.

- `DelayQueue` — элементы доступны только по истечении времени.

### Асинхронные вычисления: CompletableFuture.

`CompletableFuture` - это:
- Класс из java.util.concurrent (Java 8+).
- Реализует асинхронные вычисления (Future + колбэки).
- Позволяет писать цепочки асинхронного кода без ручного управления потоками.

**Проблема обычного Future**

```java
Future<Integer> future = executor.submit(() -> {
    Thread.sleep(1000);
    return 42;
});
Integer result = future.get(); // блокирует поток!
```
 
**Решение CompletableFuture**

```java
import java.util.concurrent.*;

public class CompletableFutureExample {
    public static void main(String[] args) throws Exception {
        CompletableFuture<Integer> future =
            CompletableFuture.supplyAsync(() -> {
                // выполняется в другом потоке
                System.out.println("Работаем в " + Thread.currentThread().getName());
                return 42;
            });

        // Не блокирующее продолжение
        future.thenAccept(result -> 
            System.out.println("Результат: " + result)
        );

        Thread.sleep(2000); // ждем, чтобы асинхронка успела выполниться
    }
}
```

#### Основные методы CompletableFuture

**Создание**

- `runAsync(Runnable)` → выполняет задачу без возврата значения.

- `supplyAsync(Supplier<T>)` → выполняет задачу и возвращает результат.

Можно передать Executor (пул потоков), иначе используется ForkJoinPool.commonPool().

**Обработка результата**

- `thenApply(fn)` → применяет функцию к результату (возвращает новый CompletableFuture).

- `thenAccept(consumer)` → выполняет действие (ничего не возвращает).

- `thenRun(runnable)` → просто запускает действие после завершения.

**Асинхронные цепочки**

```java
CompletableFuture.supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenApply(String::toUpperCase)
    .thenAccept(System.out::println);

// Вывод HELLO WORLD
```

**Комбинирование**

- `thenCombine()` → объединяет два будущих.

- `thenCompose()` → плоское объединение (чтобы избежать CompletableFuture<CompletableFuture<T>>).

- `allOf()` → ждет все.

- `anyOf()` → ждет первое.

```java
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(() -> 2);
CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(() -> 3);

CompletableFuture<Integer> sum = f1.thenCombine(f2, (a, b) -> a + b);

System.out.println(sum.get()); // 5
```
**Обработка ошибок**

- `exceptionally(ex -> значение)` → если ошибка, вернуть дефолт.

- `handle((result, ex) -> ...)` → универсальная обработка.

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
    if (true) throw new RuntimeException("Ошибка");
    return 42;
}).exceptionally(ex -> {
    System.out.println("Перехватили: " + ex);
    return -1;
});

System.out.println(future.get()); // -1
```