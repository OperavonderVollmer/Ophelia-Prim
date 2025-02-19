from functions import opheliaMouth, opheliaCareKit
import opheliaPlugins as ophePlu

def opheliaDo(command):
    if command.__contains__("command"):
        try:
            for plugin in ophePlu.plugins:
                if command.__contains__(plugin.lower()):  
                    print(f"Command Recognized: {str(plugin)}")
                    output = ophePlu.plugins[plugin].execute()
                    ophePlu.plugins["Transmission"].audioThroughMic(output, True, False) if output else None
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    elif command.__contains__("ophelia"):
        opheliaMouth.opheliaSpeak(opheliaCareKit.opheliaCareKit())

