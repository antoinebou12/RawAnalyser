# RawAnalyser
## Simple RawAnalyser for black and white clipping, gamma calculation, flatness with vignette (algolux)
### Requirement libary
    -Python 2.7
    -json
    -time
    -numpy
    -scipy
    -pyqt5
    -argparse
    -argcomplete
    -watchdog
    -logging
    -colorama
    -plotly
    -matplotlib
	
### Run the program 
	python RawAnalyser.py <pathfolder> <pointfile> --func <clipping,gamma,vignette,histogram,noHist,basic, default all> --bl <black level,default 1024> --vignette<pathvignette>
	python GUI.py
	python RawPixel.pt input<file> x y  --bitdepth <8,10,16,default 16>
	

### RawAnalyser.py
Simple RawAnalyser for testing black and white level of clipping in a raw image. Need to add a path to the folder to check 
and a json file with the region interest and for the gray patches.
#### points.json
	{
	"last_y": 798,
	"last_x": 1353,
	"gray_first_y": 691,
	"gray_first_x": 606,
	"first_x": 603,
	"first_y": 315,
	"gray_last_x": 1347,
	"gray_last_y": 795
	}
### GUI.py
Image selection GUI for the region of interest and for the gray patches in a raw or tiff file save in a json file.
Check for new file in the raw folder
### RawPixel.py
Check for the value of the pixel and the color with the bayer pattern
### 20MPto5MP.py
Converstion of the 20megapixel to 5megapixel pixel image for the new sensor
OV20880 = Camera('OV20880', ImageType.BINARY16U, shape=(3904, 5184), depth=2 ** 10 - 1, bayer='bbggbbggbbggbbggggrrggrrggrrggrr')
#### Camera
	Camera: OV2740
	Resolution: (1088, 1928)
	ImageType.BINARY16U
	Sensor value: 10 bit
	Bayer pattern: 'bggr'
