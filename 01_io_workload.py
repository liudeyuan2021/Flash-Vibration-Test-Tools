import os
from tool import fileTool as FT


def io_workload(dst):
    FT.mkPath(dst)
    print(f'cd /home/liudeyuan/Desktop/vibration/{dst}')

    filename = '/dev/sdb'
    rw = 'randread'
    size = '100%'
    numjobs = 1
    loops = 10
    runtime = '3h'

    cmd = f'sudo -S filename={filename} rw={rw} size={size} numjobs={numjobs} loops={loops} runtime={runtime} fio --output=fio_stats.log /home/liudeyuan/Desktop/vibration/01_io_workload < /home/liudeyuan/Desktop/vibration/password'
    print(cmd)


if __name__ == '__main__':
    type = 'USB_Netac_U185/ShortTerm'
    step = 'Step1'
    device = 'DeviceA'
    vibration = 'NoVibration'
    run = 'Run3'
    dst = f'data/{type}/{step}_{device}_{vibration}_{run}'
    io_workload(dst)