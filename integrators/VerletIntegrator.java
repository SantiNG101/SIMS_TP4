

public class VerletIntegrator implements Integrator {
    @Override
    public void step(Particle[] p, double dt, ForceCalculator fc) {
        int n = p.length;
        Vector[] prev = new Vector[n];
        for (int i=0;i<n;i++) prev[i] = new Vector(p[i].r.x, p[i].r.y, p[i].r.z);
        for (int i=0;i<n;i++) {
            if (Math.abs(p[i].r2.x)+Math.abs(p[i].r2.y)+Math.abs(p[i].r2.z) < 1e-12) {
                p[i].r2 = p[i].r.sub(p[i].v.mul(dt));
            }
        }
        fc.computeForces(p);
        for (int i=0;i<n;i++) {
            Vector newr = p[i].r.mul(2.0).sub(p[i].r2).add(p[i].a.mul(dt*dt));
            Vector newv = newr.sub(p[i].r2).mul(1.0/(2.0*dt));
            p[i].r2.set(prev[i]);
            p[i].r.set(newr);
            p[i].v.set(newv);
        }
    }

    @Override
    public String name() {
        return "Verlet";
    }
}
