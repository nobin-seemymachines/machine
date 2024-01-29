import socket
import time
import json

def send_request(machine):
    stx = b'\x4b'
    etx = b'\x0d\x0a'
    responses = {}

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((machine['ip'], int(machine['port'])))
        log_message = f"Epoch_time : {int(time.time())} : Connected to machine {machine['machine id']} at {machine['ip']}:{machine['port']}"

        # Send only one request
        request = stx + etx
        client_socket.send(request)

        response = client_socket.recv(2056)
        hex_response = response.hex()
        log_message += f"\nEpoch_time : {int(time.time())} : Response from machine {machine['machine id']}: {hex_response}"

        responses[1] = {"hex_response": hex_response}

        with open(f"response_machine_{machine['machine id']}.json", "w") as json_file:
            json.dump(responses, json_file)

        log_message += f"\nEpoch_time : {int(time.time())} : Response for machine {machine['machine id']} saved to response_machine_{machine['machine id']}.json"
        print(log_message)

    except Exception as e:
        log_message = f"Epoch_time : {int(time.time())} : Connection to machine {machine['machine id']} failed: ip {machine['ip']}"
        print(log_message)

    finally:
        client_socket.close()

    # Log the messages to a text file
    with open("log.txt", "a") as log_file:
        log_file.write(log_message + "\n")

def run_requests(machines, delay_minutes):
    
    for machine in machines:
        send_request(machine)

    # Sleep for the specified delay
    time.sleep(delay_minutes * 60)

if __name__ == '__main__':
    while True:
        with open("machines.json", "r") as machines_file:
            machines_data = json.load(machines_file)
            machines = machines_data["machines"]

        # Set delay time in minutes
        delay_minutes = machines_data["information"]["delay"]

        # Run the requests continuously with the specified delay
        run_requests(machines, delay_minutes)
