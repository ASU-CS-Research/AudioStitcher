import os
import scipy.io.wavfile
import wave
import numpy as np

path = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\audio1'
directory = os.fsencode(path)
outfile = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\output.wav'
num_of_files = 20  # 3166
samples_per_file = 441344
out = np.zeros((3 * samples_per_file,), dtype=np.int16)
i = 0
k = 0
files_processed = 0


def cross_fade(fade_array):
    fade_in = np.arange(.00333, 1, .00133)  # 300 samples long
    fade_in = np.hstack((fade_in, np.ones(samples_per_file - fade_in.size)))
    fade_out = fade_in[:: -1]
    beginning = fade_array[0:samples_per_file]
    middle = fade_array[samples_per_file: (2 * samples_per_file)]
    end = fade_array[(2 * samples_per_file):(3 * samples_per_file)]

    beginning = beginning * fade_out
    middle = (middle * fade_out) * fade_in
    end = end * fade_in
    final = np.hstack((beginning, middle, end))
    final = np.int16(final)
    return final


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".wav"):

        path_file = path + '\\' + filename
        rate, data = scipy.io.wavfile.read(path_file)  # READS RATE AND DATA ARRAY
        for j in range(samples_per_file):
            out[(i * samples_per_file) + j] = data[j]
        i += 1
        files_processed += 1

        if ((i % 3) == 0) or (num_of_files == files_processed):
            out = cross_fade(out)
            scipy.io.wavfile.write("output" + str(k) + ".wav", rate, out)
            out = np.zeros((3 * samples_per_file,), dtype=np.int16)
            k += 1
            i = 0
