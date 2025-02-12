import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel

# Predefined functions
def function_1(z):
    return np.sin(z)

def function_2(z):
    return z**3 - 1

def function_3(z, c=0.5 + 0.5j):
    return (z + c) * (z - c) * np.exp(-np.abs(z)**2)

# Plotting function
def plot_complex_function(ax1, ax2, func, c_value=0.5 + 0.5j, real_range=(-2, 2), imag_range=(-2, 2), resolution=100, colorbars=None):
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

    # Remove previous color bars if they exist
    if colorbars:
        for cb in colorbars:
            cb.remove()

    # Plot magnitude
    ax1.clear()  # Clear previous plot
    surf1 = ax1.plot_surface(X, Y, np.abs(W), cmap='viridis')
    ax1.set_title("Magnitude")
    ax1.set_xlabel("Re(z)")
    ax1.set_ylabel("Im(z)")
    ax1.set_zlabel("|f(z)|")
    colorbar1 = ax1.figure.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)

    # Plot phase
    ax2.clear()  # Clear previous plot
    surf2 = ax2.plot_surface(X, Y, np.angle(W), cmap='twilight')
    ax2.set_title("Phase")
    ax2.set_xlabel("Re(z)")
    ax2.set_ylabel("Im(z)")
    ax2.set_zlabel("Arg(f(z))")
    colorbar2 = ax2.figure.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)

    # Return the new color bars
    return [colorbar1, colorbar2]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Complex Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Layout setup
        self.layout = QVBoxLayout(self)

        # Label for function selection
        self.choose_function_label = QLabel("Choose Function:", self)
        self.layout.addWidget(self.choose_function_label)

        # Combobox for function selection
        self.combobox = QComboBox(self)
        self.combobox.addItem("sin(z)")
        self.combobox.addItem("z^3 - 1")
        self.combobox.addItem("(z + c) * (z - c) * np.exp(-np.abs(z)**2)")
        self.combobox.addItem("Custom Function")
        self.layout.addWidget(self.combobox)

        # Input for custom function
        self.func_input_label = QLabel("Enter Custom Function (e.g., z**2 + 1, z + c):", self)
        self.layout.addWidget(self.func_input_label)
        self.func_input = QLineEdit(self)
        self.layout.addWidget(self.func_input)

        # Input for 'c' value
        self.c_input_label = QLabel("Enter Complex Value for c (e.g., 0.5+0.5j):", self)
        self.layout.addWidget(self.c_input_label)
        self.c_input = QLineEdit(self)
        self.c_input.setText("0.5+0.5j")  # Default value
        self.layout.addWidget(self.c_input)

        # Plot button
        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.on_plot_button_click)
        self.layout.addWidget(self.plot_button)

        # Matplotlib FigureCanvas
        self.figure = plt.Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Create subplots
        self.ax1 = self.figure.add_subplot(121, projection='3d')
        self.ax2 = self.figure.add_subplot(122, projection='3d')

        # To keep track of colorbars
        self.colorbars = []

        self.combobox.currentIndexChanged.connect(self.on_combobox_change)

    def on_combobox_change(self):
        selected_func = self.combobox.currentText()

        # Show or hide the custom function input based on combobox selection
        if selected_func == "Custom Function":
            self.func_input_label.show()
            self.func_input.show()
        else:
            self.func_input_label.hide()
            self.func_input.hide()

    def on_plot_button_click(self):
        selected_func = self.combobox.currentText()
        custom_func = self.func_input.text()  # Get custom function input from text box
        c_value = complex(self.c_input.text())  # Get value of c from input field and convert to complex

        # Plot the selected function
        if selected_func == "Custom Function":
            if custom_func:
                custom_func_with_c = custom_func.replace("c", str(c_value))
                self.colorbars = plot_complex_function(self.ax1, self.ax2, custom_func_with_c, c_value, colorbars=self.colorbars)
        else:
            self.colorbars = plot_complex_function(self.ax1, self.ax2, selected_func, c_value, colorbars=self.colorbars)

        self.canvas.draw()

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
