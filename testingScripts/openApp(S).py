import os

def openApp(target):
    root_dir = os.path.dirname(os.path.abspath(__file__)) 
    shortcutPath = os.path.join(root_dir, "shortcuts", target)  
    shortcutPath += ".lnk"
    if os.path.exists(shortcutPath): 
        try:
            os.startfile(shortcutPath)  
            return(f"Opening {target}...")
        except Exception as e: print(f"An error occurred: {str(e)}")
    else:
        return(f"Shortcut '{target}' not found.")

openApp("notepad")  
