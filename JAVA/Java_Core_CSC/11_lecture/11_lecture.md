# Многопоточность в Java

### Законы

**Закон Амдала** — это формула, описывающая максимальное ускорение программы при распараллеливании.

Он говорит: ускорение ограничено той частью программы, которую нельзя параллелить.

S(N) = 1 / ((1 - P) + P/N), где  
S(N) - ускорение при использовании N потоков.  
P - доля программы, которую можно распараллелить (от 0 до 1).

**Universal Scalability Law (Gunther)**  
Джон Гюнтер расширил закон Амдала, добавив реалистичные ограничения многопоточности:
- Contention (соперничество за ресурс) — потоки делят общий ресурс (например, доступ к БД).
- Coherency delay (задержки согласования) — потоки должны обмениваться данными (например, синхронизация, кеши процессора). 

S(N) = N / (1 + α(N-1) + βN(N-1)), где  
α — коэффициент соперничества за ресурс (contention).  
β — коэффициент согласования между потоками (coherency).  

### Разделяемый ресурс

Разделяемый ресурс (shared resource) — это любая сущность, к которой могут обращаться несколько потоков одновременно.

- Память (переменные, коллекции, объекты).

- Файлы.

- Сокеты.

- Базы данных.

- Аппаратные устройства (например, принтер).

Проблема: если несколько потоков одновременно изменяют ресурс без синхронизации, возникает состояние гонки (race condition).
Пример: два потока одновременно увеличивают counter++. В итоге вместо 2 мы можем получить 1, потому что операция ++ не атомарная.

#### Виды доступа к разделяемым ресурсам

**Блокирующий доступ**

- Поток останавливается (блокируется), если ресурс занят другим потоком.

- Основан на замках (locks) или synchronized.

- Простой, безопасный, но может приводить к пробкам и deadlock’ам.

```java
class Shared {
    private int counter = 0;

    public synchronized void increment() {
        counter++;
    }

    public synchronized int getCounter() {
        return counter;
    }
}

// Здесь synchronized гарантирует, что в метод в один момент попадёт только один поток.
```

**Неблокирующий доступ (Non-blocking)**

- Поток не блокируется, если ресурс занят, он пытается выполнить операцию снова или идёт дальше.

- Обычно строится на атомарных операциях (CAS — compare-and-swap).

- Высокая производительность при большом числе потоков.

---

**Виды блокирующего доступа**

1. Взаимное исключение (Mutex, synchronized, Lock)

   - Только один поток получает доступ к ресурсу.

   - Остальные ждут.

   - Пример: ReentrantLock.

2. Читатели–писатели (ReadWriteLock)

   - Несколько потоков могут читать одновременно.

   - Запись возможна только в одиночку.

   - Оптимально для коллекций, где чаще читают, чем пишут.


**Виды неблокирующего доступа**

1. Lock-free

   - Нет блокировок.

   - Гарантия: хотя бы один поток завершит операцию за конечное время.

   - Пример: `ConcurrentLinkedQueue`.

2. Wait-free

   - Гарантия: каждый поток завершит операцию за конечное число шагов.

   - Редко реализуется, очень сложно, но самое предсказуемое.

### Теория

**Видимость (Visibility)**

Когда несколько потоков работают с одной переменной, изменения, сделанные одним потоком, могут не быть видны другим.
Причина: каждый поток может кэшировать значения переменных в своих регистрах или в кэше процессора, а не сразу обновлять их в памяти.

```java
class Example {
    private static boolean running = true;

    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            while (running) { // поток может не увидеть обновление running
            }
            System.out.println("Stopped");
        });
        t.start();

        Thread.sleep(1000);
        running = false; // главный поток меняет значение
    }
}
```

Решение: volatile гарантирует видимость изменений.

**Атомарность (Atomicity)**

Атомарная операция — это операция, которая выполняется полностью или не выполняется вообще (неделимая).

```java
class Counter {
    private int count = 0;

    public void increment() {
        count++; // НЕ атомарно
    }

    public int get() {
        return count;
    }
}
// Если несколько потоков делают increment(), то часть инкрементов теряется.
```

Решение: synchronized методы/блоки или AtomicInteger

**Потокобезопасность (Thread-safety)**

Потокобезопасный код — это код, который работает правильно при одновременном доступе из нескольких потоков.

**Java Memory Model (JMM)**

Это формальная модель памяти в Java, которая определяет:

- как потоки видят изменения в переменных;

- какие гарантии даёт volatile, synchronized, final;

- правила happens-before (что гарантированно видно другим потокам).

Основные гарантии JMM:
1. Volatile

    - Чтение/запись volatile переменной всегда видны всем потокам.

    - Операции записи volatile устанавливают "барьер памяти".

2. Synchronized

    - Вход в синхронизированный блок → сбрасывает кэш и видит последние изменения.

    - Выход → записывает изменения в память.

3. Happens-before

    - Если операция A happens-before операции B, то все изменения, сделанные до A, будут видны в B.


