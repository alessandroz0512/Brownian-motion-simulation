# 2D Brownian Motion Simulation with Elastic Collisions

This project simulates **2D Brownian motion** of multiple small particles and a single large particle in a confined square domain. It incorporates **elastic collisions between particles**, **wall bounces**, **MSD calculation**, and **chi-squared analysis** to compare simulation results with an analytical model.

---

## Methodology

1. **Initialization**
   - Small particles are randomly placed within a square domain of size `L x L`.
   - The large particle starts at the center of the domain.
   - Velocities are randomly assigned to all particles, scaled by their diffusion coefficients (`D_small` and `D_big`), to emulate stochastic motion.

2. **Simulation Loop**
   - Particle positions are updated at each time step according to their velocities.
   - **Wall collisions** are handled using velocity reversal and position clipping, ensuring particles remain inside the domain.
   - **Elastic collisions** are implemented:
     - Between small particles (small-small collisions).
     - Between small particles and the large particle (small-large collisions).
   - The loop runs for `num_steps` time steps, generating trajectories for all particles.

3. **Mean Squared Displacement (MSD)**
   - The MSD is computed for all small particles as the average squared displacement from their initial positions:
     \[
     \text{MSD}_{small}(t) = \langle (x - x_0)^2 + (y - y_0)^2 \rangle
     \]
   - The MSD for the large particle is calculated individually.

4. **Analytical MSD Model**
   - The MSD of the large particle is fitted to an analytical model:
     \[
     \text{MSD}_{model}(t) = 3 a t^2
     \]
   - The fitting parameter `a` is extracted using `scipy.optimize.curve_fit`.

5. **Chi-Squared Analysis**
   - Chi-squared (\(\chi^2\)) is computed to quantify the goodness of fit between the simulated MSD and the analytical model:
     \[
     \chi^2 = \sum_i \frac{(\text{MSD}_{sim}(t_i) - \text{MSD}_{model}(t_i))^2}{\sigma^2}
     \]
   - The reduced chi-squared is obtained by dividing by the degrees of freedom (`N-1`).

6. **Visualization**
   - Particle trajectories are plotted with trails to visualize motion over time.
   - MSD curves for both simulated and analytical models are plotted for comparison.
   - Absolute errors between the simulation and model MSD are plotted.
   - An animated GIF (`brownian_particles.gif`) shows particle motion and MSD evolution simultaneously.

---

## Analysis

- **Small particles** exhibit rapid, random motion due to a higher diffusion coefficient. Their MSD increases roughly linearly with time, consistent with classical Brownian motion theory.
- **Large particle** moves more slowly and is influenced by collisions with small particles, showing intermittent jumps in its trajectory.
- **Elastic collisions** redistribute momentum between particles, affecting the large particle’s movement and causing deviations from simple diffusion.
- **Chi-squared** provides a quantitative measure of how closely the analytical MSD model matches the simulated large particle MSD.

---

## Results

1. The simulation produces realistic Brownian motion trajectories for both small and large particles.
2. The MSD of small particles shows near-linear growth with time, confirming diffusive behavior.
3. The large particle’s MSD can be accurately described by the analytical model \(\text{MSD} = 3 a t^2\), with a fitted parameter `a`.
4. Chi-squared analysis indicates good agreement between simulation and model, validating the methodology.
5. The animated GIF visually demonstrates particle motion, collisions, and the effect of trails, making it easier to understand the dynamics of the system.

---

## Usage

- Run the Python script to simulate particle motion.
- The script outputs:
  - Animated GIF showing particle trajectories and MSD evolution.
  - Console output with fitted parameter `a` and chi-squared values.
  - Plots of MSD and absolute error for visual analysis.

---

## References

1. Einstein, A. (1905). *On the Movement of Small Particles Suspended in a Stationary Liquid*. Annalen der Physik.  
2. Nelson, D. (2004). *Biological Physics: Energy, Information, Life*. W.H. Freeman.  
3. MATLAB Central: Examples of 2D Brownian motion simulations with collisions.
