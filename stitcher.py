import os
import wave
import numpy as np
import wavio
#from pydub import AudioSegment
path = 'C:\\Users\\wattsij\\Documents\\audio_combiner\\audio1'
directory = os.fsencode(path)
files_to_combine = 37  # number of files to combine in one file
num_of_files = 37  # number of files in directory
s_p_f = 2880417         #(samples per file) 2880512 original ||||| 2880417 = cutting first 95 samples off
out = np.zeros((files_to_combine * s_p_f))
i = 0
k = 0
files_processed = 0
fade_length = 1000


def cross_fade(fade_array):

    fade_array = np.float64(fade_array)

    fade_in = np.linspace(0, 1, fade_length)
    fade_out = fade_in[:: -1]   # generates fade arrays

    beginning = fade_array[0:s_p_f]  # splitting file into three parts

    middles = fade_array[s_p_f: s_p_f * (files_to_combine - 1)]

    end = fade_array[((files_to_combine - 1) * s_p_f):(files_to_combine * s_p_f)]

    beginning[s_p_f - fade_length: s_p_f] *= fade_out  # applying fade_in/fade_out to sections

    end[0:fade_length] *= fade_in
    final = np.zeros(((files_to_combine * s_p_f) - ((files_to_combine - 1) * fade_length)), dtype=np.float64)

    for x in range(files_to_combine - 2):     #applies fade to middle files then adds to final
        array = middles[(x * s_p_f):((x+1) * s_p_f)]
        array[0: fade_length] *= fade_in
        array[s_p_f - fade_length: s_p_f] *= fade_out
        final[((x+1) * s_p_f):((x+2) * s_p_f)] += array

    final[0:s_p_f] += beginning

    final[((s_p_f * (files_to_combine - 1)) - ((files_to_combine - 1) * fade_length)):
          ((s_p_f * files_to_combine) - ((files_to_combine - 1) * fade_length))] += end  # adds last file to final

    #final = np.int16(final)  # converting to int16
    return final


for file in os.listdir(directory):
    filename = os.fsdecode(file)  # iterates through directory
    if filename.endswith(".wav"):

        path_file = path + '\\' + filename

        wav = wavio.read(path_file)  # READS RATE AND DATA ARRAY
        data = wav.data / 2**23
        rate = wav.rate
        sample_width = wav.sampwidth

        for j in range(95, s_p_f + 95):             # chops first 95 samples off each file
            out[(i * s_p_f) + (j - 95)] = data[j]
        i += 1
        files_processed += 1

        if ((i % files_to_combine) == 0) or (num_of_files == files_processed):
            out = cross_fade(out) 
            name = str("output" + str(k) + ".wav")
            wavio.write(name, out * 2 ** 23, rate, sampwidth=sample_width, scale='none')
            #wavfile = AudioSegment.from_wav(path + "\\" + name)
            #wavfile.export(path + "\\" + name, format="mp3")
            out = np.zeros((files_to_combine * s_p_f,))
            k += 1
            i = 0
