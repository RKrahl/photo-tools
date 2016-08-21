"""Provide the class IdxItem which represents an item in the index.
"""

import os.path
import hashlib
from photo.exif import Exif
from photo.geo import GeoPosition


def _checksum(fname, hashalg):
    """Calculate hashes for a file.
    """
    if not hashalg:
        return {}
    m = { h:hashlib.new(h) for h in hashalg }
    chunksize = 8192
    with open(fname, 'rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            for h in hashalg:
                m[h].update(chunk)
    return { h: m[h].hexdigest() for h in hashalg }


class IdxItem(object):

    def __init__(self, data=None, filename=None, basedir=None, hashalg=['md5']):
        if data is not None:
            self.filename = data.get('filename')
            self.checksum = data.get('checksum', {})
            if not self.checksum and 'md5' in data:
                # legacy: old index file format used to have a 'md5'
                # attribute, rather then 'checksum'.
                self.checksum['md5'] = data['md5']
            self.createDate = data.get('createDate')
            if self.createDate is None and 'createdate' in data:
                # legacy: 'createDate' used to be 'createdate' in old
                # index file format.
                self.createDate = data['createdate']
            self.orientation = data.get('orientation')
            self.gpsPosition = data.get('gpsPosition')
            self.tags = set(data.get('tags', []))
        elif filename is not None:
            self.filename = filename
            if basedir is not None:
                filename = os.path.join(basedir, filename)
            self.checksum = _checksum(filename, hashalg)
            exifdata = Exif(filename)
            self.createDate = exifdata.createDate
            self.orientation = exifdata.orientation
            self.gpsPosition = exifdata.gpsPosition
            self.tags = set()
        if self.gpsPosition:
            self.gpsPosition = GeoPosition(self.gpsPosition)

    def as_dict(self):
        d = {
            'filename': self.filename,
            'checksum': self.checksum,
            'createDate': self.createDate,
            'orientation': self.orientation,
            'gpsPosition': self.gpsPosition,
            'tags': sorted(self.tags),
        }
        if d['gpsPosition']:
            d['gpsPosition'] = d['gpsPosition'].as_dict()
        return d
