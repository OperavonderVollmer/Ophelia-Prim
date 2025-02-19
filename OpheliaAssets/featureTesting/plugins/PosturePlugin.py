from featureTesting.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Posture", prompt="How many minutes would you like Ophelia to check your posture? Say 0 or False to deactivate", needsArgs=True)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead
    def postureCheckSetup(self, t):
        try:
            def normalizeNumber(t):
                try:
                    if isinstance(t, str):
                        t = t.strip().lower()
                        if t.isdigit():
                            return int(t)
                        return opheNeu.w2n.word_to_num(t)
                    elif isinstance(t, bool): return opheNeu.defaultPostureInterval
                    else: return t        
                except ValueError: raise
            t = t.replace(" minutes", "")
            t = normalizeNumber(t)
            if t:
                interval = t
                with open(opheNeu.postureCheckFile, "w") as postFile:
                    postFile.write(str(interval))  
                opheNeu.postureCheckActive = True 
                self.postureCheckWrapped()         
                return f"Posture check is set to {interval} minutes."
            else:
                opheNeu.os.remove(opheNeu.postureCheckFile) if opheNeu.postureCheckActive else None
                opheNeu.postureCheckActive = False
                return "Posture check deactivated"
        except ValueError: return "Please provide a valid number of minutes"
    def postureCheckWrapped(self):
        def postureCheck():
            def postureCheckLoopMethod():          
                opheNeu.postureLooping = True
                try:  
                    with open(opheNeu.postureCheckFile, "r") as postFile:
                        interval = int(postFile.read())
                        print(f"interval {interval}")
                except FileNotFoundError: 
                    return "Posture check is currently inactive"            
                opheNeu.debug_log("Posture check loop started")
                checks = 12
                sleep = 5                       # no of checks * sleep MUST equal 60    
                totalChecks = interval * checks   
                opheNeu.debug_log(f"Total Checks {totalChecks}")             
                while opheNeu.postureCheckActive:            
                    c = 1
                    for _ in range(totalChecks):
                        if not opheNeu.postureCheckActive or not opheNeu.opheliaRequired:
                            opheNeu.debug_log("Posture check deactivated due to posture check being deactivated")
                            return True
                        if opheNeu.deepDebugMode: opheNeu.debug_log(f"Debug message within the posture loop #{c}")
                        #ophePlu.plugins["Transmission"].audioThroughMic(f"Debug message within the posture loop #{c}", True, False)
                        c+=1
                        opheNeu.time.sleep(sleep)                        
                    ophePlu.plugins["Transmission"].audioThroughMic(opheNeu.getRandomDialogue("posture"), True, False)
                    print(f"Playing posture audio {opheNeu.datetime.now()}")
                opheNeu.debug_log("Posture check deactivated due to posture duration being over")

            if not opheNeu.postureLooping and opheNeu.postureCheckActive: 
                postureLoop = opheNeu.thr.Thread(target=postureCheckLoopMethod, daemon=True)
                postureLoop.start()
                postureLoop.join()
                return
            else: return "Posture check is already active"
        postureThread = opheNeu.thr.Thread(target=postureCheck)
        print(f"Posture check starting at {opheNeu.datetime.now()}...")
        postureThread.start()

    def execute(self):
        target = self.prepExecute()
        return self.postureCheckSetup(target)

def get_plugin():
    return plugin()

