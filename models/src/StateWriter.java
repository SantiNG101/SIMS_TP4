import java.io.*;
import java.util.Locale;

public class StateWriter {
    private PrintWriter out;

    public StateWriter(String file) throws IOException {
        out = new
                PrintWriter(new FileWriter(file));
        out.println("time,id,x,y,z,vx,vy,vz");
    }

    public void write(double t, Particle[] particles) {
        for (Particle p : particles) {
            out.printf(Locale.US, "%.6g,%d,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g\n", t, p.id,
                    p.r.x, p.r.y, p.r.z, p.v.x, p.v.y, p.v.z);
        }
    }

    public void close() {
        out.close();
    }
}

