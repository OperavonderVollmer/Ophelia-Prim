import psutil, wmi
import opheliaNeurals as opheNeu

def getCPUStats():    
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total = (f"{ram.total / (1024 ** 3):.2f} GB")
    ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
    ram_usage = (f"{ram.percent}%")
    try:
        cpu_temp = (f"{(opheNeu.computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
    except:
        cpu_temp = "Currently Unavailable"
    text = (f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}\nRAM Total: {ram_total}\nRAM Available: {ram_available}\nCPU Temperature: {cpu_temp}")
    print(text)
    return text
def opheliaCareKit():
    return "Command Recognized: Unfortunately, this feature hasn't been implemented yet"