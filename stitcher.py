import os
import wave
import numpy as np
import wavio
path = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\audio'
directory = os.fsencode(path)
files_to_combine = 9
num_of_files = 9  # 3166
s_p_f = 2880417  # 2880512 original ||||| 2880417 = cutting first 95 samples off
out = np.zeros((files_to_combine * s_p_f))
i = 0
k = 0
files_processed = 0
fade_length = 1500


def cross_fade(fade_array):

    fade_array = np.float64(fade_array)

    fade_in = np.linspace(0, 1, fade_length)
    fade_out = fade_in[:: -1]

    beginning = fade_array[0:s_p_f]  # splitting file into three parts

    middles = fade_array[s_p_f : s_p_f * (files_to_combine - 1)]


    end = fade_array[((files_to_combine - 1) * s_p_f):(files_to_combine * s_p_f)]


    beginning[s_p_f - fade_length: s_p_f] *= fade_out  # applying fade_in/fade_out to sections

    end[0:fade_length] *= fade_in
    final = np.zeros(((files_to_combine * s_p_f) - ((files_to_combine - 1) * fade_length)), dtype=np.float64)

    for x in range(files_to_combine - 2):                   #applies fade then adds to final
        array = middles[(x * s_p_f):((x+1) * s_p_f)]
        array[0: fade_length] *= fade_in
        array[s_p_f - fade_length: s_p_f] *= fade_out
        final[((x+1) * s_p_f):((x+2) * s_p_f)] += array

    final[0:s_p_f] += beginning  # adding modified files together

    final[((s_p_f * (files_to_combine - 1)) - ((files_to_combine - 1) * fade_length)):
          ((s_p_f * files_to_combine) - ((files_to_combine - 1) * fade_length))] += end

        #final = np.int16(final)  # converting to int16
    return final


for file in os.listdir(directory):
    filename = os.fsdecode(file)  # iterates through directory((x+1) * s_p_f)
    if filename.endswith(".wav"):

        path_file = path + '\\' + filename

        wav = wavio.read(path_file)  # READS RATE AND DATA ARRAY
        data = wav.data / 2**23
        rate = wav.rate
        sample_width = wav.sampwidth

        for j in range(95, s_p_f + 95):
            out[(i * s_p_f) + (j - 95)] = data[j]
        i += 1
        files_processed += 1

        if ((i % files_to_combine) == 0) or (num_of_files == files_processed):
            out = cross_fade(out)
            wavio.write("output" + str(k) + ".wav", out * 2 ** 23, rate, sampwidth=sample_width, scale='none')
            out = np.zeros((files_to_combine * s_p_f,))
            k += 1
            i = 0
