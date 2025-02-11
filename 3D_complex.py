import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Predefined functions
def function_1(z):
    return np.sin(z)

def function_2(z):
    return z**3 - 1

def function_3(z, c=0.5 + 0.5j):
    return (z + c) * (z - c) * np.exp(-np.abs(z)**2)

# Plotting function
def plot_complex_function(func, c_value=0.5 + 0.5j, real_range=(-2, 2), imag_range=(-2, 2), resolution=100):
    real_vals = np.linspace(real_range[0], real_range[1], resolution)
    imag_vals = np.linspace(imag_range[0], imag_range[1], resolution)
    X, Y = np.meshgrid(real_vals, imag_vals)
    Z = X + 1j * Y  # Create complex grid

    if func == "sin(z)":
        W = function_1(Z)
    elif func == "z^3 - 1":
        W = function_2(Z)
    elif func == "(z + c) * (z - c) * np.exp(-np.abs(z)**2)":
        W = function_3(Z, c=c_value)
    else:
        try:
            # If a custom function is entered, evaluate it with c_value as part of the string
            custom_func_eval = func.replace("z", "Z").replace("c", str(c_value))
            W = eval(custom_func_eval)
        except Exception as e:
            print(f"Error in custom function: {e}")
            return

    fig = plt.figure(figsize=(12, 6))
    
    # Plot magnitude
    ax1 = fig.add_subplot(121, projection='3d')
    surf1 = ax1.plot_surface(X, Y, np.abs(W), cmap='viridis')
    ax1.set_title("Magnitude")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.set_zlabel("|f(z)|")
    fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10)

    # Plot phase
    ax2 = fig.add_subplot(122, projection='3d')
    surf2 = ax2.plot_surface(X, Y, np.angle(W), cmap='twilight')
    ax2.set_title("Phase")
    ax2.set_xlabel("Re(z)")
    ax2.set_ylabel("Im(z)")
    ax2.set_zlabel("Arg(f(z))")
    fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10)

    plt.show()

# Tkinter GUI setup
def on_combobox_change(event):
    selected_func = combobox.get()
    
    # Show or hide the custom function input field based on combobox selection
    if selected_func == "Custom Function":
        func_input_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        func_input.grid(row=2, column=1, padx=10, pady=10)
    else:
        func_input_label.grid_forget()
        func_input.grid_forget()

def on_plot_button_click():
    selected_func = combobox.get()
    custom_func = func_input.get()  # Get custom function input from text box
    c_value = complex(c_input.get())  # Get value of c from input field and convert to complex

    if selected_func == "Custom Function":
        if custom_func:
            # Inject c_value into the custom function expression, replace lowercase z
            custom_func_with_c = custom_func.replace("c", str(c_value))
            plot_complex_function(custom_func_with_c, c_value)
        else:
            print("Please enter a valid custom function.")
    else:
        plot_complex_function(selected_func, c_value)

# Create main window
root = tk.Tk()
root.title("Complex Function Plotter")

# Combobox for selecting the function
combobox_label = tk.Label(root, text="Select Function:")
combobox_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Human-readable options in the combobox
combobox = ttk.Combobox(root, values=["sin(z)", "z^3 - 1", "(z + c) * (z - c) * np.exp(-np.abs(z)**2)", "Custom Function"])
combobox.set("(z + c) * (z - c) * np.exp(-np.abs(z)**2)")  # Default selection
combobox.grid(row=0, column=1, padx=10, pady=10)

# Bind combobox change event
combobox.bind("<<ComboboxSelected>>", on_combobox_change)

# Input field for custom function (hidden initially)
func_input_label = tk.Label(root, text="Enter Custom Function (e.g., z**2 + 1, z + c):")
func_input = tk.Entry(root)

# Input field for 'c' value
c_input_label = tk.Label(root, text="Enter Complex Value for c (e.g., 0.5+0.5j):")
c_input_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

c_input = tk.Entry(root)
c_input.insert(0, "0.5+0.5j")  # Default value
c_input.grid(row=3, column=1, padx=10, pady=10)

# Button to plot the function
plot_button = tk.Button(root, text="Plot", command=on_plot_button_click)
plot_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

# Run the application
root.mainloop()
