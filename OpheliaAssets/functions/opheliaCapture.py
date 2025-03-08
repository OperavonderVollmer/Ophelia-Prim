import mss
import numpy as np
import cv2
import time
import win32api
import threading
from queue import Queue

"""

Algorithm

1. Capture screen with mss
2. Extract text and detect language from the screen with easy ocr
3. If non-English, translate using googletrans
4. Overlay translated text on the screen with cv2

"""

class Monitor:
    """
        The monitor object. Attributes iter, dict, and repr are defined

        Properties:
            height: The height of the monitor
            width: The width of the monitor
            monitor: The monitor object
    """
    def __init__(self, sct, index: int = 1):
        self._sct = sct
        self._monitor_index = index
        self._monitor = sct.monitors[self._monitor_index]
    
    @property
    def name(self): 
        __monitors = win32api.EnumDisplayMonitors()
        __device_info = win32api.GetMonitorInfo(__monitors[self._monitor_index - 1][0])
        return __device_info["Device"]
    @property
    def height(self) -> int: return self._sct.monitors[self._monitor_index]["height"]
    @property
    def width(self) -> int: return self._sct.monitors[self._monitor_index]["width"]    
    @property
    def monitor(self):
        return self._monitor    


    def __iter__(self): 
        yield from self._monitor.items()
    def __dict__(self):
        return dict(self._monitor)   
    def __repr__(self): 
        return f"Monitor: `{self.name}` (width={self.width}, height={self.height})"

class Snatcher:
    """
        Params:
            sct: The mss object for sct
            refreshRate: int = The refresh rate of the monitor
            capturer: str = Which capturer to use, only mss is supported right now. Will add Desktop Duplicator later
    """
    def __init__(self, refreshRate: int, capturer: str, sct: mss.mss = None):
        self._sct = sct if sct else None
        self._refreshRate = refreshRate
        self._running = False
        self._fps_timer = time.perf_counter()
        self._frame_counter = 0
        self._capturer = capturer
        self._fps = 0

    @property
    def fps(self): return self._fps

    def trackFrames(self):
        """
            NOT A TOOL TIP

            From what I understand, this is how it goes. Sets the time to now, then checks if the time between checks is greater than 1. If so, proceeds.

            Divides the number of frames generated between checks by the time between checks, this is to ensure that I'm actually capturing the fps based on the refresh rate

            Prints the fps then resets the counter

        """
        now = time.perf_counter()
        if now - self._fps_timer >= 1:
            fps = self._frame_counter / ( now - self._fps_timer )
            print(f"Snatcher FPS: {fps}")
            self._fps = fps
            self._fps_timer = now
            self._frame_counter = 0
        

    def startCapture(self, monitor: Monitor):
        """
            Captures the screen at a given refresh rate. Locks the framerate as it does
        """
        m = monitor.monitor
        self._running = True

        capture_methods = {
            "mss": self.mssCapture,
            "dda": self.ddaCapture
        }
        try:
            chosenCapturer = capture_methods[self._capturer]
        except KeyError:
            raise NotImplementedError

        while self._running:
            start = time.perf_counter()
            try:
                _screenshot = chosenCapturer(m)
                yield _screenshot

                self._frame_counter += 1
                self.trackFrames()
            except Exception as e:
                print(e)
                continue
            elapsed = time.perf_counter() - start
            remaining = max (0, 1 / self._refreshRate - elapsed)
            time.sleep(remaining)

    def mssCapture(self, monitor):
        return self._sct.grab(monitor)
    
    def ddaCapture(self, monitor):
        raise NotImplementedError

    def stopCapture(self): self._running = False            

