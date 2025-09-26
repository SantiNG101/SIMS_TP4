public class Energy {
    public static double kinetic(Particle[] particles){
        double ek=0.0;
        for (Particle p: particles){
            ek += 0.5 * p.m * p.v.norm();
        }
        return ek;
    }


    public static double potentialOscillator(Particle p, double k){
        return 0.5 * k * p.r.norm();
    }


    public static double potentialGravity(Particle[] particles, double G, double h){
        double ep=0.0;
        int n = particles.length;
        for (int i=0;i<n;i++){
            for (int j=i+1;j<n;j++){
                double dist = Math.sqrt(particles[i].r.sub(particles[j].r).norm() + h*h);
                ep += -G * particles[i].m * particles[j].m / dist;
            }
        }
        return ep;
    }
}
