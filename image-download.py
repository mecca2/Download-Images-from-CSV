#!/usr/bin/env python

# Usage: 
    # Command to run: py image-download.py {arg1} {arg2} {arg3}
        # arg1 : specifies name of the csv file to use for data. If not set uses images.csv 
        # arg2 : specifies name of directory to download images. If not specified downloads to images directory. 
        # arg3 : specifies url to get images from. If used all culumns besides first column in csv can contain images.
    # example command :: py image-download.py Sample2.csv test-100 http://google.com
# CSV Format: 
## Columns: 
    # 1) Name of item
    # 2) Url to file 
    # 3) Name of image file with file extension 
import os
import sys
import urllib
import urllib.request
#import HTTPError
#import urllib2
importlogPass = ""; 
importlogFail = ""; 
downloadedImages = []
failedImages = []
def writeLogs():
    global importlogPass 
    global importlogFail
    with open("log/failed_downloads.txt", "w") as text_file:
        print(importlogFail, file=text_file)
    with open("log/passed_downloads.txt", "w") as text_file:
        print(importlogPass, file=text_file)

def imageUploader(name, imageName, directory, url, row):
    global importlogPass 
    global importlogFail
    global downloadedImages
    global failedImages
    imageName = imageName.replace("\n","")
    fullfilename = os.path.join(directory, imageName)
    #print(url)
    imageIndex  = downloadedImages.index(imageName) if imageName in downloadedImages else -1
    image2Index  = failedImages.index(imageName) if imageName in failedImages else -1
    if imageIndex == -1 and image2Index == -1:
        try: 
            resp = urllib.request.urlopen(url)
            urllib.request.urlretrieve(url, fullfilename)
            #print(resp.code)
        except urllib.request.HTTPError:
            importlogFail += str(row) + " \t" + name + "\t" + imageName + "\n"
            print("** FAILED -- Row: " + str(row) + " Sku: " + name + " Image: " + imageName)
            failedImages.append(imageName)
        else: 
            #print('sucess')
            importlogPass += str(row) + " \t" + name + "\t" + imageName + "\n"
            print("Passed -- Row: " + str(row) + " Sku: " + name + " Image: " + imageName )
            downloadedImages.append(imageName)
    else:
        if imageIndex > 0: 
            importlogPass += str(row) + " \t" + name + "\t" + imageName + "\n"
            print("Passed (image already uploaded) -- Row: " + str(row) + " Sku: " + name + " Image: " + imageName )
        if image2Index > 0: 
            importlogFail += str(row) + " \t" + name + "\t" + imageName + "\n"
            print("** FAILED (image already failed) -- Row: " + str(row) + " Sku: " + name + " Image: " + imageName)
    writeLogs()

def main():
    global importlogPass 
    global importlogFail
    filename = "images.csv"
    uploadPath = "images"
    baseurl = ""

    if len(sys.argv) > 1 :
        if sys.argv[1] != "":
            filename = sys.argv[1]
    if len(sys.argv) > 2 :
        if sys.argv[2] != "":
            uploadPath = sys.argv[2]
    if len(sys.argv) > 3 :
        if sys.argv[3] != "":
            baseurl = sys.argv[3]



    if not os.path.exists(uploadPath):
        os.makedirs(uploadPath)
    if not os.path.exists("log"):
        os.makedirs("log")


    # open file to read
    with open("{0}".format(filename), 'r') as csvfile:
        # iterate on all lines
        i = 0

        for line in csvfile:
            # check if we have an image URL
            if i != 0:
                splitted_line = line.split(',')

                if baseurl == "":
                    if splitted_line[1] != '' and splitted_line[1] != "\n":
                        imageUploader(splitted_line[0], splitted_line[2],uploadPath,splitted_line[1], i)
                    else:
                        print("No result for {0}".format(splitted_line[0]))
                    #imageName = splitted_line[2].replace("\n","")
                    #fullfilename = os.path.join(uploadPath, imageName)
                    #urllib.request.urlretrieve(splitted_line[1], fullfilename)
                else:
                    x = 0 
                    for item in splitted_line: 
                        if x != 0:
                            if item != '' and item != '\n':
                                #print(baseurl + '/' + item)
                                if item.startswith(" "):
                                    item = item[1:]
                                imageUploader(splitted_line[0], item, uploadPath, baseurl + '/' + item.replace(" ","%20"), i)
                        x += 1
                #print ("Image {0} saved for {1}".format(imageName, splitted_line[0]))
                
            i += 1

main()