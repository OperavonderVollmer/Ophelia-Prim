from features.opheliaPluginTemplate import opheliaPlugin
import opheliaNeurals as opheNeu
import opheliaPlugins as ophePlu

class plugin(opheliaPlugin):
    def __init__(self):
        super().__init__(name="Posture", prompt="How many minutes would you like Ophelia to check your posture? Say 0 or False to deactivate", description="Ophelia shall give Master a posture check", needsArgs=True, operaOnly=True)

# call prepExecute to speak the prompt, and get args. If hasModes is true, will return an array instead
    def postureCheckSetup(self, t):
        try:
            t = t.replace(" minutes", "")
            t = ophePlu.normalizeNumber(t)
            if t := isinstance(t, bool) == True: 
                if t == True: t = opheNeu.defaultPostureInterval
                else: t = False  
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
                checks = 6
                sleep = 10                       # no of checks * sleep MUST equal 60    
                totalChecks = interval * checks   
                opheNeu.debug_log(f"Total Checks {totalChecks}")             
                while opheNeu.postureCheckActive:            
                    c = 1
                    for _ in range(totalChecks):
                        if not opheNeu.postureCheckActive or not opheNeu.opheliaRequired:
                            opheNeu.debug_log("Posture check deactivated due to posture check being deactivated")
                            return True
                        opheNeu.debug_log(f"Debug message within the posture loop #{c}", True)
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

                #command = number of seconds
    def cheatResult(self, **kwargs):
        return self.postureCheckSetup(kwargs["command"])
    
def get_plugin():
    return plugin()

