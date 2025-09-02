# Java: Что внутри?

### Общая архитектура Java
Экосистема из инструментов и сред, которые обеспечивают написание, компиляцию, выполнение и сопровождение Java-программ.

![Scheme of Java](https://i.pinimg.com/736x/27/5f/d7/275fd7ede464b00adeb64635658e9e31.jpg)

**JVM (Java Virtual Machine)**

Это виртуальная машина, которая исполняет байт-код Java.

Она не понимает исходный код (.java), а работает с байт-кодом (.class).

JVM отвечает за:

- загрузку классов,

- выполнение байт-кода,

- управление памятью (включая сборку мусора),

- безопасность и изоляцию кода.

JVM бывает разных реализаций (HotSpot, OpenJ9, GraalVM и др.), но у всех общий интерфейс — спецификация JVM.

2. JRE (Java Runtime Environment)

Это среда выполнения Java.

Состоит из:

JVM,

библиотек Java Class Library (JCL),

вспомогательных файлов (например, rt.jar в старых версиях).

То есть JRE нужен, чтобы запускать готовые Java-программы.

В JRE нет компилятора javac и других девелоперских инструментов.

3. JDK (Java Development Kit)

Это набор для разработчика, в него входит:

JRE (а значит и JVM + стандартные библиотеки),

инструменты для разработки (компилятор javac, отладчик jdb, утилиты jar, javadoc, jconsole и т. д.).

Если тебе надо писать код — нужен JDK.

Если только запускать код — достаточно JRE.
(хотя в современных версиях Oracle/OpenJDK JRE как отдельный пакет уже не выпускается, в JDK встроен runtime).

4. Java Class Library (JCL)

Это стандартные библиотеки Java, которые предоставляют базовые API:

коллекции (java.util),

ввод/вывод (java.io, java.nio),

работа с сетью (java.net),

работа с многопоточностью (java.util.concurrent),

и многое другое.

Фактически это вторая половина языка: без библиотек ты бы писал очень низкоуровневый код.

5. Java Development Tools

Это утилиты, которые входят в JDK:

javac — компилятор из .java в .class,

java — запуск программы,

jar — упаковка классов и ресурсов в .jar-архив,

javadoc — генерация документации,

jdb — отладчик,

плюс куча вспомогательных.









.class -> Class loader subsystem(loading, linking, initialization) -> runtime data area (heap, method area, stack, pc register, native method stack) -> execution engine (interpreter, jit compiler, garbage collector)-> jni -> native method library

![JVM Architecture](https://avatars.dzeninfra.ru/get-zen_doc/9505890/pub_642424dd9b2074611901dd26_642428f02f2d5107b7ba9974/scale_1200)
ClassLoader

Верификация класса, Инициализация класса

Пул констант

Сигнатуры полей, сигнатуры методов, Атрибуты класса, Поле, Инициализация полей, Метод, Код, Байткод, Инструкции

Garbage collection (Generational GC, Copying, Regionalized copying, Mark and sweep vs mark and compact, Parallel/concurrent GC, Java garbage collectors, TLAB аллокация

