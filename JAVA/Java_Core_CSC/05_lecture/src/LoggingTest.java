import java.util.logging.Level;
import java.util.logging.Logger;

public class LoggingTest {
    private static final Logger LOG = Logger.getLogger(LoggingTest.class.getName());

    public void function() {

    }
    public void identifyPrincipalEvent() {
        try {
           function();
        }
        catch(Exception ex) {
            LOG.log(Level.SEVERE, "Error while doing function", ex);
        }
    }
}
