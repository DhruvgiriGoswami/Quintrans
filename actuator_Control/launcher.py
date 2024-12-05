import os
import threading
import time
import webbrowser
import tkinter as tk
from threading import Thread
from flask import Flask, render_template
from werkzeug.serving import make_server

# Import your existing Flask app
from app import app

# Function to start Flask server
def start_flask_server():
    # Start Flask in a separate thread and handle server shutdown gracefully
    httpd = make_server('127.0.0.1', 5000, app)
    print("Flask server running at http://127.0.0.1:5000")
    httpd.serve_forever()

# Function to display the loading screen
def show_loading_screen():
    # Create the tkinter root window
    root = tk.Tk()
    root.title("Loading")
    
    # Set window size and print for debugging
    print("Window size:", "1400x700")  # Print to check if the dimensions are being set correctly
    root.geometry("1400x700")  # Set window size to 1600x600 (or any other preferred size)
    root.configure(bg="#ffffff")
    
    # Force Tkinter to update the window
    root.update()  # Refresh the window to apply the geometry
    
    # Check if window size is applied correctly
    print(f"Window size after update: {root.winfo_width()}x{root.winfo_height()}")

    # Add a logo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "static", "quintrans_Logo_Big.png")
    
    try:
        logo = tk.PhotoImage(file=logo_path)  # Load logo
        logo_label = tk.Label(root, image=logo, bg="#ffffff")
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Add a loading text
    loading = tk.Label(root, text="Starting the server...", bg="#ffffff", font=("Arial", 14))
    loading.pack()

    # Close the loading screen after 5 seconds
    def close_screen():
        time.sleep(5)
        root.destroy()

    Thread(target=close_screen).start()

    # When the window is closed, terminate the Flask server
    def on_close():
        print("Window closed. Shutting down Flask server.")
        os._exit(0)  # Terminate the process when the window is closed

    root.protocol("WM_DELETE_WINDOW", on_close)  # Register on_close when the window is closed
    root.mainloop()

# Main function to run the program
if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()

    # Show the loading screen
    show_loading_screen()

    # Open the actuator control site in the browser
    webbrowser.open("http://127.0.0.1:5000")
