import hid
from time import sleep

class XpgSummonerControl:

    def __init__(self, vid=0x125f, did=0x9418):
        self.hidraw = hid.device(vid,did)
        while True:
            try:
                self.hidraw.open(vid,did)
                break
            except Exception:
                pass
    def selectProfile(self, profileID):
        if not (profileID in range(0,5)):
            raise Exception("wrong profile ID")

        for i in range(1,3):
          self.hidraw.send_feature_report([0x07, 0xa6, 0x00, 0x4d, 0x00, 0x00, 0x00, profileID])
          self.hidraw.get_feature_report(0,32)

xsc = XpgSummonerControl()

for p in range(0,5):
    print(p)
    xsc.selectProfile(p)
    sleep(3)