public class BeemanIntegrator implements Integrator {
    @Override
    public void step(Particle[] p, double dt, ForceCalculator fc) {
        int n = p.length;

        // --- Predicción de posiciones ---
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            Vector rnew = pi.r
                    .add(pi.v.mul(dt))
                    .add(pi.a.mul((2.0 / 3.0) * dt * dt))
                    .sub(pi.a_prev.mul((1.0 / 6.0) * dt * dt));
            pi.r.set(rnew);
        }

        // --- Calcular aceleraciones en t+dt ---
        fc.computeForces(p);

        // --- Corrección de velocidades ---
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            Vector a_next = pi.a; // ya calculada con posiciones nuevas
            Vector vnew = pi.v
                    .add(a_next.mul(dt / 3.0))
                    .add(pi.a.mul(5.0 * dt / 6.0))
                    .sub(pi.a_prev.mul(dt / 6.0));

            // actualizar v y almacenar a_prev para próximo paso
            pi.v.set(vnew);
            pi.a_prev.set(pi.a);
        }
    }

    @Override
    public String name() {
        return "Beeman";
    }
}

