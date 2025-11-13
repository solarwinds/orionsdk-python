import orionsdk

server = 'orion_server'
username = 'username'
password = 'password'

# The structure of the payload required for the verbs (Enable|Disable)Sensors is not straight-forward.
# Below is what the payload should look like:

# payload_template = [
#     {'HardwareInfoID': int, 'HardwareCategoryStatusID': int, 'UniqueName': str},
# ]
# Notice that you can supply multiple sensors in the payload.

# This script shows how to create a payload to disable/enable every sensor -
#  on a particular node by supplying the node's IP address.
#  This could be re-written to target specific/individual sensors.


def main():
    ip_address = '192.168.1.1'  # Change this value to the node you want to target.
    payload = collect_sensor_data(ip_address=ip_address)
    change_sensor_state(payload, enabled=True)  # Change the enabled bool if you want to disable sensors.


def sensor_payload(hardware_info_id: int, hardware_category_status_id: int, unique_name: str):
    data = {
        'HardwareInfoID': hardware_info_id,
        'HardwareCategoryStatusID': hardware_category_status_id,
        'UniqueName': unique_name
    }
    return data


def change_sensor_state(payload, enabled=True):
    # Defaults to the sensor being enabled unless enabled flag is set to False.
    if enabled:
        verb = 'EnableSensors'
    else:
        verb = 'DisableSensors'
    client = orionsdk.SwisClient(server, username, password)
    client.invoke('Orion.HardwareHealth.HardwareItemBase', verb, payload)


def collect_sensor_data(ip_address):

    # Hardware Sensors are tied to the node via the Node ID.
    #  Collect the NodeID by supplying the IP address of the node.
    # This query assumes that we will only get one result back (targeting index 0 of the results)
    #  You could target another index value or restructure this code if you need to accommodate multiple results.
    client = orionsdk.SwisClient(server, username, password)
    node_id = client.query(
        "SELECT NodeID, IPAddress "
        "FROM Orion.Nodes "
        f"WHERE IPAddress = '{ip_address}' "
    )['results'][0]['NodeID']

    # Collect all the Hardware Sensors on that Node.
    hardware_sensors = client.query(
        "SELECT HardwareInfoID, HardwareCategoryStatusID, UniqueName "
        "FROM Orion.HardwareHealth.HardwareItem "
        f"WHERE HardwareInfoID = '{node_id}' "
    )['results']

    sensor_list = []
    # Loop through the results and add every sensor to a list to generate the payload
    for sensor in hardware_sensors:
        hardware_info_id = sensor['HardwareInfoID']
        hardware_category_status_id = sensor['HardwareCategoryStatusID']
        unique_name = sensor['UniqueName']
        sensor_list.append(sensor_payload(hardware_info_id, hardware_category_status_id, unique_name))

    return sensor_list


if __name__ == '__main__':
    main()
