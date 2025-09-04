import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# -----------------------------
# PARAMETERS
# -----------------------------
num_steps =200
dt = 0.1
D_small = 1.0
D_big = 0.5
num_small = 200
trail_length = 20
radius_small = 0.3
radius_big = 0.8
m_small = 0.3
m_big = 1.0
L = 20  # dominio di simulazione

# -----------------------------
# INITIALIZE PARTICLES
# -----------------------------
# Piccole particelle: posizioni iniziali casuali
x_small = np.zeros((num_small, num_steps))
y_small = np.zeros((num_small, num_steps))
x_small[:, 0] = np.random.uniform(0, L, num_small)
y_small[:, 0] = np.random.uniform(0, L, num_small)

# Grande particella: al centro
x_big = np.zeros(num_steps)
y_big = np.zeros(num_steps)
x_big[0] = L/2
y_big[0] = L/2

# Velocità costanti
dx_small = np.random.uniform(-.3, .3, num_small) * np.sqrt(2*D_small*dt)
dy_small = np.random.uniform(-.3, .3, num_small) * np.sqrt(2*D_small*dt)
dx_big = np.random.uniform(-.1, .1) * np.sqrt(2*D_big*dt)
dy_big = np.random.uniform(-.1, .1) * np.sqrt(2*D_big*dt)

# -----------------------------
# SIMULATION LOOP WITH BOUNCING WALLS
# -----------------------------
for t in range(1, num_steps):
    # Small particles move in straight lines
    x_small[:, t] = x_small[:, t-1] + dx_small
    y_small[:, t] = y_small[:, t-1] + dy_small

    # Bounce off walls for small particles
    out_x_low = x_small[:, t] < 0
    out_x_high = x_small[:, t] > L
    dx_small[out_x_low | out_x_high] *= -1
    x_small[:, t][out_x_low] = 0
    x_small[:, t][out_x_high] = L

    out_y_low = y_small[:, t] < 0
    out_y_high = y_small[:, t] > L
    dy_small[out_y_low | out_y_high] *= -1
    y_small[:, t][out_y_low] = 0
    y_small[:, t][out_y_high] = L

    # Big particle
    x_new = x_big[t-1] + dx_big
    y_new = y_big[t-1] + dy_big

    # Bounce off walls for big particle
    if x_new < 0 or x_new > L:
        dx_big *= -1
        x_new = np.clip(x_new, 0, L)
    if y_new < 0 or y_new > L:
        dy_big *= -1
        y_new = np.clip(y_new, 0, L)

    # Collisions big-small
    for i in range(num_small):
        dist = np.sqrt((x_new - x_small[i, t])**2 + (y_new - y_small[i, t])**2)
        if dist < (radius_big + radius_small):
            dx_collision = (m_small/m_big) * dx_small[i]
            dy_collision = (m_small/m_big) * dy_small[i]
            x_new += dx_collision
            y_new += dy_collision

    x_big[t] = x_new
    y_big[t] = y_new

    # Small-small collisions (same as before)
    for i in range(num_small):
        for j in range(i+1, num_small):
            dist = np.sqrt((x_small[i, t] - x_small[j, t])**2 + (y_small[i, t] - y_small[j, t])**2)
            if dist < (2 * radius_small):
                dx_collision_ss = (dx_small[i] - dx_small[j]) * 0.5
                dy_collision_ss = (dy_small[i] - dy_small[j]) * 0.5
                x_small[i, t] += dx_collision_ss
                y_small[i, t] += dy_collision_ss
                x_small[j, t] -= dx_collision_ss
                y_small[j, t] -= dy_collision_ss
# -----------------------------
# CALCOLA MSD
# -----------------------------
msd_small = np.mean((x_small - x_small[:, [0]])**2 + (y_small - y_small[:, [0]])**2, axis=0)
msd_big = (x_big - x_big[0])**2 + (y_big - y_big[0])**2


# -----------------------------
# FIGURE SETUP
# -----------------------------
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,6))
frames = []

# -----------------------------
# GENERA FRAMES
# -----------------------------
for frame in range(num_steps):
    ax1.clear()
    ax2.clear()

    # Tracce particelle
    ax1.set_xlim(-1, L+1)
    ax1.set_ylim(-1, L+1)
    ax1.set_title("2D Brownian Motion with Elastic Scattering")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")

    start = max(0, frame-trail_length)
    for i in range(num_small):
        ax1.plot(x_small[i,start:frame+1], y_small[i,start:frame+1], 'b-', alpha=0.3)
    ax1.plot(x_small[:,frame], y_small[:,frame], 'bo', ms=4)

    start_big = max(0, frame-trail_length)
    ax1.plot(x_big[start_big:frame+1], y_big[start_big:frame+1], 'r-', alpha=0.6)
    ax1.plot(x_big[frame], y_big[frame], 'ro', ms=10)

    # MSD plot
    ax2.set_xlim(0, num_steps*dt)
    ax2.set_ylim(0, max(msd_small.max(), msd_big.max())*1.1)
    ax2.plot(np.arange(frame+1)*dt, msd_small[:frame+1], 'b', label="Avg Small MSD")
    ax2.plot(np.arange(frame+1)*dt, msd_big[:frame+1], 'r', label="Big MSD")
    ax2.legend()
    ax2.set_xlabel("Time")
    ax2.set_ylabel("MSD")
    ax2.set_title("Mean Squared Displacement")

    # Converti in immagine
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    img = Image.fromarray(buf[:, :, :3])
    frames.append(img)

# -----------------------------
# SALVA GIF
# -----------------------------
frames[0].save("brownian_particles.gif", save_all=True, append_images=frames[1:], duration=50, loop=0)

# Visualizza GIF
from IPython.display import Image as IPImage
IPImage("brownian_particles.gif")
