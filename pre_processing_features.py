import numpy as np
import scipy.signal
import csv
import matplotlib.pyplot as pp
import scipy.io

# given ppg input, minimum distance between peaks, writes the extracted features to filepath
def pre_process_input(ppg, distance, filepath):

    peaks = scipy.signal.find_peaks(ppg, distance= distance)[0]
    valleys = scipy.signal.find_peaks(-1 * ppg, distance= distance)[0]

    if peaks[0] < valleys[0]:
        peaks = peaks[1:]

    valleys = find_valleys(peaks, valleys, True).astype(int)
    print(peaks, valleys)
    ppg_info = []
    i = 0

    while i < len(peaks) - 2:

        cardiac_period = peaks[i + 1] - peaks[i]
        SUT = peaks[i] - valleys[i]
        DT = valleys[i + 1] - peaks[i]

        first_half = ppg[valleys[i]:peaks[i]]
        second_half = ppg[peaks[i]:valleys[i + 1]]

        if len(first_half) != 0 and len(second_half) != 0:
            height = ppg[peaks[i]] - ppg[valleys[i]]
            height50 = (0.50 * height) + ppg[valleys[i]]
            height25 = (0.25 * height) + ppg[valleys[i]]
            height75 = (0.75 * height) + ppg[valleys[i]]
            height33 = (0.33 * height) + ppg[valleys[i]]
            height66 = (0.66 * height) + ppg[valleys[i]]
            height10 = (0.10 * height) + ppg[valleys[i]]

            first_index_50 = np.argmin(abs(first_half - height50)) + valleys[i]
            second_index_50 = np.argmin(abs(second_half - height50)) + peaks[i]

            first_index_25 = np.argmin(abs(first_half - height25)) + valleys[i]
            second_index_25 = np.argmin(abs(second_half - height25)) + peaks[i]

            first_index_75 = np.argmin(abs(first_half - height75)) + valleys[i]
            second_index_75 = np.argmin(abs(second_half - height75)) + peaks[i]

            first_index_33 = np.argmin(abs(first_half - height33)) + valleys[i]
            second_index_33 = np.argmin(abs(second_half - height33)) + peaks[i]

            first_index_66 = np.argmin(abs(first_half - height66)) + valleys[i]
            second_index_66 = np.argmin(abs(second_half - height66)) + peaks[i]

            first_index_10 = np.argmin(abs(first_half - height10)) + valleys[i]
            second_index_10 = np.argmin(abs(second_half - height10)) + peaks[i]

            SW_10 = peaks[i] - first_index_10
            DW_10 = second_index_10 - peaks[i] + 0.001

            SW_25 = peaks[i] - first_index_25
            DW_25 = second_index_25 - peaks[i] + 0.001

            SW_33 = peaks[i] - first_index_33
            DW_33 = second_index_33 - peaks[i] + 0.001

            SW_50 = peaks[i] - first_index_50
            DW_50 = second_index_50 - peaks[i] + 0.001

            SW_66 = peaks[i] - first_index_66
            DW_66 = second_index_66 - peaks[i] + 0.001

            SW_75 = peaks[i] - first_index_75
            DW_75 = second_index_75 - peaks[i] + 0.001

            ppg_info.append([cardiac_period, SUT, DT, DW_10, DW_25, DW_33, DW_50, DW_66,
                     DW_75, SW_10 + DW_10, SW_10/DW_10, SW_25 + DW_25, SW_25/DW_25, SW_33 + DW_33, SW_10/DW_33,
                     SW_50 + DW_50, SW_50 / DW_50, SW_66 + DW_66, SW_66 / DW_66,SW_75 + DW_75, SW_75 / DW_75])
        i = i + 1

    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(ppg_info)

    return np.array(ppg_info)

# analyze windows to find peaks
def find_peaks(signal):
    peaks = scipy.signal.find_peaks(signal[:1000], distance=70)[0]
    period = peaks[2] - peaks[1]
    length = len(signal)
    windows_num = int(length / period)
    min_indices = []
    max_indices = []
    for n in range(windows_num):
        if n == 0:
            window = signal[0: period + 5]
            min_index = np.argmin(window)
            max_index = np.argmax(window)
        else:
            window = signal[n * period - 5: n * period + 5]
            min_index = np.argmin(window) + n * period - 5
            max_index = np.argmax(window) + n * period - 5
        max_indices.append(max_index)
        min_indices.append(min_index)

    return np.array(max_indices), np.array(min_indices)

