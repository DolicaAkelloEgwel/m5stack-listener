import socket
import json

RSSI_VALUES = dict()
MEDIAN_RSSI = dict()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 8000))

names = ("eduroam", "UAL-IoT", "UAL-WiFi", "UAL-Guest-WiFi", "Igloo")

print("Listening...")


def calculate_median(vals):
    mid_index = 50 // 2
    ordered = sorted(vals)
    return (ordered[mid_index - 1] + ordered[mid_index]) / 2


counter = 0

while counter < 200:

    data, addr = sock.recvfrom(2048)
    data = data.decode()
    d = json.loads(data)
    print("Received data.")

    for key in d.keys():
        if d[key]["name"] not in names:
            continue

        combined_name = f"{d[key]['name']}-{key}"
        if combined_name not in RSSI_VALUES:
            RSSI_VALUES[combined_name] = []

        if len(RSSI_VALUES[combined_name]) < 50:
            RSSI_VALUES[combined_name].append(d[key]["rssi"])

    counter += 1
    if len(RSSI_VALUES) > 10 and all(
        [len(vals) == 50 for vals in RSSI_VALUES.values()]
    ):
        break

MEDIAN_RSSI = {
    key: calculate_median(RSSI_VALUES[key])
    for key in RSSI_VALUES
    if len(RSSI_VALUES[key]) == 50
}

for key in MEDIAN_RSSI:
    print(f"{key}: {MEDIAN_RSSI[key]}")

exit()
