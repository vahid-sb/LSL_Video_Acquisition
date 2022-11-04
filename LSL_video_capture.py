# -*- coding: utf-8 -*-
"""
Created on 28.10.2022.

@author: Vahid S. Bokharaie
"""

def createOutlet(index, filename):
    import uuid
    import os
    import sys
    from pylsl import StreamInfo, StreamOutlet
    
    streamName = 'FrameMarker'+str(index+1)
    info = StreamInfo(name=streamName,
                      type='videostream',
                      channel_format='float32',
                      channel_count=1,
                      source_id=str(uuid.uuid4()))

    dir_file = os.path.dirname(filename)
    if not os.path.exists(dir_file):
        print('Creating folder', dir_file)
        os.makedirs(dir_file)
    if sys.platform == "linux":
        videoFile = os.path.splitext(filename)[0]+'.ogv'
    videoFile = filename
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)


if __name__ == "__main__":
    import cv2
    import datetime
    import os 
    
    dir_out = os.path.dirname(os.path.realpath(__file__))
    # ## Use check_available_ports.py to find out the index number of the webcam/camera
    dev = 1 
    cap = cv2.VideoCapture(dev)  
    if not cap.isOpened():
        print("Cannot open camera")
        import sys
        sys.exit()
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('(fps, width, height) = ', (fps, width, height))
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    str_datetime = datetime.datetime.now().strftime("_%Y%m%d_%H%M")
    filename = os.path.join(dir_out, 'Camera' + str(dev) +
                            str_datetime + '.avi')
    out = cv2.VideoWriter(filename, fourcc, fps, (int(width), int(height)))
    frameCounter = 1
    outlet = createOutlet(dev, filename)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
  
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        out.write(frame)
        outlet.push_sample([frameCounter])
        cv2.imshow('Press q to end.', frame)
        frameCounter += 1
        if cv2.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Saved output video to:', filename)
    # filename is logged in 'info' -> 'desc' part of the xdf file saved by LSL Lab Recorder. 
    