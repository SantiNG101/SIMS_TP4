public class BeemanIntegrator implements Integrator {

    private boolean firstStep = true;

    @Override
    public void step(Particle[] p, double dt, ForceCalculator fc) {
        int n = p.length;

        // **LA CORRECCIÓN CLAVE**: En el primer paso, nos aseguramos de que a(0) esté
        // calculada a partir de r(0) y v(0) antes de hacer nada más.
        if (firstStep) {
            fc.computeForces(p);
        }

        // 1. Guardar estado actual: aceleraciones a(t) y velocidades v(t)
        Vector[] a_n = new Vector[n];
        Vector[] v_n = new Vector[n];
        for (int i = 0; i < n; i++) {
            a_n[i] = new Vector(p[i].a.x, p[i].a.y, p[i].a.z);
            v_n[i] = new Vector(p[i].v.x, p[i].v.y, p[i].v.z);
        }

        // 2. Inicialización de alta precisión en el primer paso
        if (firstStep) {
            for (int i = 0; i < n; i++) {
                Particle pi = p[i];

                Vector r_curr = new Vector(pi.r.x, pi.r.y, pi.r.z);
                Vector v_curr = new Vector(pi.v.x, pi.v.y, pi.v.z);
                Vector a_curr = a_n[i];

                Vector r_prev_est = r_curr.sub(v_curr.mul(dt)).add(a_curr.mul(0.5 * dt * dt));
                Vector v_prev_est = v_curr.sub(a_curr.mul(dt));

                pi.r.set(r_prev_est);
                pi.v.set(v_prev_est);

                fc.computeForces(p);

                pi.a_prev.set(pi.a);

                pi.r.set(r_curr);
                pi.v.set(v_curr);
                pi.a.set(a_curr);
            }
            firstStep = false;
        }

        // --- PREDICCIÓN ---
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];

            Vector r_pred = pi.r
                    .add(v_n[i].mul(dt))
                    .add(a_n[i].mul((2.0 / 3.0) * dt * dt))
                    .sub(pi.a_prev.mul((1.0 / 6.0) * dt * dt));

            Vector v_pred = v_n[i]
                    .add(a_n[i].mul(1.5 * dt))
                    .sub(pi.a_prev.mul(0.5 * dt));

            pi.r.set(r_pred);
            pi.v.set(v_pred);
        }

        // --- EVALUACIÓN DE FUERZAS ---
        fc.computeForces(p);

        // --- CORRECCIÓN ---
        for (int i = 0; i < n; i++) {
            Particle pi = p[i];
            Vector a_next = pi.a;

            Vector v_corrected = v_n[i]
                    .add(a_next.mul((1.0 / 3.0) * dt))
                    .add(a_n[i].mul((5.0 / 6.0) * dt))
                    .sub(pi.a_prev.mul((1.0 / 6.0) * dt));

            pi.v.set(v_corrected);
        }

        // --- ACTUALIZACIÓN ---
        for (int i = 0; i < n; i++) {
            p[i].a_prev.set(a_n[i]);
        }
    }

    @Override
    public String name() {
        return "Beeman";
    }
}




