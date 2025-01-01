import os
import threading
import time
import webbrowser
import subprocess  # Import subprocess for dependency installation
import sys  # Import sys for exiting the program
import tkinter as tk

# Function to check and install dependencies
def install_dependencies():
    print("Checking and installing dependencies...")
    try:
        # Ensure pip is available
        subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])

        # Install packages from requirements.txt
        requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All dependencies installed.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

# Function to display the loading screen
def show_loading_screen():
    # Create the tkinter root window
    root = tk.Tk()
    root.title("Loading")

    # Set window size
    root.geometry("1400x700")  
    root.configure(bg="#ffffff")

    # Force Tkinter to update the window
    root.update()  # Refresh the window to apply the geometry

    # Add a logo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "static", "quintrans_Logo_Big.png")

    try:
        logo = tk.PhotoImage(file=logo_path)  # Load logo
        logo_label = tk.Label(root, image=logo, bg="#ffffff")
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Add a message for resolving dependencies
    loading_label = tk.Label(root, text="Resolving dependencies...", bg="#ffffff", font=("Arial", 14))
    loading_label.pack()

    # Update the window to show the message
    root.update()

    # Install dependencies
    install_dependencies()

    # Update message after dependencies are installed
    loading_label.config(text="Starting the server...")

    # Run the Tkinter mainloop in a separate thread to allow GUI updates while running the server
    def start_flask_server():
        try:
            # Run app.py as the Flask server
            subprocess.Popen([sys.executable, "app.py"])
        except Exception as e:
            print(f"Error starting Flask server: {e}")
            sys.exit(1)

    # Start the Flask server in a separate thread
    threading.Thread(target=start_flask_server).start()

    # Show the window for 2 seconds before closing
    def close_screen():
        time.sleep(2)
        root.destroy()

    # Start the close_screen function in a separate thread
    threading.Thread(target=close_screen).start()

    # Open the actuator control site in the browser
    webbrowser.open("http://127.0.0.1:5000")

    # When the window is closed, terminate the program
    def on_close():
        print("Window closed. Shutting down.")
        os._exit(0)  # Terminate the process when the window is closed

    root.protocol("WM_DELETE_WINDOW", on_close)  # Register on_close when the window is closed
    root.mainloop()

# Main function to run the program
if __name__ == "__main__":
    # Show the loading screen first
    show_loading_screen()
