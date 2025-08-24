import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

public class FileExample {

    // Создать директорию, файл и записать в него
    public void createDirectoryFile() throws IOException {
        File dir = new File("out");
        if (!dir.exists() && !dir.mkdirs()) {
            throw new IOException("Не удалось создать каталог: " + dir);
        }
        File file = new File(dir, "hello.txt");
        if (file.createNewFile()) {
            try (OutputStream os = new FileOutputStream(file)) {
                os.write("Привет, файл!\n".getBytes());
            }
        }
    }

    // Рекурсивно обойти каталог и распечатать дерево
    public static void walk(File root, int level) {
        if (root == null || !root.exists()) return;
        System.out.println("  ".repeat(level) + (root.isDirectory() ? "[D] " : "[F] ") + root.getName());
        if (root.isDirectory()) {
            File[] children = root.listFiles();
            if (children != null) {
                for (File c : children) walk(c, level + 1);
            }
        }
    }

    // Удалить директорию с содержимым
    public static boolean deleteRecursively(File f) {
        if (f.isDirectory()) {
            File[] children = f.listFiles();
            if (children != null) {
                for (File c : children) {
                    if (!deleteRecursively(c)) return false;
                }
            }
        }
        return f.delete();
    }

}
