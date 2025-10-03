public class VerletIntegrator implements Integrator {
    @Override
    public void step(Particle[] p, double dt, ForceCalculator fc) {
        int n = p.length;

        // Guardar posición actual
        Vector[] current = new Vector[n];
        for (int i = 0; i < n; i++) {
            current[i] = new Vector(p[i].r.x, p[i].r.y, p[i].r.z);
        }

        // Inicializar r_prev si es la primera vez
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            if (pi.r_prev == null) {
                pi.r_prev = pi.r.sub(pi.v.mul(dt)).add(pi.a.mul(0.5 * dt * dt));
            }
        }

        // Recalcular fuerzas
        fc.computeForces(p);

        // Integrar posiciones y velocidades
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];

            Vector newr = pi.r.mul(2.0).sub(pi.r_prev).add(pi.a.mul(dt * dt));
            Vector newv = newr.sub(pi.r_prev).mul(1.0 / (2.0 * dt));

            pi.r_prev.set(current[i]); // actualizar r_{n-1}
            pi.r.set(newr);
            pi.v.set(newv);
        }
    }

    @Override
    public String name() {
        return "Verlet";
    }
}

