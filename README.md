# Download Images from CSV 

Script is used to download images from a CSV and save to local directory. 

## Usage 
- Command to run: py image-download.py {arg1} {arg2} {arg3}
	- arg1 : specifies name of the csv file to use for data. If not set uses images.csv 
	- arg2 : specifies name of directory to download images. If not specified downloads to images directory. 
	- arg3 : specifies url to get images from. If used all culumns besides first column in csv can contain images.
- example command :: py image-download.py Sample2.csv test-100 http://google.com
- CSV can have 2 formats depending on usage 
	1) Single Image per row 
		- File will need 3 columns 
			1) Name of thing to download 
			2) url to image 
			3) file name for image when uploaded to local machine
	2) Multiple images per row 
		- File can have 2 or more columns 
			1) Name of thing to download 
			2) All columns can have an image name or blank. Program will load all images in row. 
				- Require arg3 set in the command line for this to know where to download images from. 