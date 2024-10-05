from flask import Flask, render_template, request
from gpiozero import LED

app = Flask(__name__)

# Define LED pins
leds = {
    '1': LED(6),
   # '2': LED(7),
   # '3': LED(9),
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle/<led_id>', methods=['POST'])
def toggle_led(led_id):
    if led_id in leds:
        leds[led_id].toggle()  # Toggle the LED state
    return '', 204  # No content response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
