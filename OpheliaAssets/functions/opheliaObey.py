from functions import opheliaMouth, opheliaCareKit
import opheliaPlugins as ophePlu
import opheliaNeurals as opheNeu

def opheliaDo(command, speechSource=True, isLoud=True):
    command = command.lower()
    if command.__contains__("command"):
        command = command[8:]
        try:
            for plugin in ophePlu.plugins:
                if command.__contains__(plugin.lower()):  
                    print(f"Command Recognized: {str(plugin)}")
                    command = command.replace(plugin.lower(), "").strip()

                    output = ophePlu.plugins[plugin].cheatResult(command) if not speechSource else ophePlu.plugins[plugin].execute()

                    if output and isLoud and output != "556036":
                        def outputThread():
                            ophePlu.plugins["Transmission"].audioThroughMic(output, True, False)
                        thre = opheNeu.thr.Thread(target=outputThread)
                        thre.start()
                    return output
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    elif command.__contains__("ophelia"):
        opheliaMouth.opheliaSpeak(opheliaCareKit.opheliaCareKit())

