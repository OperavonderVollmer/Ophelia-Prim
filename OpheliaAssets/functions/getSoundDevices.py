import sounddevice as sd
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, CLSCTX_ALL
from ctypes import cast, POINTER
print(sd.query_devices())
print("\n-------------------------------------\n")

# Get only output devices
output_devices = [device for device in sd.query_devices() if device['max_output_channels'] > 0]

for i, device in enumerate(output_devices):
    print(f"{i}: {device['name']}")

def get_device_guid(device_name):
    """
    Retrieves the GUID of an audio device by its name.

    Args:
        device_name (str): The name of the audio device.

    Returns:
        str: The GUID of the device, or None if not found.
    """
    devices = AudioUtilities.GetSpeakers()  # Gets the default speakers (playback)
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    devices = AudioUtilities.GetAllDevices()

    for device in devices:
        print(device.FriendlyName)
        if device.FriendlyName == device_name:
            return device.id #This is the GUID.
    return None

# Example usage:
device_name = "SteelSeries Sonar - Microphone (SteelSeries Sonar Virtual Audio Device)" # Replace with the correct device name
guid = get_device_guid(device_name)
print(guid)
