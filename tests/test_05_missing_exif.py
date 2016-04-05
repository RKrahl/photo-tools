"""Handle missing exif tags gracefully.  (Issue #15)

When creating a new index, the constructor of class IdxItem reads some
exif tags like DateTimeOriginal and Orientaion from the images to add
the information to the index.  But it should not raise an error if
some exif tags are missing.
"""

import shutil
import pytest
import photo.index
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_1190.jpg", "dsc_4623.jpg", "dsc_4664.jpg", 
    "dsc_4831.jpg", "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir

@pytest.mark.xfail(raises=KeyError, reason="Issue #15")
def test_create(imgdir):
    idx = photo.index.Index(imgdir=imgdir)
    idx.write()
