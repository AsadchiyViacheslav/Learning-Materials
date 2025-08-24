# Ввод-вывод

Потоковый ввод-вывод (java.io):
- InputStream - читать байты
- OutputStream - писать байты
- Reader - читать символы
- Writer - писать символы

### InputStream

InputStream — это абстрактный класс в пакете java.io.

Используется для чтения последовательности байтов из источника: файл, сеть, массив, клавиатура и т.д.

**Основные методы**

| Метод                                  | Описание                                                                                                  |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `int read()`                           | Читает **один байт** и возвращает его как `int` (0–255). Возвращает `-1`, если конец потока.              |
| `int read(byte[] b)`                   | Читает **несколько байтов** и записывает в массив `b`. Возвращает количество прочитанных байтов или `-1`. |
| `int read(byte[] b, int off, int len)` | Читает до `len` байтов и записывает в массив начиная с позиции `off`.                                     |
| `long skip(long n)`                    | Пропускает `n` байтов.                                                                                    |
| `int available()`                      | Сколько байтов доступно для чтения без блокировки.                                                        |
| `void close()`                         | Закрывает поток и освобождает ресурсы.                                                                    |

#### Подклассы

`FileInputStream` — чтение байтов из файла.

```java
FileInputStream fis = new FileInputStream("example.txt");
int b;
while ((b = fis.read()) != -1) {
    System.out.print((char) b);
}
fis.close();
```

`ByteArrayInputStream` — чтение из массива байтов.

```java
byte[] data = {65, 66, 67}; // A, B, C
ByteArrayInputStream bis = new ByteArrayInputStream(data);
int b;
while ((b = bis.read()) != -1) {
    System.out.print((char) b);
    }
```

`BufferedInputStream` — буферизированный поток для ускорения чтения. (читаем блоками, а не по одному байту)
```java
BufferedInputStream bis = new BufferedInputStream(new FileInputStream("example.txt"));
int b;
while ((b = bis.read()) != -1) {
    System.out.print((char) b);
}
bis.close();
```

`DataInputStream` — позволяет читать примитивные типы (int, double) из потока.

```java
DataInputStream dis = new DataInputStream(new FileInputStream("data.bin"));
int num = dis.readInt();
double d = dis.readDouble();
dis.close();
```

`ObjectInputStream` - позволяет читать сериализации объектов.

### OutputStream

OutputStream — это абстрактный класс из пакета java.io

Используется для записи байтов (а не символов).

**Основные методы**

| Метод                                    | Описание                                                                               |
| ---------------------------------------- | -------------------------------------------------------------------------------------- |
| `void write(int b)`                      | Записывает один байт (`0–255`).                                                        |
| `void write(byte[] b)`                   | Записывает весь массив байтов.                                                         |
| `void write(byte[] b, int off, int len)` | Записывает часть массива: `len` байтов начиная с `off`.                                |
| `void flush()`                           | Принудительно записывает данные из буфера (очень важно при работе с сетями и файлами). |
| `void close()`                           | Закрывает поток и освобождает ресурсы.                                                 |

#### Подклассы

`FileOutputStream` — запись байтов в файл

```java
try (FileOutputStream fos = new FileOutputStream("example.txt")) {
    String text = "Hello, world!";
    fos.write(text.getBytes()); // преобразуем строку в байты
} catch (IOException e) {
    e.printStackTrace();
}
```

`ByteArrayOutputStream` — запись в массив байтов в памяти

```java
ByteArrayOutputStream baos = new ByteArrayOutputStream();
baos.write("ABC".getBytes());
baos.write(68); // символ 'D'
byte[] result = baos.toByteArray(); 
System.out.println(new String(result)); // ABCD
```

`BufferedOutputStream` — буферизация записи

```java
try (BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream("buffered.txt"))) {
    for (int i = 0; i < 5; i++) {
        bos.write(("Line " + i + "\n").getBytes());
    }
    bos.flush(); // важно!
} catch (IOException e) {
    e.printStackTrace();
}
```

`DataOutputStream` — запись примитивных типов (int, double и т.д.)

```java
try (DataOutputStream dos = new DataOutputStream(new FileOutputStream("data.bin"))) {
    dos.writeInt(123);
    dos.writeDouble(45.67);
    dos.writeBoolean(true);
} catch (IOException e) {
    e.printStackTrace();
}
```

`ObjectOutputStream` — сериализация объектов

```java
try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("object.dat"))) {
    oos.writeObject("Hello");
    oos.writeObject(123);
} catch (IOException e) {
    e.printStackTrace();
}
```

### Reader

Reader — это абстрактный класс из пакета java.io.

Используется для чтения символов (в отличие от InputStream, который работает с байтами). Поддерживает Unicode, то есть можно читать не только ASCII, но и любые символы.

**Основные методы**

