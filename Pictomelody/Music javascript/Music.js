var fs = require('fs');
var midiConverter = require('midi-converter');
var midiSong = fs.readFileSync('C:/Users/Akriti/Documents/GitHub/createRandomTrack/Pictomelody/track.midi', 'binary');
var jsonSong = midiConverter.midiToJson(midiSong);
fs.writeFileSync('example.json', JSON.stringify(jsonSong));