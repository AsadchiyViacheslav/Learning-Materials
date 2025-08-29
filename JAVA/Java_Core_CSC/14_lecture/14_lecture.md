# Java: Что внутри?

Общая структура работы Java

.class -> Class loader subsystem(loading, linking, initialization) -> runtime data area (heap, method area, stack, pc register, native method stack) -> execution engine (interpreter, jit compiler, garbage collector)-> jni -> native method library

ClassLoader

Верификация класса, Инициализация класса

Пул констант

Сигнатуры полей, сигнатуры методов, Атрибуты класса, Поле, Инициализация полей, Метод, Код, Байткод, Инструкции

Garbage collection (Generational GC, Copying, Regionalized copying, Mark and sweep vs mark and compact, Parallel/concurrent GC, Java garbage collectors, TLAB аллокация

