# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 07:39:42 2020

@author: Anuj
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 00:33:34 2020

@author: Anuj
"""

import numpy as np
import cv2
import socket
import requests
import pygame
import os
import time
import pandas as pd
UP = LEFT = DOWN = RIGHT = ACCELERATE = DECELERATE = False

class StreamingServer(object):
    def __init__(self):
        # REST API url
        #Home hotspot IP: 192.168.43.137
        self.restUrl = 'http://192.168.0.31:5000/messages'

        # Start Socket Server
        self.server_socket = socket.socket()
        #Home hotspot PC IP: 192.168.43.248/0.19
        self.server_socket.bind(('192.168.0.19', 8000))
        self.server_socket.listen(1)
        self.conn, self.client_address = self.server_socket.accept()
        self.connection = self.conn.makefile('rb')
        
        self.send_inst = True
        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')
        
        # Pygame Initialization
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((800,600))
        pygame.display.set_caption('SDRC')

        # Stream and collect data
        self.streamAndCollectData()  

    def get_keys(self):
        change = False
        stop = False
        key_to_global_name = {
            pygame.K_LEFT: 'LEFT',
            pygame.K_RIGHT: 'RIGHT',
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_ESCAPE: 'QUIT',
            pygame.QUIT: 'QUIT'
        }

        for event in pygame.event.get():
            if event.type in {pygame.K_q, pygame.QUIT}:
                stop = True
            elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
                down = (event.type == pygame.KEYDOWN)
                change = (event.key in key_to_global_name)
                if event.key in key_to_global_name:
                    globals()[key_to_global_name[event.key]] = down
        return (UP, DOWN, LEFT, RIGHT, change, stop)
    
    def sendData(self,dat):       
        payload = dict(data=dat)
        response = requests.post(self.restUrl, params=payload)
    
    def streamAndCollectData(self):
        saved_frame = 0
        total_frame = 0
        try:
            print("Connection from:", self.client_address)
            print("Start Collecting Images....")
            e1 = cv2.getTickCount()
            image_array = np.zeros((1, 38400))
            label_array = np.zeros((1, 4), 'float')
            command = 'x'
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last!= -1:
                    jpg = stream_bytes[first:last+2]
                    stream_bytes = stream_bytes[last+2:]
                    
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    roi = image[120:240, :]
                    cv2.imwrite('training_img/frame{:>05}.jpg'.format(frame), image)
                    
                    
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    frame += 1
                    total_frame += 1
                    time.sleep(0.5)
                    up_key, down, left, right, change, stop = self.get_keys()
                    if change:
                        print('Change')
                        command = 'x'
                        
                        #image_array = np.vstack((image_array, temp_array))
                        #label_array = np.vstack((label_array, self.k[4]))
                        
                        #saved_frame += 1
                                        
                        if up_key:
                            #cmmd = 'Forward' # ADDED
                            print('up')
                            command = 'w'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[2])) # UP: self.k[2] = [0., 0., 1.]
        
                            saved_frame+=1
                                    
                        elif down:
                            #cmmd = 'Reverse' # ADDED
                            print('down')
                            command = 's'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[3]))
        
                            saved_frame+=1
                        #append = lambda x: cmmd + '_' + x if cmmd != 'idle' else x
                        elif right:
                            #cmmd = append('right') # ADDED
                            print('right')
                            command = 'd'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1])) # RIGHT self.k[1] = [0., 1., 0.]
        
                            saved_frame+=1
                                    
                        elif left:
                            #cmmd = append('left') # ADDED
                            print('left')
                            command = 'a'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0])) # LEFT self.k[0] = [1., 0., 0.]
        
                            saved_frame+=1
                        #Complex Commands
                        elif up_key and right:
                            print('Forward Right')
                            command = 'q'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[1]))
        
                            saved_frame += 1
                        elif up_key and left:
                            print("Forward Left")
                            command = 'e'
                            
                            #cv2.imwrite('training_images/Imageframe{:>05}.jpg'.format(frame), image)
                            
                            image_array = np.vstack((image_array, temp_array))
                            label_array = np.vstack((label_array, self.k[0]))
                            
                            saved_frame += 1
                    elif stop:
                        print("Exit")
                        self.send_inst = False
                        break
                        
                        
                        #print(cmmd)
                    self.sendData(command)
                    
                    train = image_array[1:, :]
                    train_label = label_array[1:, :]
                    
                    #Save Data as a Numpy File
                    file_name = str(int(time.time()))
                    directory = "training_data"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        np.savez(directory + '/' + file_name + '.npz', train= train, train_label = train_label)
                    except IOError as e:
                        print(e)
                    
                        
                    #pygameimage = pygame.transform.scale(pygameimage, (800,600))
                    #self.gameDisplay.fill((0,0,0))
                    #self.gameDisplay.blit(pygameimage, (0, 0))
                    #pygame.display.update()
    
                    #df = pd.DataFrame({"image_path":image_path,"labels":label_array})
                    #df.to_csv("dataset.csv",index = False)
                    e2 = cv2.getTickCount()
                    time0 = (e2 - e1)/cv2.getTickFrequency()
                    print('Streaming Frame:', time0)
                    print('Total Frames: ',total_frame)
                    print('Saved Frame:', saved_frame)
        finally:
            self.connection.close()
            self.server_socket.close()
        pygame.quit()
        quit()
            
                

if __name__ == '__main__':
    StreamingServer()