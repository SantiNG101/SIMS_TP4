import java.io.*;
import java.util.List;
import java.util.Locale;

public class MDOutput {
    private BufferedWriter writer;

    public void open(String fname) throws IOException {
        writer = new BufferedWriter(new FileWriter(fname));
        writer.write("# time,id,x,y,z,vx,vy,vz\n");
    }

    public void write(double t, List<Particle> particles) throws IOException {
        for (Particle p : particles) {
            writer.write(String.format(Locale.US,"%.6g,%d,%.12g,%.12g,%.12g,%.12g,%.12g,%.12g\n",
                    t, p.id, p.r.x,p.r.y,p.r.z,p.v.x,p.v.y,p.v.z));
        }
    }

    public void close() throws IOException {
        if(writer!=null){
            writer.flush();writer.close();
        }
    }
}

