
import os
import scipy.io.wavfile
import wave
import numpy as np

path = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\audio1'
directory = os.fsencode(path)
outfile = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\output.wav'
num_of_files = 20                       #3166
samples_per_file = 441344
out = np.zeros((3 * samples_per_file,), dtype=np.int16)
i = 0
k = 0
files_processed = 0
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".wav"):


        path_file = path + '\\' + filename                  #
        rate, data = scipy.io.wavfile.read(path_file)       #READS RATE AND DATA ARRAY
        for j in range(samples_per_file):
            out[(i * samples_per_file) + j] = data[j]
        i += 1
        files_processed += 1

        if (((i % 3) == 0) or (num_of_files == files_processed)):
            scipy.io.wavfile.write("output" + str(k) + ".wav", rate, out)
            out = np.zeros((3 * samples_per_file,), dtype=np.int16)
            k += 1
            i = 0
