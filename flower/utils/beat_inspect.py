from __future__ import absolute_import

import shelve
import shutil


def inspect_beat(beat_file):
    shutil.copyfile(beat_file, beat_file+".backup")
    sf = shelve.open(beat_file + ".backup")
    entries = sf['entries']
    detailed_entires = []
    for name, entry in entries.iteritems():
        detailed_entires.append(entry.__dict__)
    sf.close()
    return detailed_entires
        

def inspect_all_beats(beat_file_list):
    all_schedules = []
    for beat_file in beat_file_list:
        all_schedules +=  inspect_beat(beat_file)
    return all_schedules
