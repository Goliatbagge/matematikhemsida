import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as path_effects

# Skapa figur med hög upplösning
fig = plt.figure(figsize=(16, 5), dpi=150)
ax = plt.gca()

# Bakgrund med gradient-effekt
gradient = np.linspace(0, 1, 256).reshape(1, -1)
gradient = np.vstack((gradient, gradient))

# Skapa blå till ljusblå gradient
ax.imshow(gradient, aspect='auto', extent=[0, 16, 0, 5],
          cmap=plt.get_cmap('Blues'), alpha=0.8)

# Lägg till en andra gradient för djup
gradient2 = np.linspace(1, 0, 256).reshape(-1, 1)
ax.imshow(gradient2, aspect='auto', extent=[0, 16, 0, 5],
          cmap=plt.get_cmap('Oranges'), alpha=0.2)

# Rita några eleganta matematiska kurvor
x = np.linspace(0, 16, 1000)

# Sinus-våg (subtil)
y1 = 2.5 + 0.8 * np.sin(x * 0.8)
ax.plot(x, y1, color='white', linewidth=3, alpha=0.3)

# Cosinus-våg (subtil)
y2 = 2.5 + 0.6 * np.cos(x * 0.6 + np.pi/4)
ax.plot(x, y2, color='#f39c12', linewidth=2.5, alpha=0.4)

# Geometriska former (cirklar)
circles = [
    (2, 4, 0.4, 'white', 0.2),
    (5, 1.2, 0.3, '#f39c12', 0.3),
    (9, 4.2, 0.5, 'white', 0.15),
    (13, 1.5, 0.35, '#f39c12', 0.25),
    (14.5, 3.8, 0.25, 'white', 0.2),
]

for cx, cy, r, color, alpha in circles:
    circle = plt.Circle((cx, cy), r, color=color, alpha=alpha)
    ax.add_patch(circle)

# Geometriska former (trianglar)
triangles = [
    ([1, 1.5, 0.5], [0.8, 0.8, 1.5], 'white', 0.15),
    ([7, 7.6, 6.4], [0.5, 0.5, 1.2], '#f39c12', 0.2),
    ([12, 12.5, 11.5], [4.2, 4.2, 4.8], 'white', 0.18),
]

for xs, ys, color, alpha in triangles:
    triangle = plt.Polygon(list(zip(xs, ys)), color=color, alpha=alpha)
    ax.add_patch(triangle)

# Huvudtext: "Enkel matematik"
text = ax.text(8, 2.5, 'Enkel matematik',
               fontsize=72, fontweight='bold',
               ha='center', va='center',
               color='white',
               family='sans-serif')

# Lägg till texteffekter (skugga)
text.set_path_effects([
    path_effects.Stroke(linewidth=8, foreground='#2c3e50', alpha=0.5),
    path_effects.Normal()
])

# Undertext
subtext = ax.text(8, 1.6, 'Lär dig matematik och fysik - enkelt och tydligt',
                  fontsize=20, ha='center', va='center',
                  color='white', alpha=0.9,
                  family='sans-serif',
                  style='italic')

subtext.set_path_effects([
    path_effects.Stroke(linewidth=3, foreground='#2c3e50', alpha=0.3),
    path_effects.Normal()
])

# Ta bort axlar och marginaler
ax.set_xlim(0, 16)
ax.set_ylim(0, 5)
ax.axis('off')

# Spara bilden
plt.tight_layout(pad=0)
plt.savefig('hero-image.jpg', dpi=150, bbox_inches='tight',
            pad_inches=0, facecolor='#4a90e2')

print('Hero-bild skapad: hero-image.jpg')
print('Storlek: 2400x750 pixlar (16:5 ratio)')
print('Lämplig för hero-section på webbplatsen!')

plt.close()
