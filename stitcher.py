import os
import scipy.io.wavfile
import wave
import numpy as np

path = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\audio1'
directory = os.fsencode(path)
outfile = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\output.wav'
num_of_files = 20  # 3166
samples_per_file = 441249  # *3 = 882498 original is 441344 cutting first 95 samples off
out = np.zeros((3 * samples_per_file,), dtype=np.int16)
i = 0
k = 0
files_processed = 0


def cross_fade(fade_array):
    fade_array = np.float64(fade_array)
    fade_in = np.linspace(0, 1, 200)  # 200 samples long
    # fade_in = np.arange(0, 200)

    fade_out = fade_in[:: -1]

    beginning = fade_array[0:samples_per_file]  # splitting file into thirds
    middle = fade_array[samples_per_file: (2 * samples_per_file)]
    end = fade_array[(2 * samples_per_file):(3 * samples_per_file)]

    beginning[samples_per_file - 200: samples_per_file] *= fade_out  # applying fade_in/fade_out to sections
    middle[0:200] *= fade_in
    middle[samples_per_file - 200: samples_per_file] *= fade_out
    end[0:200] *= fade_in
    final = np.zeros((3 * samples_per_file - 400,), dtype=np.float64)

    final[0:samples_per_file] += beginning  # adding modified files together
    final[(samples_per_file - 200):(samples_per_file * 2 - 200)] += middle
    final[(samples_per_file * 2 - 400):(samples_per_file * 3 - 400)] += end

    final = np.int16(final)  # converting to int16
    return final


for file in os.listdir(directory):
    filename = os.fsdecode(file)  # iterates through directory
    if filename.endswith(".wav"):

        path_file = path + '\\' + filename
        rate, data = scipy.io.wavfile.read(path_file)  # READS RATE AND DATA ARRAY
        for j in range(95, samples_per_file + 95):
            out[(i * samples_per_file) + (j - 95)] = data[j]
        i += 1
        files_processed += 1

        if ((i % 3) == 0) or (num_of_files == files_processed):
            out = cross_fade(out)
            scipy.io.wavfile.write("output" + str(k) + ".wav", rate, out)
            out = np.zeros((3 * samples_per_file,), dtype=np.int16)
            k += 1
            i = 0
