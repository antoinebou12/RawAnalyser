# RawAnalyser
## Simple RawAnalyser for black and white clipping, gamma calculation, flatness with vignette (algolux)
### Requirement libary
    -Python 2.7
    -json
    -getopt
    -time
    -numpy
    -scipy
    -pyqt5
    -watchdog
    -logging
	
### Run the program 
	python RawAnalyser.py -h
	python RawAnalyser.py -f <pathfolder> -p <pointfile>
	python GUI.py

### RawAnalyser.py
Simple RawAnalyser for testing black and white level of clipping in a raw image.Need to add a path to the folder to check 
and a json file with the region interest.
#### points.json
 	{
 	"last_y": 1088,
	"last_x": 1928,
 	"first_x": 0,
 	"first_y": 0
  	}
### GUI.py
Image selection GUI for the region of interest in a raw or tiff file save in a json file.
Check for new file in the raw folder

	-Camera: OV2740
	-Resolution: (1088, 1928)
	-ImageType.BINARY16U
	-Sensor value: 10 bit
	-Bayer pattern: 'bggr'
