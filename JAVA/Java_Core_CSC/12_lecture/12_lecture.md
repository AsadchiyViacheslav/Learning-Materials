# Java: примитивы синхронизации, конкурентные коллекции

Проблемы: Dead lock, Live lock, Race condition, Starvation

Высокоуровневые механизмы синхронизации (java.util.concurrent)
ReentrantLock (чем лучше/хуже synchronized).
ReentrantReadWriteLock.
Semaphore, CountDownLatch, CyclicBarrier.
Phaser.
Exchanger.


Пул потоков (Executors)
Интерфейс Executor, ExecutorService.
newFixedThreadPool, newCachedThreadPool, newSingleThreadExecutor, newScheduledThreadPool.
Методы submit(), invokeAll(), invokeAny().
Callable и Future, FutureTask.
Завершение пула (shutdown(), awaitTermination()).

Атомарные операции и неблокирующие структуры
Пакет java.util.concurrent.atomic:
AtomicInteger, AtomicLong, AtomicReference.
CAS (Compare-And-Set) — принцип работы.
LongAdder / LongAccumulator (лучше масштабируются).
Concurrent-коллекции:
ConcurrentHashMap,
CopyOnWriteArrayList,
ConcurrentLinkedQueue.


Асинхронные вычисления: CompletableFuture.
 