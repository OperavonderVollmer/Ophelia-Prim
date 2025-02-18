import time
from datetime import datetime 
interval = 1 # minutes
postureCheckActive = True
minutes = 0
while True:
    # no of checks * sleep MUST equal 60
    checks = 12
    sleep = 5
    testCheck = checks
    for _ in range(interval * checks):
        if not postureCheckActive:
            print("Posture check deactivated due to posture check being deactivated")
            break
        if minutes % interval == 0 and minutes != 0: testCheck = checks; print(f"{minutes} minutes have passed...")
        testCheck -= 1; print(testCheck)
        time.sleep(sleep)
        
    print("audioThroughMic(opheNeu.getRandomDialogue(), True, False)")
    print(f"Playing posture audio {datetime.now()}")
print("Posture check deactivated due to posture duration being over")