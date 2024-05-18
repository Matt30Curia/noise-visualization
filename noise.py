import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from perlin_noise import PerlinNoise
import numpy as np
import random


def generateNoise(dimX, dimY, seed=0):
    randomSeed = seed if seed != 0 else random.randint(1, 100_000)
    noise = PerlinNoise(octaves=3, seed=randomSeed)
    
    # Dimensioni dell'immagine
    xpix, ypix = dimX, dimY
    pic = np.array([[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)])  # Matrice del rumore di Perlin
    
    return pic


def showNoise(noise, fig):
    ax = fig.add_subplot(1, 3, 3)
    ax.imshow(noise, cmap='gray')
    ax.set_ylabel('Perlin noise')


def showTerrain(noise, fig):
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    X, Y = np.meshgrid(np.arange(0, dim["x"], 1), np.arange(0, dim["y"], 1))
    ax.plot_surface(X, Y, noise, rstride=50, cstride=8, cmap="gist_earth")
    return ax


class WindowManager:
    def __init__(self, dimX, dimY, fig, showTerrain, showNoise, generateNoise, ax):
        self.dimX = dimX
        self.dimY = dimY
        self.fig = fig
        self.showTerrain = showTerrain
        self.showNoise = showNoise
        self.generateNoise = generateNoise
        self.ax = ax
        self.animation = None

    def generate(self, event):

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
    # Genera nuovo rumore
        noise = self.generateNoise(self.dimX, self.dimY)
    
    # Mostra il terreno
        self.ax = self.showTerrain(noise, self.fig)
    
    # Mostra il rumore
        self.showNoise(noise, self.fig)
    
    # Ruota il grafico
        self.rotate()

    def rotate(self):
        # Stop current animation 
        if self.animation is not None:
            self.animation.event_source.stop()
        
        def update_rotation(frame):
            self.ax.view_init(elev=30, azim=frame)
        
        self.animation = FuncAnimation(self.fig, update_rotation, frames=np.arange(0, 360, 2), interval=50)
        plt.show()


# Variable initialization
dim = {"x": 800, "y": 800}
noise = generateNoise(dim["x"], dim["y"]) * 25
fig = plt.figure(figsize=plt.figaspect(1.))
fig.suptitle('Perlin noise')

showNoise(noise, fig)

terrain_ax = showTerrain(noise, fig)

# WindowManager initialization
windowManager = WindowManager(dim["x"], dim["y"], fig, showTerrain, showNoise, generateNoise, terrain_ax)
button_ax = fig.add_axes([0.81, 0.05, 0.1, 0.075])
button = Button(button_ax, 'Regenerate')
button.on_clicked(windowManager.generate)

# Start loop
windowManager.rotate()