### Thread и synchronized

#### Класс `Thread`

В Java поток (thread) — это независимая единица выполнения внутри программы.
Каждая программа на Java всегда запускается хотя бы с одним потоком — main thread.

Существует два варианта создания потока. Первый с помощью наследования:

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("Привет из потока " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) {
        Thread t1 = new MyThread();
        t1.start(); // запускаем поток
    }
}
```

Второй способ через реализацию интерфейса Runnable:

```java
class MyTask implements Runnable {
    public void run() {
        System.out.println("Выполняется задача в " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(new MyTask());
        t.start();
    }
}
```

Лучше использовать Runnable, так как поддерживается множественное наследование интерфейсов.

Лямбда-вариант (короче всего):

```java
public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(() -> {
            System.out.println("Выполняется задача через лямбду");
        });
        t.start();
    }
}
```

Управление потоком:

- `start()` — запускает новый поток.

- `join()` — заставляет текущий поток ждать завершения другого.

- `sleep(ms)` — усыпляет поток.

- `yield()` — поток добровольно отдаёт управление другим.

- `interrupt()` — сигнал прерывания (но не мгновенная остановка).

#### Ключевое слово synchronized

`synchronized` — это ключевое слово, которое гарантирует:
- Взаимное исключение (mutual exclusion) — в блок кода или метод в один момент времени может войти только один поток.
- Согласованность памяти (memory visibility) — изменения, сделанные одним потоком, видны другим.

```java
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;  // потокобезопасное увеличение
    }

    public synchronized int getCount() {
        return count;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });

        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Результат: " + counter.getCount()); // всегда 2000
    }
}
```

Можно синхронизировать не весь метод, а только часть кода:

```java
class Counter {
    private int count = 0;

    public void increment() {
        synchronized (this) { // монитор — текущий объект
            count++;
        }
    }
}
```
**Объектная блокировка**

Каждый объект в Java имеет монитор (внутренный замок).
- synchronized работает именно через монитор:

- synchronized (obj) → поток получает замок объекта obj.

- Если замок уже у другого потока → текущий поток блокируется.

Проблемы и ограничения synchronized:

- Может привести к deadlock (взаимной блокировке), если несколько потоков ждут замки друг друга.

- Нет возможности гибко управлять (например, таймаут ожидания).

- Может быть медленнее, чем атомарные переменные (AtomicInteger) или Lock.

### Ключевое слово `volatile`

volatile — это модификатор переменной, который даёт гарантию видимости изменений переменной между потоками.

Когда переменная объявлена как volatile, это значит:

- Каждый поток читает её всегда из основной памяти (RAM), а не из кэша процессора или локального кэша потока.

- Каждая запись в переменную сразу же "сбрасывается" в основную память.

- Но важно: volatile НЕ гарантирует атомарность (например, counter++ всё равно небезопасен).

```java
class Example {
    private static volatile boolean running = true;

    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            while (running) { // всегда читаем из памяти
            }
            System.out.println("Stopped");
        });

        t.start();
        Thread.sleep(1000);
        running = false; // сразу видно в другом потоке
    }
}
```

### Singletom

`Singleton` — это шаблон проектирования, когда у класса есть только один объект (экземпляр) во всей программе, и к нему можно глобально обращаться.

#### Singleton (Lazy) — ленивый (НЕ потокобезопасный)

```java
public class SingletonLazy {
    private static SingletonLazy instance; // пока null

    private SingletonLazy() {} // приватный конструктор

    public static SingletonLazy getInstance() {
        if (instance == null) {   // создаём при первом обращении
            instance = new SingletonLazy();
        }
        return instance;
    }
}

// Проблема: если два потока одновременно вызовут getInstance(), оба могут создать объект.
```

#### Singleton (Lazy, Thread-Safe) — с synchronized
Добавляем synchronized к методу.
Теперь два потока не создадут разные экземпляры.
Но каждый вызов метода блокируется, что замедляет работу.

```java
public class SingletonThreadSafe {
    private static SingletonThreadSafe instance;

    private SingletonThreadSafe() {}

    public static synchronized SingletonThreadSafe getInstance() {
        if (instance == null) {
            instance = new SingletonThreadSafe();
        }
        return instance;
    }
}
```

#### Singleton (Double-Checked Locking) — оптимизированный

Используем volatile + проверку дважды.
Сначала проверяем без блокировки.
Только если объект null, входим в synchronized.
Внутри синхронизированного блока снова проверяем null (на случай, если другой поток уже создал объект).

```java
public class SingletonDCL {
    private static volatiles SingletonDCL instance; // volatile важно!

    private SingletonDCL() {}

    public static SingletonDCL getInstance() {
        if (instance == null) {  // 1-я проверка (без блокировки)
            synchronized (SingletonDCL.class) {
                if (instance == null) { // 2-я проверка (с блокировкой)
                    instance = new SingletonDCL();
                }
            }
        }
        return instance;
    }
}
```