import numpy as np
import yaml
import json

# Given a JSON packet as a string...
# (each entry in the xlsx files will be a JSON string)


# TOF data will be inside the JSON packets that contain keywords like 'luminance' or 'accelerometer_x'/y/z
json_string = "{'luminance': 60, 'battery_voltage': 4266, 'roi_values': '62635D5C', 'accelerometer_y': 0.0, 'accelerometer_x': -585.9375, 'captured_by': {'0': {'0000000028c7b980': -85}}, 'accelerometer_z': -789.0625, 'raw': '010462635D5CAA10013CB5009B1600', 'captured_at': '2023-01-16T14:06:31.589Z', 'luminance_in_mv': 22, 'pir_triggered': True, 'pir_error': False, 'crc': True, 'pir_event_counter': 1}"
# 1) Convert string to JSON (equivalent to a python dict)
json_dict = yaml.load(json_string, Loader=yaml.FullLoader)
# print(json.dumps(json_dict, indent=4))
# 2) TOF data is saved under the keyword 'roi_values'
tof_roi_values = json_dict['roi_values']
# 3) Data is saved a a HEX string. In order to get the values per pixel you split 1D4C05AA into a list of pairs like 1D 4C 05 AA
# 4) Each value sent is divided by two (to save allocated bits in BLE transmission protocols)
# So to get the actual value to convert teh base 16 value into base 10 and multiply by two
tof_roi_values = [int(x+y,16)*2 for x,y in zip(tof_roi_values[::2], tof_roi_values[1::2])]
# This is the distance the sensor sears from itself to the target in cm
# Note: sensor readings are adaptive. The Tof data can be in 2x2 or 3x3 mode.
# We can know this by simply measuring the lenght of out list
# 5) When standing at the base of the beed at facing it, sensor readings are from top-right to bottom-left
# So the readings in matrix form would then look like this
current_tof_resolution = int(len(tof_roi_values)*.5)
tof_data_matrix = np.array(tof_roi_values).reshape((current_tof_resolution, current_tof_resolution))
# Flip left to right so it's top-right to bottom-left
tof_data_matrix = np.fliplr(tof_data_matrix)
# Result
print('TOF raw readings:', tof_roi_values)
print('Decoded TOF data:\n', tof_data_matrix)
print('\n\n')



# Thermal data will be inside JSON packets that contain the keyword 'type' with value 'THERMAL_ROI'
json_string = "{'crc': True, 'captured_by': [{'0': {'0000000028c7b980': -87, '00000000dedd8941': -78, '0000000090de2ebf': -75, '10000000f01b4c9d': -84, '00000000e4540cab': -80, '0000000053816128': -82}, '1': {'0000000028c7b980': -86, '00000000dedd8941': -77, '0000000090de2ebf': -74, '10000000f01b4c9d': -88, '00000000e4540cab': -79, '0000000053816128': -82}}, {'0': {'0000000028c7b980': -88, '00000000dedd8941': -83, '0000000090de2ebf': -74, '10000000f01b4c9d': -86, '00000000e4540cab': -83, '0000000053816128': -78, '00000000ccfdc71e': -86}, '1': {'0000000090de2ebf': -75}}], 'captured_at': '2023-01-16T14:07:13.911Z', 'type': 'THERMAL_ROI', 'roi': '2728272C272527282D2B2D3D362A2B2B2F2D303D3A2D2C2C30303033322F2D2D31313132302F2E31312F3132323533373431323230373A3E3535343434393B3E', 'version': 1}"
# 1) Convert string to JSON
json_dict = yaml.load(json_string, Loader=yaml.FullLoader)
# print(json.dumps(json_dict, indent=4))
# 2) Thermal data is saved under the keyword 'roi'
thermal_roi_values = json_dict['roi']
# 3) Data is saved in a hex string like before. It is sent in increments of 0.25 degrees starring from a minimum value of 10
thermal_roi_values = [10+int(x+y,16)*.25 for x,y in zip(thermal_roi_values[::2], thermal_roi_values[1::2])]
# 4) When standing at the base of the base faving it, the readings are top-left to bottom-right
thermal_data_matrix = np.array(thermal_roi_values).reshape((8, 8))
# 5) The readings have internal noise. To correct it we add a bias. This is a fixed value
THERMAL_BIAS = [
    [ 2.8,   2.49,  2.41,  2.52,  2.41,  2.25,  2.38,  2.28],
    [ 1.62,  1.77,  1.36,  1.67,  1.83,  1.59,  1.46,  1.37],
    [ 0.9,   1.38,  0.92,  0.99,  0.99,  1.25,  1.08,  0.99],
    [ 0.71,  0.69,  0.94,  0.66,  0.62,  0.68,  0.95,  0.87],
    [ 0.26,  0.41,  0.61,  0.35,  0.65,  0.56,  0.8,   0.43],
    [ 0.36,  0.47,  0.48,  0.18,  0.19,  0.44,  0.3,   0.08],
    [-0.52,  0.03, -0.19, -0.15,  0.27,  0.04, -0.05,  -0  ],
    [-0.78, -0.89, -0.72, -0.63, -0.55, -0.3,  -0.39, -0.88]
]
thermal_data_matrix = thermal_data_matrix + THERMAL_BIAS
# Result
print('Thermal raw readings:', thermal_roi_values)
print('Decoded TOF data:\n', thermal_data_matrix)
print('\n\n')


# PIR data will be in packets that contain the field "seconds" and/or "pir_data"
json_string = "{'seconds': 4260, 'error_state': '00', 'pir_data': '40', 'crc': True, 'captured_by': {'0': {'00000000e4540cab': -81}}, 'hundredsOfSeconds': 41, 'pir_data_count': 1, 'raw': 'A41000002927000140', 'captured_at': '2023-01-16T14:06:32.028Z', 'interval': 1.625}"
# 1) Convert string to JSON (equivalent to a python dict)
json_dict = yaml.load(json_string, Loader=yaml.FullLoader)
# 2) Data is saved under 'pir_data'. To decode it...
pirData = int(json_dict['pir_data'], 16)
active_pirs = []
for pos in range(8):
    if (0 == pirData & (1 << pos)):
        # PIR indices are the positions in a Byte. So 0100 0000 means position 7-PIR is active
        # Multiple PIRs can be active inside one packet
        continue
    active_pirs.append(pos+1)
# active_pirs then tells you which PIRs were recently active
# To combine them, you need to use a mooving window. We use a 300ms window
# How to resolve thze crossings exactly refer to the PIR matrix specification pptx
# PIR matrix layout:
#
#             1
#
#             2
#     5   6       7   8
#             3
#
#             4
# So if 1 and 5 are active within some moving window, the crossing would be (where the X)
#
#      X      1
#
#             2
#     5   6       7   8
#             3
#
#             4
# Result
print('PIR raw readings (base 16):', json_dict['pir_data'])
bits = bin(int(json_dict['pir_data'], 16))[2:].zfill(8)
print('PIR readings base 2:', bits)
print('Active PIRs', active_pirs)


# NOTE: all packets will contain a field called 'crc'. This value has to be True. If not the data can be discarded. (this is a checksum flag)
