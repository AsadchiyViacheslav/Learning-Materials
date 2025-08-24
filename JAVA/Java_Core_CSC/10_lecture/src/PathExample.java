import java.io.IOException;
import java.nio.file.*;

public class PathExample {
    public static void main(String[] args) throws IOException {
        Path p1 = Paths.get("data.txt");              // относительный путь
        Path p2 = Paths.get("/tmp/logs/app.log");     // абсолютный путь
        Path p3 = Paths.get(System.getProperty("user.home"), "docs", "file.txt"); // из нескольких сегментов

        System.out.println(p1.getFileName());   // data.txt
        System.out.println(p2.getParent());     // /tmp/logs
        System.out.println(p2.toAbsolutePath());
        System.out.println(p2.toRealPath());    // Канонический путь (разворачивает ссылки, . и ..)


        // Проверка существования и свойств
        Path file = Paths.get("data.txt");

        // Проверки
        boolean exists = Files.exists(file);
        boolean isFile = Files.isRegularFile(file);
        boolean isDir  = Files.isDirectory(file);
        boolean readable = Files.isReadable(file);
        boolean writable = Files.isWritable(file);
        boolean executable = Files.isExecutable(file);


        // Создание, удаление, копирование и перемещение
        Path dir = Paths.get("out/logs");
        Files.createDirectories(dir);  // создает все каталоги цепочки

        Path f = dir.resolve("app.log");
        Files.createFile(f);           // создает пустой файл

        // Копирование
        Path copy = dir.resolve("app_copy.log");
        Files.copy(f, copy, StandardCopyOption.REPLACE_EXISTING);

        // Перемещение / Переименование
        Path target = dir.resolve("app_new.log");
        Files.move(f, target, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);

        // Удаление
        Files.delete(target);          // исключение, если нет файла
        Files.deleteIfExists(copy);    // безопасно, если нет файла



        // Перечисление содержимого каталога
        Path dir2 = Paths.get("out");

        // DirectoryStream — эффективный перебор
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir2, "*.log")) {
            for (Path entry : stream) {
                System.out.println(entry.getFileName());
            }
        }

    }
}
