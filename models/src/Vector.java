public class Vector {
    public double x, y, z;

    public Vector() {
        this(0,0,0);
    }

    public Vector(double x, double y, double z) {
        this.x=x;
        this.y=y;
        this.z=z;
    }

    public Vector add(Vector o) {
        return new Vector(x+o.x, y+o.y, z+o.z);
    }

    public Vector sub(Vector o) {
        return new Vector(x-o.x, y-o.y, z-o.z);
    }

    public Vector mul(double s) {
        return new Vector(x*s, y*s, z*s);
    }

    @Override
    public String toString() { return String.format("(%.6g,%.6g,%.6g)", x,y,z); }
}

