"""Define filter for photo indices by command line arguments.
"""

import re
import datetime
from photo.geo import GeoPosition


class IdxFilter(object):

    def __init__(self, args):
        if args.tags is not None:
            self.taglist = set()
            self.negtaglist = set()
            if args.tags:
                for t in args.tags.split(","):
                    if t.startswith("!"):
                        self.negtaglist.add(t[1:])
                    else:
                        self.taglist.add(t)
        else:
            self.taglist = None
            self.negtaglist = None
        self.date = args.date
        if args.gpspos:
            self.gpspos = GeoPosition(args.gpspos)
            self.gpsradius = args.gpsradius
        else:
            self.gpspos = None
        self.filelist = set(args.files) if args.files else None

    def __call__(self, item):
        if self.filelist and not item.filename in self.filelist:
            return False
        if self.taglist is not None:
            if not self.taglist <= item.tags:
                return False
            if self.negtaglist & item.tags:
                return False
            if not self.taglist and not self.negtaglist and item.tags:
                return False
        if self.date and (item.createDate < self.date[0] or 
                          item.createDate >= self.date[1]):
            return False
        if self.gpspos:
            if (not item.gpsPosition or
                (item.gpsPosition - self.gpspos) > self.gpsradius):
                return False
        return True


_datere = re.compile(r'''^
    (?P<y0>\d{1,})-(?P<m0>\d{1,2})-(?P<d0>\d{1,2})
    $''', re.X)

def _strpdate(s):
    match = re.match(_datere, s)
    if match:
        y, m, d = match.group('y0', 'm0', 'd0')
        try:
            startdate = datetime.datetime(int(y), int(m), int(d))
            enddate = startdate + datetime.timedelta(days=1)
            return (startdate, enddate)
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("Invalid date value '%s'" % s)

def addFilterArguments(argparser):
    argparser.add_argument('--tags', 
                           help="select images by comma separated list of tags")
    argparser.add_argument('--date', type=_strpdate, 
                           help="select images by date")
    argparser.add_argument('--gpspos', 
                           help="select images by GPS position")
    argparser.add_argument('--gpsradius', type=float, default=3.0, 
                           help="radius around GPS position in km", 
                           metavar='DISTANCE')
    argparser.add_argument('files', nargs='*', 
                           help="select images by file name")
    return argparser
