import random
import sys
import os
import numpy
from mingus.containers import *
import mingus.core.keys
import mingus.extra.lilypond as lilypond
from mingus.midi import midi_file_out
import mingus.core.progressions as progressions

from mingus.core import notes
def make_progression(base_chord, major):
    temp = notes.note_to_int(base_chord)
    base_chord = notes.int_to_note(temp, 'b')
    if (major):
        return progressions.to_chords(['I', 'V', 'VIm', 'IV'], base_chord)
    else:
        return progressions.to_chords(['Im', 'Vm', 'VI', 'IVm'], base_chord)
#function returns a (basic) chord progression for a given base chord
def alternative_progression(key,major):
    if major: #major
        first = notes.int_to_note((notes.note_to_int(key) + 9)%12)
        second = notes.int_to_note((notes.note_to_int(key) + 7)%12)
        third = notes.int_to_note((notes.note_to_int(key) + 5)%12)
        return [[key,True],[first, False], [second, True], [third, True]]
    else: #minor
        first = notes.int_to_note((notes.note_to_int(key) + 3)%12)
        second = notes.int_to_note((notes.note_to_int(key) + 7)%12)
        third = notes.int_to_note((notes.note_to_int(key) + 5)%12)
        return [[key,False],[first, True], [second, False], [third, False]]
#returns a list of alternate base chords in that key that go well with main progression

def create_random_track(key, happy,bars):
    temp = notes.note_to_int(key)
    key = notes.int_to_note(temp, 'b') #convert all accidentals to flats
    newTrack= Track()
    progressionChoice = alternative_progression(key, happy) #get an array of the possible progressions
    prevProg=False
    for i in range (0,bars):
        curBar = Bar(key, (4, 4))
        if (prevProg): #if it's not the first bar
            progIndex = prevProgInd + random.choice([1, -1])
            # make sure the current progression is next to the previous one
            if progIndex == -1:
                progIndex = 3
            elif progIndex == 4:
                progIndex = 0
        else:
            progIndex = random.choice(range(0, 4)) #the first progression is randmly chosen
        prevProg = True
        prevProgInd = progIndex
        useProgression = progressionChoice[progIndex]
        Progression = make_progression(useProgression[0], useProgression[1]) #get the progression
        prevChord = False
        while curBar.current_beat < 1:
            if (prevChord): #if it's not the first chord
                chordIndex = prevInd + random.choice([1, -1])
                # to make sure the current chord is next to the previous one in the progression
                if chordIndex == -1:
                    chordIndex = 3
                elif chordIndex == 4:
                    chordIndex = 0
            else:
                chordIndex = random.choice(range(0, 4)) #the first chord is a random chord from the progression
            prevChord = True
            curBar.place_notes(Progression[chordIndex], 4)
            prevInd = chordIndex
        newTrack + curBar #add bar to the track
    return newTrack
someTrack = create_random_track('C', True, 24)
print someTrack
print mingus.extra.lilypond.from_Track(someTrack)
mingus.midi.midi_file_out.write_Track("track.midi", someTrack) #create a midi file
