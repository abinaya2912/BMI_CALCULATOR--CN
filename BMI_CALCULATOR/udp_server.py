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

# Create a UDP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '192.168.210.253'  # Server's IP
port = 12345  # Port number
server_socket.bind((host, port))
print(f"UDP Server is listening on port {port}")

while True:
    try:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(1024)  # Buffer size 1024 bytes
        print(f"Received data from {client_address}: {data.decode()}")

        # Split the received data into weight and height
        try:
            weight, height_cm = map(float, data.decode().split())

            # Calculate BMI and determine the category
            bmi = calculate_bmi(weight, height_cm)
            category = get_bmi_category(bmi)

            # Prepare the response string
            response = f"BMI: {bmi:.2f}, Category: {category}"

        except ValueError:
            # Handle invalid input (e.g., non-numeric values)
            response = "Error: Invalid input. Please provide numeric values for weight and height."

        # Send the response back to the client
        server_socket.sendto(response.encode(), client_address)

    except Exception as e:
        # General error handling for the server
        print(f"An error occurred: {str(e)}")
