import os
import numpy as np
import matplotlib.pyplot as plt
from tool import fileTool as FT
from pathlib import Path


def generate_stats(f, type):

    for src in f:
        log_path = Path(src) / Path(f'{type}.log')
        read_stats_path = Path(src) / Path(f'{type}_read.stats')
        if os.path.exists(read_stats_path):
            return
        os.system(f'touch {read_stats_path}')
        write_stats_path = Path(src) / Path(f'{type}_write.stats')
        os.system(f'touch {write_stats_path}')

        log = open(log_path, 'r')
        read_stats = open(read_stats_path, 'w')
        write_stats = open(write_stats_path, 'w')
        A = []
        B = []

        for l in log.readlines():
            s = l.split(', ')
            if int(s[2]) == 0:
                A.append(int(s[1]))
            else:
                B.append(int(s[1]))

        A = np.sort(np.array(A))
        B = np.sort(np.array(B))

        # only read or write
        if A.shape[0] == 0:
            A = B.copy()
        if B.shape[0] == 0:
            B = A.copy()

        read_stats.write(f'min:{np.min(A)}\n')
        read_stats.write(f'max:{np.max(A)}\n')
        read_stats.write(f'avg:{np.mean(A)}\n')
        read_stats.write(f'std:{np.std(A)}\n')
        read_stats.write(f'sample:{A.shape[0]}\n')

        write_stats.write(f'min:{np.min(B)}\n')
        write_stats.write(f'max:{np.max(B)}\n')
        write_stats.write(f'avg:{np.mean(B)}\n')
        write_stats.write(f'std:{np.std(B)}\n')
        write_stats.write(f'sample:{B.shape[0]}\n')

        percentile_list = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 99.5, 99.9, 99.95, 99.99, 99.999, 99.9999, 100]
        for p in percentile_list:
            ia = int(0.01 * p * A.shape[0]) - 1
            ib = int(0.01 * p * B.shape[0]) - 1
            if ia >= 0 and ia < A.shape[0]:
                read_stats.write(f'{p}%:{A[ia]}\n')
            if ib >= 0 and ib < B.shape[0]:
                write_stats.write(f'{p}%:{B[ib]}\n')

        log.close()
        read_stats.close()
        write_stats.close()


def compute_solve1(f, type):

    read, write = np.zeros(25), np.zeros(25)

    for src in f:
        read_stats_path = Path(src) / Path(f'{type}_read.stats')
        write_stats_path = Path(src) / Path(f'{type}_write.stats')

        read_stats = open(read_stats_path, 'r')
        write_stats = open(write_stats_path, 'r')

        for i, l1, l2 in zip(range(25), read_stats.readlines(), write_stats.readlines()):
            s1 = l1.split(':')
            s2 = l2.split(':')
            read[i] += float(s1[1][:-1])
            write[i] += float(s2[1][:-1])

        read_stats.close()
        write_stats.close()

    read /= len(f)
    write /= len(f)

    return read, write


def compute_solve2(path, labels, data):

    os.system(f'touch {path}')
    file = open(path, 'w')
    for l, d in zip(labels, data):
        file.write(f'{l}:{d}\n')
    file.close()


def compute_avg_stats(f1, f2, f3, type):

    A_read, A_write = compute_solve1(f1, type)
    B_read, B_write = compute_solve1(f2, type)
    labels = ['min', 'max', 'avg', 'std', 'sample', '1%', '5%', '10%', '20%', '30%', '40%', '50%', '60%', '70%',
              '80%', '90%', '95%', '99%', '99.5%', '99.9%', '99.95%', '99.99%', '99.999%', '99.9999%', '100%']

    f1_read_path = f'{f3}/{type}_read_f1.stats'
    f1_write_path = f'{f3}/{type}_write_f1.stats'
    f2_read_path = f'{f3}/{type}_read_f2.stats'
    f2_write_path = f'{f3}/{type}_write_f2.stats'

    FT.mkPath(f3)
    compute_solve2(f1_read_path, labels, A_read)
    compute_solve2(f1_write_path, labels, A_write)
    compute_solve2(f2_read_path, labels, B_read)
    compute_solve2(f2_write_path, labels, B_write)


def plot(f, type, rw, normalize):

    stats1 = open(Path(f) / Path(f'{type}_{rw}_f1.stats'), 'r')
    stats2 = open(Path(f) / Path(f'{type}_{rw}_f2.stats'), 'r')

    labels = []
    A = []
    B = []
    for l1, l2 in zip(stats1.readlines(), stats2.readlines()):
        s1 = l1.split(':')
        s2 = l2.split(':')
        labels.append(s1[0])
        A.append(float(s1[1][:-1]))
        B.append(float(s2[1][:-1]))

    A = np.array(A)
    B = np.array(B)
    if normalize:
        B = np.around(100 * (B - A) / A, 2)
        B_labels = [f'{i}%' for i in B]

    y = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(1, 1, figsize=(10, 15))
    if normalize:
        rects = ax.barh(y - width / 2, B, width, label='normalize')
    else:
        rects1 = ax.barh(y - width / 2, A, width, label='baseline')
        rects2 = ax.barh(y + width / 2, B, width, label='other')

    ax.set_title(f'Compare {type}_{rw} stats info')
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.legend()

    if normalize:
        ax.bar_label(rects, B_labels, padding=10)
    else:
        ax.bar_label(rects1, padding=10)
        ax.bar_label(rects2, padding=10)

    plt.savefig(Path(f) / Path(f'{type}_{rw}.png'))
    plt.show()

    stats1.close()
    stats2.close()


def compare_data(f1, f2, f3, type):
    generate_stats(f1, type)
    generate_stats(f2, type)
    compute_avg_stats(f1, f2, f3, type)
    plot(f3, type, rw='read', normalize=True)
    plot(f3, type, rw='write', normalize=True)


def clear_data(f):
    cmd = f'sudo -S rm -rf {f}'
    os.system(cmd)


if __name__ == '__main__':
    f1 = ['data/USB_Netac_U185/ShortTerm/Step1_DeviceA_NoVibration_Run2']
    f2 = ['data/USB_Netac_U185/ShortTerm/Step1_DeviceA_NoVibration_Run3']
    f3 = 'data/result'
    compare_data(f1, f2, f3, type='fio_lat')
    compare_data(f1, f2, f3, type='fio_bw')