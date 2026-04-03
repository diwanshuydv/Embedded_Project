import cv2
import serial
import struct
import time
import numpy as np

# ===== CONFIG =====
URL = "http://172.31.75.172:8080/video"
SERIAL_PORT = "/dev/ttyACM0"   
BAUD = 115200                 

IMG_SIZE = 64

# Use a small timeout so the serial read doesn't block the video stream
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.01)
cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Error: Cannot open video stream")
    exit()

print("Streaming started... Waiting for echo.")

last_send_time = time.time()
rx_buffer = bytearray()  # Buffer to store incoming fragmented serial data

while True:
    # 1. Keep reading the camera to keep the stream buffer empty/fresh
    ret, frame = cap.read()
    if not ret:
        break

    # 2. Read any incoming echoed data from the STM32
    if ser.in_waiting > 0:
        rx_buffer.extend(ser.read(ser.in_waiting))

    # 3. Check if we have a full packet in our buffer
    header_idx = rx_buffer.find(b'\xAA\x55')
    if header_idx != -1:
        # We found a header! Throw away any corrupted bytes before it
        if header_idx > 0:
            rx_buffer = rx_buffer[header_idx:]

        # Check if we have at least enough bytes to read the size field (Header=2, Size=2)
        if len(rx_buffer) >= 4:
            # Unpack the 2-byte size field (Little Endian)
            expected_data_size = struct.unpack('<H', rx_buffer[2:4])[0]
            expected_packet_size = 4 + expected_data_size

            # Check if the FULL image packet has arrived
            if len(rx_buffer) >= expected_packet_size:
                # Extract just the image pixel data
                img_data = rx_buffer[4:expected_packet_size]

                # Remove this processed packet from the buffer
                rx_buffer = rx_buffer[expected_packet_size:]

                # Reconstruct the image from the raw bytes
                try:
                    # Convert raw bytes to an unsigned 8-bit integer array
                    echoed_array = np.frombuffer(img_data, dtype=np.uint8)
                    
                    # Reshape it back into the 2D image matrix
                    echoed_img = echoed_array.reshape((IMG_SIZE, IMG_SIZE))

                    # Scale it up slightly so it's easier to see on your monitor
                    display_img = cv2.resize(echoed_img, (256, 256), interpolation=cv2.INTER_NEAREST)
                    
                    # Display the echoed image
                    cv2.imshow("Echoed Image from STM32", display_img)
                    print("✅ Successfully reconstructed echoed frame!")
                except Exception as e:
                    print(f"Error reconstructing image: {e}")

    # 4. ===== SEND EVERY 5 SECONDS =====
    if time.time() - last_send_time >= 5:
        last_send_time = time.time()

        # Preprocess
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (IMG_SIZE, IMG_SIZE))

        data = small.flatten().tobytes()

        header = b'\xAA\x55'
        size = struct.pack('<H', len(data))
        packet = header + size + data

        ser.write(packet)
        print(f"Sent frame of size {len(data)} bytes to STM32...")

    # Wait 1ms for GUI events (required for cv2.imshow to update)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()