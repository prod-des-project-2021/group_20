
from imutils.video import VideoStream
import time

import loging_GUI



vs = VideoStream(usePiCamera=(0)).start()

pba = loging_GUI.Login_GUI(vs)
pba.root.mainloop()
