public class Vector {
    public double x, y, z;


    public Vector() {
        this(0, 0, 0);
    }

    public Vector(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }


    public Vector add(Vector o) {
        return new Vector(x + o.x, y + o.y, z + o.z);
    }

    public Vector sub(Vector o) {
        return new Vector(x - o.x, y - o.y, z - o.z);
    }

    public Vector mul(double s) {
        return new Vector(x * s, y * s, z * s);
    }

    public double norm() {
        return x * x + y * y + z * z;
    }

    public void set(Vector o) {
        x = o.x;
        y = o.y;
        z = o.z;
    }

    public void set(double nx, double ny, double nz) {
        x = nx;
        y = ny;
        z = nz;
    }

    @Override
    public String toString() {
        return String.format("(%.6g,%.6g,%.6g)", x, y, z);
    }
}


