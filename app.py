import cv2
import webbrowser
from pyzbar.pyzbar import decode
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cap.isOpened():
    raise Exception("Could not access the camera.")

processed_codes = set()  # Store processed QR codes to avoid duplicates

@app.route('/')
def index():
    """Render the main page."""
    return render_template_string("""
    <html>
    <head>
        <title>QR Code Scanner</title>
    </head>
    <body>
        <h1>QR Code Scanner</h1>
        <p>Point your webcam at a QR code.</p>
        <p>Detected URLs will open automatically in your browser.</p>
        <img src="/video_feed" width="640" height="480" />
    </body>
    </html>
    """)

def handle_qr_data(data):
    """Perform actions based on the QR code data."""
    print(f"Processing QR code data: {data}")
    
    # Example: Open a URL if the data is a web address
    if data.startswith("http://") or data.startswith("https://"):
        print("Opening URL in the browser...")
        webbrowser.open(data)
    else:
        print(f"No specific action defined for: {data}")

def generate_frames():
    """Generate video frames for the web interface."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        qr_codes = decode(frame)
        new_codes = []  # Store newly detected QR codes for this frame

        for qr in qr_codes:
            qr_data = qr.data.decode('utf-8')
            print(f"QR code detected: {qr_data}")  # Debugging output

            # Avoid processing the same QR code multiple times
            if qr_data not in processed_codes:
                new_codes.append(qr_data)
                processed_codes.add(qr_data)  # Mark QR code as processed

                # Handle the QR code data
                handle_qr_data(qr_data)

                # Draw bounding box and show the QR data
                x, y, w, h = qr.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = f"{qr.type}: {qr_data}"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Process multiple QR codes at once
        print(f"New QR codes detected: {new_codes}")

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video feed route."""
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
