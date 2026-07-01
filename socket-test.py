import socket
import json

RSSI_VALUES = dict()
MEDIAN_RSSI = dict()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 8000))

names = ("eduroam", "UAL-IoT", "UAL-WiFi", "UAL-Guest-WiFi")

print("Listening...")


def calculate_median(vals):
    mid_index = 50 // 2
    ordered = sorted(vals)
    return (ordered[mid_index - 1] + ordered[mid_index]) / 2


counter = 0

while counter < 150:

    data, addr = sock.recvfrom(2048)
    data = data.decode()
    d = json.loads(data)
    print("Received data.")

    for key in d.keys():
        if d[key]["name"] not in names:
            continue
        if key not in RSSI_VALUES:
            RSSI_VALUES[key] = []
        RSSI_VALUES[key].append(d[key]["rssi"])

    counter += 1
    if len(RSSI_VALUES) < 10 and not all(
        [len(vals) >= 50 for vals in RSSI_VALUES.values()]
    ):
        break

MEDIAN_RSSI = {key: calculate_median(RSSI_VALUES[key]) for key in RSSI_VALUES}
print(MEDIAN_RSSI)
exit()
