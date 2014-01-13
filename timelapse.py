# timelapseish effect for audio files
#
# Copyright (c) 2013 Olli Erik Keskinen
# All rights reserved.

# This code is released under The BSD 2-Clause License.
# See the file LICENSE.txt for information.

import numpy as np
import progtimer
from scipy.io import wavfile


def timelapse(input_signal, ratio, window_size, overlap=4):
    hop_in = window_size/overlap
    hop_out = hop_in/ratio

    #print "Ratio: ", float(Hin)/float(Hout), " Hout:", Hout

    # pre- and postpad
    padding = window_size - hop_in
    signal_in = np.zeros(len(input_signal) + 2*padding)
    signal_in[padding : len(input_signal)+padding] = input_signal

    length = len(signal_in)
    window = np.hanning(window_size)

    signal_out = np.zeros(length/ratio + window_size)

    unit_angle = np.ones(window_size, dtype='complex')
    non_zero = np.ones(window_size) * 1e-15

    pt = progtimer.ProgTimer()

    p_in = 0
    p_out = 0
    while p_in < length - (window_size + hop_out):

        p1_int = int(p_in)
        spectrum_last = np.fft.fft(window * signal_in[p1_int : p1_int+window_size])
        magnitude_last = np.abs(spectrum_last)

        p2_int = int(p_in + hop_out)
        spectrum = np.fft.fft(window * signal_in[p2_int : p2_int+window_size])
        magnitude = np.abs(spectrum)

        unit_angle *= (spectrum * magnitude_last) / (magnitude * spectrum_last + non_zero)

        p_out_int = int(p_out)

        signal_out[p_out_int : p_out_int + window_size] += window * np.fft.ifft(unit_angle*magnitude).real
        p_out += hop_out
        p_in += hop_in

        pt.tick(p_in, length)

    return signal_out[0:p_out-hop_out]

def main():
    window_size = 16384
    condensation_ratio = 10
    overlap = 8

    filename = "lafille"

    (sampling_rate, signal_in) = wavfile.read(filename+".wav")
    #signal_in = np.append(np.zeros(window_size/2), signal_in)
    signal_out = timelapse(signal_in, condensation_ratio, window_size, overlap=overlap)
    signal_out = np.nan_to_num(signal_out)
    signal_out -= np.mean(signal_out) # account for dc offset
    signal_out *= 2**14 / np.amax(signal_out)
    signal_out = np.array(signal_out, dtype="int16")

    wavfile.write(filename+"_timelapse.wav", sampling_rate, signal_out)

    print("Done.")

main()