| Метод                                     | Описание                                                            |
| ----------------------------------------- | ------------------------------------------------------------------- |
| `int read()`                              | Читает один символ (возвращает `int`, -1 если конец файла).         |
| `int read(char[] cbuf)`                   | Читает символы в массив. Возвращает количество реально прочитанных. |
| `int read(char[] cbuf, int off, int len)` | Читает часть массива.                                               |
| `void close()`                            | Закрывает поток.                                                    |
| `boolean ready()`                         | Проверяет, можно ли читать (не всегда надёжен).                     |
| `long skip(long n)`                       | Пропускает `n` символов.                                            |
| `mark(int readAheadLimit)` / `reset()`    | Позволяют "откатиться" назад (не все реализации поддерживают).      |

#### Подклассы

`FileReader` — чтение текста из файла

```java
try (FileReader fr = new FileReader("text.txt")) {
    int ch;
    while ((ch = fr.read()) != -1) {
        System.out.print((char) ch);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

`BufferedReader` — чтение с буфером (ускоряет)

```java
try (BufferedReader br = new BufferedReader(new FileReader("text.txt"))) {
    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

`CharArrayReader` — чтение из массива символов

```java
char[] data = "Hello".toCharArray();
CharArrayReader car = new CharArrayReader(data);
int ch;
while ((ch = car.read()) != -1) {
    System.out.print((char) ch);
}
```

`StringReader` — чтение из строки

```java
try (StringReader sr = new StringReader("Java Reader Example")) {
    int ch;
    while ((ch = sr.read()) != -1) {
        System.out.print((char) ch);
    }
}
```

`InputStreamReader` — мост между байтовыми и символьными потоками

```java
try (InputStreamReader isr = new InputStreamReader(
         new FileInputStream("text.txt"), StandardCharsets.UTF_8)) {
    int ch;
    while ((ch = isr.read()) != -1) {
        System.out.print((char) ch);
    }
}
```

### Writer

Writer — это абстрактный класс из пакета java.io

Используется для записи символов (char и строк) в разные источники: файлы, массивы, строки, каналы и т.п.

**Основные методы**

| Метод                                       | Описание                                                            |
| ------------------------------------------- | ------------------------------------------------------------------- |
| `void write(int c)`                         | Записывает один символ.                                             |
| `void write(char[] cbuf)`                   | Записывает массив символов.                                         |
| `void write(char[] cbuf, int off, int len)` | Записывает часть массива.                                           |
| `void write(String str)`                    | Записывает строку.                                                  |
| `void write(String str, int off, int len)`  | Записывает часть строки.                                            |
| `Writer append(CharSequence csq)`           | Добавляет символы/строку в конец.                                   |
| `void flush()`                              | Принудительно выталкивает буфер в поток (важно!).                   |
| `void close()`                              | Закрывает поток (обязательно, иначе часть данных может потеряться). |

#### Подклассы

`FileWriter` — запись в файл

```java
try (FileWriter fw = new FileWriter("output.txt")) {
    fw.write("Привет, Java!\n");
    fw.write("Вторая строка.");
} catch (IOException e) {
    e.printStackTrace();
}
```

`BufferedWriter` — запись с буферизацией

```java
try (BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {
    bw.write("Первая строка");
    bw.newLine(); // перенос строки (кроссплатформенно)
    bw.write("Вторая строка");
}
```

`CharArrayWriter` — запись в массив символов (в памяти)

```java
CharArrayWriter caw = new CharArrayWriter();
caw.write("Hello World!");
System.out.println(caw.toString()); // Hello World!
```

`StringWriter` — запись в строку

```java
StringWriter sw = new StringWriter();
sw.write("Java ");
sw.append("Writer");
System.out.println(sw.toString()); // Java Writer
```

`PrintWriter` — удобный вывод (как System.out)

```java
try (PrintWriter pw = new PrintWriter("out.txt")) {
    pw.println("Привет");
    pw.printf("Формат: %d + %d = %d", 2, 3, 2 + 3);
}
```

`OutputStreamWriter` — мост между байтовыми и символьными потоками

```java
try (Writer writer = new OutputStreamWriter(
         new FileOutputStream("utf8.txt"), StandardCharsets.UTF_8)) {
    writer.write("Текст в UTF-8");
}
```

### java.io.File

`java.io.File` — это абстракция пути к файлу или каталогу (директории).

Создание new File(...) не создаёт сам файл/папку на диске — это только объект-указатель на путь.

```java
File f = new File("notes.txt");     // относительный путь (от "текущей" папки)
File abs = new File("/var/log/app"); // абсолютный путь (Unix-подобные)
```

**Проверки и свойства**

```java
File f = new File("data.bin");
f.exists();         // есть ли на диске
f.isFile();         // обычный файл?
f.isDirectory();    // каталог?
f.isHidden();       // скрытый (зависит от ОС)
f.length();         // размер файла в байтах (для директории обычно 0/неинформативно)
f.lastModified();   // timestamp (миллисекунды epoch)
f.canRead(); f.canWrite(); f.canExecute();    // права доступа (грубо)
```

**Пути и нормализация**

```java
f.getName();            // только имя (без пути)
f.getParent();          // строка-родитель или null
f.getAbsolutePath();    // абсолютный путь (без разрешения ссылок/..)
f.getCanonicalPath();   // канонический (разворачивает символические ссылки, . и ..)
File child = new File(f, "subdir/file.txt"); // путь = f/subdir/file.txt
```

**Создание/удаление/переименование**

```java
File dir = new File("out/logs");
dir.mkdir();       // создать один каталог
dir.mkdirs();      // создать всю цепочку каталогов

File file = new File(dir, "app.log");
file.createNewFile();   // создать пустой файл, true если создан, false если уже есть

File tmp = File.createTempFile("prefix-", ".tmp"); // временный файл в системном tmp
tmp.deleteOnExit(); // удалить при завершении JVM (осторожно: держит ссылку в памяти)

file.renameTo(new File(dir, "app-1.log")); // переименование/перемещение (boolean)
file.delete();     // удалить файл (или пустой каталог)
```

**Перечисление содержимого каталогов**

```java
File home = new File(System.getProperty("user.home"));

String[] names = home.list();                 // имена (может вернуть null)
File[] files = home.listFiles();              // объекты File (может вернуть null)

// Фильтрация по имени (только .txt)
String[] txt = home.list((dir, name) -> name.endsWith(".txt"));

// Фильтрация по File (только файлы размером > 1 МБ)
File[] bigFiles = home.listFiles(f2 -> f2.isFile() && f2.length() > 1_000_000);
```
### java.nio.file

Конечно! java.nio.file — это современный API для работы с файлами и путями, появившийся в Java 7 в рамках NIO.2. Он пришёл на смену устаревшему java.io.File, решая его ограничения и добавляя надёжность, производительность и удобство.

**Основные классы и интерфейсы**

| Класс / Интерфейс    | Назначение                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| `Path`               | Абстракция пути к файлу или директории (замена `File`)                                                   |
| `Paths`              | Фабрика для создания `Path` объектов (`Paths.get(...)`)                                                  |
| `Files`              | Статические методы для работы с файлами и директориями (чтение, запись, копирование, удаление, проверка) |
| `FileSystem`         | Представление файловой системы (полезно для работы с разными файловыми системами)                        |
| `FileSystems`        | Фабрика для получения `FileSystem` (обычно используем дефолтную)                                         |
| `StandardCopyOption` | Опции для копирования/перемещения файлов (`REPLACE_EXISTING`, `ATOMIC_MOVE`)                             |
| `StandardOpenOption` | Опции открытия файлов (`CREATE`, `APPEND`, `TRUNCATE_EXISTING`)                                          |
| `DirectoryStream`    | Итератор по содержимому каталога (эффективнее `File.listFiles`)                                          |
| `WatchService`       | Слежение за изменениями в директории (создание, удаление, модификация файлов)                            |


### URL и HttpClient

`java.net.URL` — это абстракция адреса в интернете, может представлять ресурсы по протоколам HTTP, HTTPS, FTP и т.д.

Пример:

```java
import java.net.URL;

public class URLExample {
    public static void main(String[] args) throws Exception {
        URL url1 = new URL("https://example.com");
        URL url2 = new URL("https", "example.com", 443, "/path/resource");

        System.out.println(url1.getProtocol()); // https
        System.out.println(url1.getHost());     // example.com
        System.out.println(url1.getPort());     // -1 (если порт не указан)
        System.out.println(url1.getPath());     // /
    }
}
```

Минусы URL:
- Нет удобных средств для POST-запросов, заголовков, таймаутов и асинхронного выполнения.
- Только синхронный доступ.

`java.net.http.HttpClient` — современный клиент для HTTP/HTTPS, поддерживает:
- GET, POST и другие методы
- Таймауты
- Асинхронные запросы (CompletableFuture)
- Настройку заголовков
- Redirect
- Работа с Body как String, Stream или File

Пример:

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class HttpClientExample {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://example.com"))
                .GET()
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Status code: " + response.statusCode());
        System.out.println("Body: " + response.body());
    }
}
```

Post запрос с телом:

```java
HttpRequest postRequest = HttpRequest.newBuilder()
        .uri(URI.create("https://example.com/api"))
        .POST(HttpRequest.BodyPublishers.ofString("{\"name\":\"John\"}"))
        .header("Content-Type", "application/json")
        .build();

HttpResponse<String> postResponse = client.send(postRequest, HttpResponse.BodyHandlers.ofString());
System.out.println(postResponse.body());
```