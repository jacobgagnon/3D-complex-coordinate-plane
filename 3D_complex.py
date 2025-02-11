import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def complex_function(z):
    #return np.sin(z)  # Example function, modify as needed

    #return z**3 - 1

    # Define a complex constant c
    c = 0.5 + 0.5j  # Example value
    # Compute the function
    return (z + c) * (z - c) * np.exp(-np.abs(z)**2)

def plot_complex_function(real_range=(-2, 2), imag_range=(-2, 2), resolution=100):
    real_vals = np.linspace(real_range[0], real_range[1], resolution)
    imag_vals = np.linspace(imag_range[0], imag_range[1], resolution)
    X, Y = np.meshgrid(real_vals, imag_vals)
    Z = X + 1j * Y  # Create complex grid
    W = complex_function(Z)  # Compute function values
    
    fig = plt.figure(figsize=(12, 6))
    
    # Plot magnitude
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, np.abs(W), cmap='viridis')
    ax1.set_title("Magnitude")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.set_zlabel("|f(z)|")
    
    # Plot phase
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(X, Y, np.angle(W), cmap='twilight')
    ax2.set_title("Phase")
    ax2.set_xlabel("Re(z)")
    ax2.set_ylabel("Im(z)")
    ax2.set_zlabel("Arg(f(z))")
    
    plt.show()

# Example usage
plot_complex_function()