# in cases where the bp and ppg are not aligned, shifts them so that they match
def align_signals(bp_peaks, ppg_peaks):

    if len(bp_peaks) < len(ppg_peaks):
        diff = ppg_peaks[0:len(bp_peaks)] - bp_peaks
        # print("diff", diff)
    if len(bp_peaks) > len(ppg_peaks):
        diff = ppg_peaks - bp_peaks[0:len(ppg_peaks)]
        # print("diff", diff)
    if len(bp_peaks) == len(ppg_peaks):
        diff = ppg_peaks - bp_peaks
        # print("diff", diff)

    ppg_peaks_fixed = np.array([])
    bp_peaks_fixed = np.array([])
    ppg_ind = 0
    bp_ind = 0
    for i in range(len(diff) - 1):
        if ppg_ind < len(ppg_peaks) and bp_ind < len(bp_peaks):
            ppg_peaks_fixed = np.append(ppg_peaks_fixed, ppg_peaks[ppg_ind])
            bp_peaks_fixed = np.append(bp_peaks_fixed, bp_peaks[bp_ind])
        if diff[i + 1] > diff[i] + 50:
            bp_ind += 2
            ppg_ind += 1
        if diff[i + 1] < diff[i] - 50:
            ppg_ind += 2
            bp_ind += 1
        if diff[i + 1] < diff[i] + 50 and diff[i + 1] > diff[i] - 50:
            ppg_ind += 1
            bp_ind += 1

    return ppg_peaks_fixed, bp_peaks_fixed


def align_multiple_times(bp_peaks, ppg_peaks, n):
    bp_fixed = bp_peaks
    ppg_fixed = ppg_peaks
    for i in range(n):
        bp_fixed, ppg_fixed = align_signals(bp_fixed, ppg_fixed)
    return ppg_fixed, bp_fixed

# finds valleys corresponding with each peak
def find_valleys(signal_peaks, signal_valleys, isPPG):
    valleys_fixed = np.array([])
    if isPPG:
        valleys_fixed = np.append(valleys_fixed, signal_valleys[0])
    for i in range(len(signal_peaks)):
        # if signal_valleys[np.argmax(signal_valleys > signal_peaks[i])] not in valleys_fixed:
        valleys_fixed = np.append(valleys_fixed, signal_valleys[np.argmax(signal_valleys > signal_peaks[i])])
        # else:
        #     valleys_fixed = np.append(valleys_fixed, signal_valleys[np.argmax(signal_valleys > valleys_fixed)])
        # else:
        #     valleys_fixed = np.append(valleys_fixed, np.max(valleys_fixed)+ 70)
    return valleys_fixed

# the peaks which are not aligned well are removed from both bp and ppg
def remove_noise(bp_peaks, ppg_peaks):
    difference = ppg_peaks - bp_peaks
    offset = np.mean(difference[:3])
    ppg_peaks = ppg_peaks[np.where((difference < offset + 20) & (difference > offset - 20))]
    bp_peaks = bp_peaks[np.where((difference < offset + 20) & (difference > offset - 20))]
    return ppg_peaks, bp_peaks


