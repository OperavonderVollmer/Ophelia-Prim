from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__("Stats")

    def execute(self):
        cpu_usage = opheNeu.psutil.cpu_percent(interval=1)
        ram = opheNeu.psutil.virtual_memory()
        ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
        ram_usage = (f"{ram.percent}%")
        try:
            cpu_temp = (f"{(opheNeu.computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
        except:
            cpu_temp = "Currently Unavailable"
        text = (f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}\nRAM Available: {ram_available}\nCPU Temperature: {cpu_temp}")
        print(text)
        return text

def get_plugin():
    return plugin()

