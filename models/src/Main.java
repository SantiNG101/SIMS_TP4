import java.io.File;
import java.io.IOException;
import java.util.Random;

public class Main {

    // Parameters
    static String mode = "gravity"; // "oscillator" or "gravity"
    static String integratorName = "verlet"; // "verlet", "beeman", "gear5"
    static double dt = 1e-2;
    static double tf = 50.0;

    public static void main(String[] args) throws IOException {
        if (mode.equalsIgnoreCase("oscillator")) {
            runOscillator(integratorName, dt, tf);
        } else if (mode.equalsIgnoreCase("gravity")) {
            runGravity(integratorName, dt, tf);
        } else {
            throw new IllegalArgumentException("Unknown mode: " + mode);
        }
    }

    static Integrator buildIntegrator(String integratorName) {
        if (integratorName.equalsIgnoreCase("verlet")) {
            return new VerletIntegrator();
        } else if (integratorName.equalsIgnoreCase("beeman")) {
            return new BeemanIntegrator();
        } else if (integratorName.equalsIgnoreCase("gear5")) {
            return new Gear5Integrator();
        } else {
            throw new IllegalArgumentException("Unknown integrator: " + integratorName);
        }
    }

    static void runOscillator(String integratorName, double dt, double tf) throws IOException {
        String folder = "outputs/oscillator/sim_results/";
        new File(folder).mkdirs(); 
        String out = folder + integratorName + "_out.csv";
        String eout = folder + integratorName + "_energy.csv";

        Particle p = new Particle(0);
        p.m = 70.0;
        p.r.set(1.0, 0, 0);

        double k = 1e4;
        double gamma = 100.0;
        double A = 1.0;
        p.v.set(-A * gamma / (2.0 * p.m), 0, 0);

        Particle[] arr = new Particle[]{p};
        ForceCalculator fc = new OscillatorForce(k, gamma, p);
        Integrator integrator = buildIntegrator(integratorName);

        StateWriter sw = new StateWriter(out);
        EnergyWriter ew = new EnergyWriter(eout, "E_kin,E_pot,E_tot");

        double t = 0.0;
        while (t <= tf + 1e-12) {
            sw.write(t, arr);
            double ek = Energy.kinetic(arr);
            double ep = Energy.potentialOscillator(p, k);
            ew.write(t, ek, ep, ek + ep);

            integrator.step(arr, dt, fc);
            t += dt;
        }

        sw.close();
        ew.close();
        System.out.println("Finished oscillator with " + integrator.name() + " -> " + out + ", " + eout);
    }

    static void runGravity(String integratorName, double dt, double tf) throws IOException {
        int N = 200;

        String folder = "outputs/gravity/sim_results/";
        new File(folder).mkdirs(); 
        String out = folder + "out.csv";
        String eout = folder + "energy_dt"+ String.format("%.0e",dt) +".csv";

        Particle[] arr = new Particle[N];
        Random rnd = new Random(1);
        for (int i = 0; i < N; i++) {
            arr[i] = new Particle(i);
            arr[i].m = 1.0;
            arr[i].r.set(rnd.nextGaussian(), rnd.nextGaussian(), rnd.nextGaussian());
            double theta = 2 * Math.PI * rnd.nextDouble();
            double phi = Math.acos(2 * rnd.nextDouble() - 1);
            arr[i].v.set(
                    0.1 * Math.cos(theta) * Math.sin(phi),
                    0.1 * Math.sin(theta) * Math.sin(phi),
                    0.1 * Math.cos(phi)
            );
        }

        final double G = 1.0, h = 0.05;
        ForceCalculator fc = new GravityForce(G, h);
        Integrator integrator = buildIntegrator(integratorName);

        StateWriter sw = new StateWriter(out);
        EnergyWriter ew = new EnergyWriter(eout, "E_kin,E_pot,E_tot");

        double t = 0.0;
        tf += 1e-12;
        while (t <= tf) {
            // sw.write(t, arr); // para graficar estado de las particulas
            double ek = Energy.kinetic(arr);
            double ep = Energy.potentialGravity(arr, G, h);
            ew.write(t, ek, ep, ek + ep);

            integrator.step(arr, dt, fc);
            t += dt;
        }

        sw.close();
        ew.close();
        System.out.println("Finished gravity with " + integrator.name() + " -> " + out + ", " + eout);
    }
}



