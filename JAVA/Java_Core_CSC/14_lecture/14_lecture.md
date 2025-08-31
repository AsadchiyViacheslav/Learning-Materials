# Java: Что внутри?

Общая структура работы Java
![Scheme of Java](https://i.pinimg.com/736x/27/5f/d7/275fd7ede464b00adeb64635658e9e31.jpg)

.class -> Class loader subsystem(loading, linking, initialization) -> runtime data area (heap, method area, stack, pc register, native method stack) -> execution engine (interpreter, jit compiler, garbage collector)-> jni -> native method library

![JVM Architecture](https://avatars.dzeninfra.ru/get-zen_doc/9505890/pub_642424dd9b2074611901dd26_642428f02f2d5107b7ba9974/scale_1200)
ClassLoader

Верификация класса, Инициализация класса

Пул констант

Сигнатуры полей, сигнатуры методов, Атрибуты класса, Поле, Инициализация полей, Метод, Код, Байткод, Инструкции

Garbage collection (Generational GC, Copying, Regionalized copying, Mark and sweep vs mark and compact, Parallel/concurrent GC, Java garbage collectors, TLAB аллокация