class Displayer:
    def __init__(self, refreshRate: int, capturer: str):
        self._refreshRate = refreshRate
        self._running = False
        self._start_time = time.time()
        self._fps = 0
        self._fps_timer = time.perf_counter()
        self._frame_counter = 0
        self._frame_queue = Queue(maxsize=10)
        self._display_thread = None

    @property
    def fps(self): return self._fps

    class ClosedStream(Exception): 
        """Raised when the video stream is closed."""
        def __init__(self, message="Stream is closed"):
            super().__init__(message)            
            cv2.destroyAllWindows()
            time.sleep(.1)

    def trackFrames(self):
        now = time.perf_counter()
        if now - self._fps_timer >= 1:
            fps = self._frame_counter / ( now - self._fps_timer )
            print(f"Displayer FPS: {fps}")
            self._fps = fps
            self._fps_timer = now
            self._frame_counter = 0

    def drawFPSCounter(self, frame):
        text = f"FPS: {self._fps: .2f}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return frame

    def displayThis(self, frame):
        if not self._running:
            print("Please properly start the display")
            raise self.ClosedStream

        if not self._frame_queue.full():
            self._frame_queue.put(frame)
        else:
            print("Frame queue is full, dropping frame")
        
        if not self._display_thread or not self._display_thread.is_alive():
            self.startDisplay()
        
    def _display_loop(self):
        try:
            while self._running:
                if not self._frame_queue.empty():
                    frame = self._frame_queue.get()
                    self._frame_counter += 1
                    self.trackFrames()

                    frame = np.array(frame)

                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    frame = self.drawFPSCounter(frame)
                    cv2.imshow("Ophelia Capture", frame)
                    cv2.resizeWindow("Ophelia Capture", 1920, 1080)

                    if cv2.waitKey(int(1000 / self._refreshRate)) & 0xFF == 27:
                        self._running = False
                        break
                else:
                    time.sleep(.25)

            raise self.ClosedStream
        except self.ClosedStream:
            pass

    def startDisplay(self): 
        self._running = True
        self._display_thread = threading.Thread(target=self._display_loop, daemon=True)
        self._display_thread.start()

    def stopDisplay(self): self._running = False

    def __del__(self): 
        cv2.destroyAllWindows()
        pass

class Linguist:
    def __init__(self):
        self._running = False


    def startLinguist(self): self._running = True
    def stopLinguist(self): self._running = False


class LargeMaid:
    """
        Captures the screen
    """

    def __init__(self, refreshRate: int, capturer: str = "mss"):
        self._capturer = capturer
        self._sct = mss.mss() if capturer == "mss" else None
        self._refreshRate = refreshRate
        self._monitor = Monitor(self._sct)
        self._snatch = Snatcher(sct=self._sct, refreshRate=self._refreshRate, capturer=self._capturer)
        self._display = Displayer(refreshRate=self._refreshRate, capturer=self._capturer)
        self.lock = threading.Lock()
        self._errorCount = 0
        self._reveal = False

    @property
    def reveal(self): return self._reveal
    @reveal.setter
    def reveal(self, value): self._reveal = value

    def stop(self): 
        self._snatch.stopCapture()
        self._display.stopDisplay()

    def run(self):
        with self.lock:
            try:
                self._display.startDisplay() if self._reveal else None
                for frame in self._snatch.startCapture(self._monitor):
                    if self._reveal:
                        self._display.displayThis(frame)




            except NotImplementedError as e:
                self._errorCount += 1
                print(f"Invalid capturer. Error: {e}")
                if self._errorCount >= 3:
                  self._errorCount = 0
                  return
                print("Defaulting to mss.")
                self._snatch.stopCapture()
                self._snatch = None
                self._snatch = Snatcher(sct=self._sct, refreshRate=self._refreshRate, capturer="mss")
                self.run()

            except Displayer.ClosedStream as e: 
                return


            except Exception as e:
                self._errorCount += 1
                print(f"An error of type {type(e).__name__} occurred. Error Count {self._errorCount}. Verbose: {e}")
                if self._errorCount >= 3:
                  self._errorCount = 0
                  print("Failed three times, silently failing...")
# TODO: After adding opheliaCapture to main branch, add opheliaNeural's logging here 
                  return
                print("Retrying in 5 seconds...")
                time.sleep(5)
                self.run()


    @property
    def monitor (self): return self._monitor   


if __name__ == "__main__":
    
    lm = LargeMaid(24)
    lm.reveal = True
    lm.run()