# reads data and extract bp and ppg features and writes to two separate files
def pre_process_mat_files(input_path):
    part1 = scipy.io.loadmat(input_path)
    part1_data = part1['p'][0]

    part1_size = len(part1_data)
    print(part1_size)

    checked = []
    number_of_pulses = 0

    for record in range(part1_size):
        bp = part1_data[record][1]
        bp_peaks = scipy.signal.find_peaks(bp, distance=70)[0]
        bp_valleys = scipy.signal.find_peaks(-1 * bp, distance=70)[0]

        ppg = part1_data[record][0]
        ppg_peaks = scipy.signal.find_peaks(ppg, distance=70)[0]
        ppg_valleys = scipy.signal.find_peaks(-1 * ppg, distance=70)[0]

        if ppg_peaks[0] < ppg_valleys[0]:
            ppg_peaks = ppg_peaks[1:]
            if bp_valleys[0] < bp_peaks[0]:
                bp_valleys = bp_valleys[1:]
            bp_peaks = bp_peaks[1:]


        ppg_peaks_fixed, bp_peaks_fixed = align_signals(bp_peaks, ppg_peaks)
        ppg_peaks_fixed, bp_peaks_fixed = remove_noise(bp_peaks_fixed, ppg_peaks_fixed)

        ppg_valleys_fixed = find_valleys(ppg_peaks_fixed, ppg_valleys, True)
        bp_valleys_fixed = find_valleys(bp_peaks_fixed, bp_valleys, False)

        checked.append(record)

        bp_valleys_fixed = bp_valleys_fixed.astype(int)
        bp_peaks_fixed = bp_peaks_fixed.astype(int)
        ppg_peaks_fixed = ppg_peaks_fixed.astype(int)
        ppg_valleys_fixed = ppg_valleys_fixed.astype(int)

        ppg_diff = ppg_valleys_fixed[1:] - ppg_peaks_fixed
        if ppg_diff != []:
            if ppg_diff[-1] < 0:
                ppg_peaks_fixed = ppg_peaks_fixed[:-1]
                ppg_valleys_fixed = ppg_valleys_fixed[:-1]

        bp_info = []
        ppg_info = []
        i = 0
        while i < len(ppg_peaks_fixed) - 1:

            if i == len(bp_valleys_fixed) - 1:
                break
            if i == len(bp_peaks_fixed) - 1:
                break
            diastolic = bp[bp_valleys_fixed[i]]
            systolic = bp[bp_peaks_fixed[i]]

            cardiac_period = ppg_peaks_fixed[i + 1] - ppg_peaks_fixed[i]
            SUT = ppg_peaks_fixed[i] - ppg_valleys_fixed[i]
            DT = ppg_valleys_fixed[i + 1] - ppg_peaks_fixed[i]

            first_half = ppg[ppg_valleys_fixed[i]:ppg_peaks_fixed[i]]
            second_half = ppg[ppg_peaks_fixed[i]:ppg_valleys_fixed[i + 1]]
            if len(first_half) != 0 and len(second_half) != 0:
                # print(len(ppg_peaks_fixed), len(ppg_valleys_fixed), i)
                height = ppg[ppg_peaks_fixed[i]] - ppg[ppg_valleys_fixed[i]]
                height50 = (0.50 * height) + ppg[ppg_valleys_fixed[i]]
                height25 = (0.25 * height) + ppg[ppg_valleys_fixed[i]]
                height75 = (0.75 * height) + ppg[ppg_valleys_fixed[i]]
                height33 = (0.33 * height) + ppg[ppg_valleys_fixed[i]]
                height66 = (0.66 * height) + ppg[ppg_valleys_fixed[i]]
                height10 = (0.10 * height) + ppg[ppg_valleys_fixed[i]]

                first_index_50 = np.argmin(abs(first_half - height50)) + ppg_valleys_fixed[i]
                second_index_50 = np.argmin(abs(second_half - height50)) + ppg_peaks_fixed[i]

                first_index_25 = np.argmin(abs(first_half - height25)) + ppg_valleys_fixed[i]
                second_index_25 = np.argmin(abs(second_half - height25)) + ppg_peaks_fixed[i]

                first_index_75 = np.argmin(abs(first_half - height75)) + ppg_valleys_fixed[i]
                second_index_75 = np.argmin(abs(second_half - height75)) + ppg_peaks_fixed[i]

                first_index_33 = np.argmin(abs(first_half - height33)) + ppg_valleys_fixed[i]
                second_index_33 = np.argmin(abs(second_half - height33)) + ppg_peaks_fixed[i]

                first_index_66 = np.argmin(abs(first_half - height66)) + ppg_valleys_fixed[i]
                second_index_66 = np.argmin(abs(second_half - height66)) + ppg_peaks_fixed[i]

                first_index_10 = np.argmin(abs(first_half - height10)) + ppg_valleys_fixed[i]
                second_index_10 = np.argmin(abs(second_half - height10)) + ppg_peaks_fixed[i]

                SW_10 = ppg_peaks_fixed[i] - first_index_10
                DW_10 = second_index_10 - ppg_peaks_fixed[i] + 0.001

                SW_25 = ppg_peaks_fixed[i] - first_index_25
                DW_25 = second_index_25 - ppg_peaks_fixed[i] + 0.001

                SW_33 = ppg_peaks_fixed[i] - first_index_33
                DW_33 = second_index_33 - ppg_peaks_fixed[i] + 0.001

                SW_50 = ppg_peaks_fixed[i] - first_index_50
                DW_50 = second_index_50 - ppg_peaks_fixed[i] + 0.001

                SW_66 = ppg_peaks_fixed[i] - first_index_66
                DW_66 = second_index_66 - ppg_peaks_fixed[i] + 0.001

                SW_75 = ppg_peaks_fixed[i] - first_index_75
                DW_75 = second_index_75 - ppg_peaks_fixed[i] + 0.001

                if 40 < diastolic < 85 and 75 < systolic < 165:
                    ppg_info.append(
                        [cardiac_period, SUT, DT, DW_10, DW_25, DW_33, DW_50, DW_66,
                         DW_75, SW_10 + DW_10, SW_10/DW_10, SW_25 + DW_25, SW_25/DW_25, SW_33 + DW_33, SW_10/DW_33,
                         SW_50 + DW_50, SW_50 / DW_50, SW_66 + DW_66, SW_66 / DW_66,SW_75 + DW_75, SW_75 / DW_75])
                    bp_info.append([diastolic, systolic])
            i = i + 1

        print(bp_info)
        print(ppg_info)
        number_of_pulses += len(ppg_info)

        with open('part2_ppg.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(ppg_info)

        with open('part2_bp.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(bp_info)

    print("number of pulses: ", number_of_pulses)



