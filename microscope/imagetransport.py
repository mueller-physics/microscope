#!/usr/bin/python
# -*- coding: utf-8
#
# Copyright 2017 Marcel Mueller (muellerphysics@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
import struct
import numpy
from time import sleep

class ImageSender:

    """Minimalistic class to interface with the Java ImageReceiver code"""

    def __init__(self, imgSize=512):
	self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	self.sendCount = 0   
	self.imgSize = imgSize
 
    def connect( self, hostname="localhost", port=32320 ):
	self.sock.connect( ( hostname, 32320 ))

    def disconnect( self ):
        self.sock.close()
 
    def sendImage( self, data ):
    
        self.sendCount+=1
        width  = data.shape[0]
        height = data.shape[1]

        nrPixels = width*height  # width * height, basically
        dataLen = nrPixels * 2          # size at 2 bytes per pxl
    
        header = struct.pack(
            "QIIBB8s6xhh128x",
            self.sendCount, # seq Nr
            0,          # payload offset
            nrPixels,       # nr of pixels
            1,          # protocol vers. 1
            2,          # 'unsigned short' pxl type
            "LIVESIM",      # magic string
            width,    # width
            height    # height
            )
        
        image = data.astype(numpy.uint16)

        totalsend = 0
        while totalsend < 128:
            sent = self.sock.send( header[totalsend:128] )
            if sent == 0 :
                raise RuntimeError("header stopped sending")
            totalsend += sent

        totalsend = 0
        while totalsend < dataLen:
            sent = self.sock.send( image[totalsend:] )
            if sent == 0 :
                raise RuntimeError("image stopped sending")
            totalsend += sent



def test( hostname="localhost", nrImages=10000, delayTime=.1):

    imgSend = ImageSender()
    imgSend.connect( hostname )

    print "generating data"
    data = [ numpy.random.random_integers( i*10+1000, i*10+2000, [512,512] ) for i in range(0,100)]
 
    print "sending data"
    
    for imgCount in range( 0, nrImages ):
        print "sending ",imgCount
        imgSend.sendImage(data[imgCount%100])
        sleep(delayTime)



