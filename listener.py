import json
import socket

RSSI_VALUES = dict()
MEDIAN_RSSI = dict()

# create a socket for listening to M5Stick messages
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 8000))
print("Listening...")

# track names of nearby wifi networks
WIFI_NAMES = ("eduroam", "UAL-IoT", "UAL-WiFi", "UAL-Guest-WiFi", "Igloo")


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
        # continue if the network isn't in the list
        if d[key]["name"] not in WIFI_NAMES:
            continue

        combined_name = f"{d[key]['name']}-{key}"

        # create a new dictionary entry if this has not been seen before
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
