import socket
import time
import json
import os
from datetime import datetime,timedelta

LOG_FILE_INTERVAL = 5 * 60
LOG_FILE_EXPIRATION = 10 * 60

def send_request(machine):
    stx = b'\x4b'
    etx = b'\x0d\x0a'
    responses = {}

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((machine['ip'], int(machine['port'])))
        log_message = f"Epoch_time : {int(time.time())} : Connected to machine {machine['machine id']} at {machine['ip']}:{machine['port']}"

        request = stx + etx
        client_socket.send(request)

        response = client_socket.recv(2056)
        hex_response = response.hex()
        log_message += f"\nEpoch_time : {int(time.time())} : Response from machine {machine['machine id']}"

        responses['machine_id'] = machine['machine id']
        responses['ip'] = machine['ip']
        responses['port'] = machine['port']
        responses['data'] = hex_response

        with open(f"response_machine{machine['machine id']}.json", "w") as json_file:
            json.dump(responses, json_file)

        log_message += f"\nEpoch_time : {int(time.time())} : Response for machine {machine['machine id']} saved to response_machine_{machine['machine id']}.json"
    
    except Exception as e:
        log_message = f"Epoch_time : {int(time.time())} : Connection to machine {machine['machine id']} failed: ip {machine['ip']}"
    
    finally:
        client_socket.close()

    with open_log_file() as log_file:
        log_file.write(log_message + "\n")
    
def open_log_file():
    log_file_path = get_current_log_file_path()
    return open(log_file_path, "a")

def get_current_log_file_path():
    log_file_prefix = "log_file"
    log_file_extension = ".txt"
    current_time = int(time.time())
    log_file_number = current_time // LOG_FILE_INTERVAL + 1

    log_file_path = f"{log_file_prefix}{log_file_number}{log_file_extension}"
    delete_old_log_files(current_time)
    return log_file_path

def delete_old_log_files(current_time):
    log_file_prefix = "log_file"
    log_file_extension = ".txt"
    for log_file_name in os.listdir():
        if log_file_name.startswith(log_file_prefix) and log_file_name.endswith(log_file_extension):
            log_file_path = os.path.join(log_file_name)
            creation_time = os.path.getctime(log_file_path)
            if current_time - creation_time > LOG_FILE_EXPIRATION:
                os.remove(log_file_path)
                print(f"Deleted old log file: {log_file_path}")


def run_requests(machines, delay_minutes):
    
    for machine in machines:
        send_request(machine)

    time.sleep(delay_minutes * 60)

if __name__ == '__main__':
    while True:
        with open("./machines.json", "r") as machines_file:
            machines_data = json.load(machines_file)
            machines = machines_data["machines"]

        delay_minutes = machines_data["information"]["delay"]

        run_requests(machines, delay_minutes)



