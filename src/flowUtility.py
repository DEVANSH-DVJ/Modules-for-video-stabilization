import numpy as np

TAG_FLOAT = 202021.25
TAG_STRING = 'PIEH'


def readFlow(path):
    with open(path, 'rb') as f:
        tag = float(np.fromfile(f, np.float32, count=1)[0])
        assert(tag == TAG_FLOAT)
        w = np.fromfile(f, np.int32, count=1)[0]
        h = np.fromfile(f, np.int32, count=1)[0]

        flow = np.fromfile(f, np.float32, count=h * w * 2)
        flow.resize((h, w, 2))

    return flow


def writeFlow(flow, filename):

    # assert type(filename) is str, "file is not str %r" % str(filename)
    # assert filename[-4:] == '.flo', "file ending is not .flo %r" % file[-4:]

    height, width, nBands = flow.shape
    assert nBands == 2, "Number of bands = %r != 2" % nBands
    u = flow[:, :, 0]
    v = flow[:, :, 1]
    assert u.shape == v.shape, "Invalid flow shape"
    height, width = u.shape

    f = open(filename, 'wb')
    f.write(bytes(TAG_STRING, 'utf-8'))
    np.array(width).astype(np.int32).tofile(f)
    np.array(height).astype(np.int32).tofile(f)
    tmp = np.zeros((height, width*nBands))
    tmp[:, np.arange(width)*2] = u
    tmp[:, np.arange(width)*2 + 1] = v
    tmp.astype(np.float32).tofile(f)

    f.close()
