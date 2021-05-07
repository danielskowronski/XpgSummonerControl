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

        for i in range(0,3):
          self.hidraw.send_feature_report([0x07, 0xa6, 0x00, 0x4d, 0x00, 0x00, 0x00, profileID])
          self.hidraw.get_feature_report(0,32)

    def setColorForProfile(self, profileID, red, green, blue):
        if not (profileID in range(0,5)):
            raise Exception("wrong profile ID")
        if not (red in range(0,256)):
            raise Exception("red must be 0x00-0xFF (0-255)")
        if not (green in range(0,256)):
            raise Exception("green must be 0x00-0xFF (0-255)")
        if not (blue in range(0,256)):
            raise Exception("blue must be 0x00-0xFF (0-255)")

        for i in range(0,3):
          self.hidraw.send_feature_report([0x07, 0xa3, 0x00, profileID, 0x00, 0x3e, red, green, blue])
          self.hidraw.get_feature_report(0,32)
          self.hidraw.send_feature_report([0x07, 0xea, 0x04])
          self.hidraw.get_feature_report(0,32)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=
        'XpgSummonerControl - control ADATA XPG Summoner keyboard backlight (RGB) and profiles')
    subparsers = parser.add_subparsers(help='commands',dest='cmd')

    switchProfile_parser = subparsers.add_parser('switch_profile')
    switchProfile_parser.add_argument('--profile', type=int, choices=range(0,5),required=True, help='profile number; F1 is 0, F2 is 1, ...')

    setColor_parser = subparsers.add_parser('set_color')
    setColor_parser.add_argument('--profile', type=int, choices=range(0,5),  required=True, help='profile number; F1 is 0, F2 is 1, ...')
    setColor_parser.add_argument('--red',     type=int, choices=range(0,256),required=True, help='red value')
    setColor_parser.add_argument('--green',   type=int, choices=range(0,256),required=True, help='green value')
    setColor_parser.add_argument('--blue',    type=int, choices=range(0,256),required=True, help='blue value')  

    args = parser.parse_args()
    xsc = XpgSummonerControl()

    if args.cmd=='switch_profile':
        xsc.selectProfile(args.profile)
    if args.cmd=='set_color':
        xsc.setColorForProfile(args.profile, args.red, args.green, args.blue)
