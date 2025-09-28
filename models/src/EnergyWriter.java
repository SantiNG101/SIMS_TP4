import java.io.*;
import java.util.Locale;

public class EnergyWriter {
    private PrintWriter out;

    public EnergyWriter(String file, String header) throws IOException {
        out = new PrintWriter(new FileWriter(file));
        out.println("time," + header);
    }

    public void write(double t, double... vals) {
        out.printf(Locale.US, "%.6g", t);
        for (double v : vals) out.printf(",%.6g", v);
        out.println();
    }

    public void close() {
        out.close();
    }
}

