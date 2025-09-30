


public class BeemanIntegrator implements Integrator {
    @Override
    public void step(Particle[] p, double dt, ForceCalculator fc) {
        int n = p.length;

        // --- Guardar aceleraciones actuales (a_n) para cada partícula ---
        Vector[] a_n = new Vector[n];
        for (int i = 0; i < n; i++) {
            a_n[i] = new Vector(p[i].a.x, p[i].a.y, p[i].a.z); // copia
        }

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
            Vector a_next = new Vector(pi.a.x, pi.a.y, pi.a.z);  // a_{n+1} (copia)
            Vector a_curr = a_n[i];                               // a_n (copia guardada)
            Vector a_prev = new Vector(pi.a_prev.x, pi.a_prev.y, pi.a_prev.z); // a_{n-1}

            // v_{n+1} = v_n + dt/6 (2 a_{n+1} + 5 a_n - a_{n-1})
            Vector vnew = pi.v
                    .add(a_next.mul((2.0 * dt) / 6.0))
                    .add(a_curr.mul((5.0 * dt) / 6.0))
                    .sub(a_prev.mul((1.0 * dt) / 6.0));

            // actualizar v y almacenar a_prev para próximo paso
            pi.v.set(vnew);
            pi.a_prev.set(a_curr);
        }
    }

    @Override
    public String name() {
        return "Beeman";
    }
}

