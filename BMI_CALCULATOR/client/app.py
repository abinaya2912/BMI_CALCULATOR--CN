from flask import Flask, request, jsonify,render_template
import socket

app = Flask(__name__)

# TCP client function
def send_bmi_tcp(server_addr, weight, height):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print("tcp")
        client_socket.connect(server_addr)
        message = f"{weight} {height}"
        print(f"TCP message sent: {message}")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        return data.decode()

# UDP client function
def send_bmi_udp(server_addr, weight, height):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("udp")
    message = f"{weight} {height}"
    print(f"UDP message sent: {message}")
    client_socket.sendto(message.encode(), server_addr)
    data, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return data.decode()

# Default route
@app.route('/')
def index():
    return render_template('index.html')

# Route for BMI calculation
@app.route('/calculate', methods=['POST'])
def calculate_bmi():
    print("Received BMI calculation request")

    # Expecting JSON data
    if not request.is_json:
        return jsonify({"error": "Expected JSON data"}), 400

    data = request.get_json()

    # Check if required fields are in the JSON
    if 'weight' not in data or 'height' not in data or 'protocol' not in data:
        return jsonify({"error": "Missing 'weight', 'height', or 'protocol' parameter"}), 400

    weight = data['weight']
    height = data['height']
    protocol = data['protocol']

    server_ip = '192.168.153.44'  # Replace with your server's IP address
    server_port = 12345           # Replace with your server's port number
    server_addr = (server_ip, server_port)

    # Send data based on the selected protocol
    if protocol.lower() == 'tcp':
        response = send_bmi_tcp(server_addr, weight, height)
    else:  # Assuming UDP as the default protocol
        response = send_bmi_udp(server_addr, weight, height)

    bmi_value, category = response.split(", ")
    bmi = bmi_value.split(": ")[1]
    category = category.split(": ")[1]

    # Return the parsed response as JSON
    return jsonify({"bmi": bmi, "category": category})

if __name__ == '__main__':
    app.run(debug=True)
