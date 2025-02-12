import wmi, psutil, time

computer = wmi.WMI(namespace="root\\wmi") #exported
drives = ['C:/', 'B:/', 'C:/']

#exported
def getCPUStats():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total = (f"{ram.total / (1024 ** 3):.2f} GB")
    ram_available = (f"{ram.available / (1024 ** 3):.2f} GB")
    ram_usage = (f"{ram.percent}%")
    cpu_temp = (f"{(computer.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10) - 273.15:.2f}°C")
#exported


def getDiskStats():    
    return "Not working rn"
        
def getComputerSpecs():  
    for cpu in computer.Win32_Processor():
        print(f"Processor: {cpu.Name}")
        print(f"Logical Cores: {cpu.NumberOfLogicalProcessors}")
        print(f"Max Clock Speed: {cpu.MaxClockSpeed} MHz")
    for drive in drives:
        usage = psutil.disk_usage(drive)
        total = usage.total / (2**30)  # Convert bytes to GiB
        used = usage.used / (2**30)
        free = usage.free / (2**30)
        percent = usage.percent
        print(f"Drive {drive}:")
        print(f"  Total: {total:.2f} GiB")
        print(f"  Used: {used:.2f} GiB")
        print(f"  Free: {free:.2f} GiB")
        print(f"  Utilization: {percent}%")
        print("-" * 30)


getCPUStats()