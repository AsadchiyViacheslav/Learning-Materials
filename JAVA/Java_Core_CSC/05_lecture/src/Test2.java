import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Test2 {
    static class MyException extends Exception {
        public MyException(String message) { super(message); }

        public MyException(String message, Throwable cause) {
            super(message, cause);
        }
    }

    public static void main(String[] args) throws MyException {
        try {
            byte[] bytes = Files.readAllBytes(Paths.get("/etc/passwd"));
        }
        catch (IOException e) {
            throw new MyException("Ошибка чтения", e);
        }
    }
}
