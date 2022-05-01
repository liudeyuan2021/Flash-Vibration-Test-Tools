import os

def get_rw(src):
    x, total = 0, 0
    f = open(src, 'r')
    for l in f.readlines():
        n = int(l.split(', ')[2])
        x += (n == 1)
        total += 1
    print(float(x) / total)

if __name__ == '__main__':
    get_rw('/home/liudeyuan/Desktop/VendorC/ShortTerm/VerticalVibration/Run2_VerticalVibration/fio_iops.log')