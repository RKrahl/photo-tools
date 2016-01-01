#! /usr/bin/python

import sys
import argparse
from PySide import QtGui
import photo.index
import photo.idxfilter
from photo.qt import ImageViewer


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', help="image directory", default=".")
argparser.add_argument('--scale', help="scale factor", default=(625.0/4096.0))
photo.idxfilter.addFilterArguments(argparser)
args = argparser.parse_args()

app = QtGui.QApplication([])
idx = photo.index.Index(idxfile=args.directory)
idxfilter = photo.idxfilter.IdxFilter(args)
imageViewer = ImageViewer(idx, idxfilter, args.scale)
sys.exit(app.exec_())