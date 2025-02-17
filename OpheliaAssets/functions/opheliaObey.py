from functions import opheliaMouth, opheliaCareKit

def opheliaDo(command, commandMap):
    if command.__contains__("command"):
        try:
            for keyword, response in commandMap.items():
                if keyword in command:
                    print(f"Command Recognized: {str(keyword)}")    
                    opheliaMouth.opheliaSpeak(f"{response(keyword) if callable(response) else response}")
        except Exception as e:
            print(e)
            return(f"Command cannot be executed")
    elif command.__contains__("ophelia"):
        opheliaMouth.opheliaSpeak(opheliaCareKit.opheliaCareKit())