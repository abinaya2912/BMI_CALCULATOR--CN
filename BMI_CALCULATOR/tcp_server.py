import socket

# Function to calculate BMI
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    return bmi

# Function to categorize BMI
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Create a TCP server socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to a specific IP and port
tcp_server_socket.bind(('192.168.210.253', 12345))  # Change the IP to the appropriate one for your server

# Set the server to listen for incoming connections
tcp_server_socket.listen(5)
print("TCP Server is listening on port 12345")

# Infinite loop to keep the server running and accepting connections
while True:
    # Accept a new client connection
    client_socket, addr = tcp_server_socket.accept()
    print(f"Connection from {addr} has been established!")

    # Receive data from the client
    data = client_socket.recv(1024).decode()

    # Split the received data into weight and height
    try:
        weight, height_cm = map(float, data.split())

        # Calculate BMI and determine the category
        bmi = calculate_bmi(weight, height_cm)
        category = get_bmi_category(bmi)

        # Prepare the response string
        response = f"BMI: {bmi:.2f}, Category: {category}"

    except ValueError:
        # Handle invalid input
        response = "Error: Invalid input format. Please provide weight and height as numbers."

    # Send the response back to the client
    client_socket.send(response.encode())

    # Close the connection with the client
    client_socket.close()
