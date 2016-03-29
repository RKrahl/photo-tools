"""Provide the class Index which represents an index of photos.
"""

import os
import os.path
import fnmatch
from collections import MutableSequence
import yaml
from photo.idxitem import IdxItem
from photo.helper import tmpchdir


class Index(MutableSequence):

    defIdxFilename = ".index.yaml"

    def __init__(self, idxfile=None, imgdir=None, hashalg=['md5']):
        super(Index, self).__init__()
        self.directory = None
        self.idxfilename = None
        self.items = []
        if idxfile:
            self.read(idxfile)
        if imgdir:
            self.readdir(imgdir, hashalg)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __setitem__(self, index, value):
        self.items.__setitem__(index, value)

    def __delitem__(self, index):
        self.items.__delitem__(index)

    def insert(self, index, value):
        self.items.insert(index, value)

    def _idxfilename(self, idxfile):
        """Determine the index file name for reading and writing.
        """
        if idxfile is not None:
            idxfile = os.path.abspath(idxfile)
            if os.path.isdir(idxfile):
                idxfile = os.path.join(idxfile, self.defIdxFilename)
            return idxfile
        elif self.idxfilename is not None:
            return self.idxfilename
        else:
            d = self.directory if self.directory is not None else os.getcwd()
            return os.path.abspath(os.path.join(d, self.defIdxFilename))

    def readdir(self, imgdir, hashalg=['md5']):
        """Add all image files in a directory to the index.
        """
        imgdir = os.path.abspath(imgdir)
        if not self.directory:
            self.directory = imgdir
        known = { i.filename for i in self.items }
        with tmpchdir(self.directory):
            for f in sorted(os.listdir(imgdir)):
                f = os.path.relpath(os.path.join(imgdir, f))
                if (os.path.isfile(f) and fnmatch.fnmatch(f, '*.jpg') and
                    f not in known):
                    self.items.append(IdxItem(filename=f, hashalg=hashalg))

    def read(self, idxfile=None):
        """Read the index from a file.
        """
        self.idxfilename = self._idxfilename(idxfile)
        self.directory = os.path.dirname(self.idxfilename)
        with open(self.idxfilename, 'rt') as f:
            self.items = [IdxItem(data=i) for i in yaml.load(f)]

    def write(self, idxfile=None):
        """Write the index to a file.
        """
        with open(self._idxfilename(idxfile), 'wt') as f:
            items = [i.as_dict() for i in self.items]
            yaml.dump(items, f, default_flow_style=False)
