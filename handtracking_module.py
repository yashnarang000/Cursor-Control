import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

class HandTrace:
    def __init__(self, static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,min_tracking_confidence=0.5):
        
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.hands = mpHands.Hands(static_image_mode = self.static_image_mode, 
                              max_num_hands = self.max_num_hands, 
                              model_complexity = self.model_complexity,
                              min_detection_confidence = self.min_detection_confidence,
                              min_tracking_confidence = self.min_tracking_confidence)
        
    
    def id2axes(self, frame, input_id):
        '''
        returns a tuple (x,y)
        '''
        axes = self.axesDict(frame)
        
        if axes == None:
            (x,y) = (None, None)
        else:
            (x,y) = axes[input_id]
        
        return (x,y)
        
    def axesDict(self, frame):
        '''
        returns a dictionary {id: (x,y)}
        '''
        palm_data = self.hands.process(frame)
        multi_hand_landmarks = palm_data.multi_hand_landmarks
        
        if multi_hand_landmarks != None:
            axes = {}
            for single_hand_landmarks in multi_hand_landmarks:
                for temp_id, landmark in enumerate(single_hand_landmarks.landmark):
                    height, width, channels = frame.shape
                    cx, cy = int(width*landmark.x), int(height*landmark.y)
                    axes.update({temp_id:(cx, cy)})

            return axes
    
    def drawHandConnections(self, detection_frame, display_frame=0):
        '''
        detection_frame: frame in which the hand is to be tracked
        display_frame: frame in which the landmark connections are to be drawn (optional)
        '''
        palm_data = self.hands.process(detection_frame)
        multi_hand_landmarks = palm_data.multi_hand_landmarks
        if multi_hand_landmarks != None:
            for single_hand_landmarks in multi_hand_landmarks:
                if str(type(display_frame)) == "<class 'numpy.ndarray'>" :
                    mpDraw.draw_landmarks(display_frame, single_hand_landmarks, mpHands.HAND_CONNECTIONS)
                else:
                    mpDraw.draw_landmarks(detection_frame, single_hand_landmarks, mpHands.HAND_CONNECTIONS)

def distance(pt1, pt2):
        (xa, ya) = pt1
        (xb, yb) = pt2

        xn = abs(xb - xa)
        yn = abs(yb - ya)

        xs = pow(xn, 2)
        ys = pow(yn, 2)

        h = int(pow(xs + ys, 0.5))
        return h