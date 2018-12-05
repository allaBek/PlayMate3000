#!/usr/bin/env python

'''
Feature-based image matching sample.

Note, that you will need the https://github.com/opencv/opencv_contrib repo for SIFT and SURF

USAGE
  arm_feature_detector.py [--feature=<sift|surf|orb|akaze|brisk>[-flann]] [ <reference> ]

  --feature  - Feature to use. Can be sift, surf, orb or brisk. Append '-flann'
               to feature name to use Flann-based matcher instead bruteforce.

'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

class ArmDetector:

    FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
    FLANN_INDEX_LSH    = 6

    def anorm2(self, a):
        return (a*a).sum(-1)

    def anorm(self, a):
        return np.sqrt( self.anorm2(a) )

    def getsize(self, img):
        h, w = img.shape[:2]
        return w, h

    def init_feature(self, name):
        chunks = name.split('-')
        if chunks[0] == 'sift':
            detector = cv.xfeatures2d.SIFT_create()
            norm = cv.NORM_L2
        elif chunks[0] == 'surf':
            detector = cv.xfeatures2d.SURF_create(800)
            norm = cv.NORM_L2
        elif chunks[0] == 'orb':
            detector = cv.ORB_create(400)
            norm = cv.NORM_HAMMING
        elif chunks[0] == 'akaze':
            detector = cv.AKAZE_create()
            norm = cv.NORM_HAMMING
        elif chunks[0] == 'brisk':
            detector = cv.BRISK_create()
            norm = cv.NORM_HAMMING
        else:
            return None, None
        if 'flann' in chunks:
            if norm == cv.NORM_L2:
                flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            else:
                flann_params= dict(algorithm = FLANN_INDEX_LSH,
                                   table_number = 6, # 12
                                   key_size = 12,     # 20
                                   multi_probe_level = 1) #2
            matcher = cv.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
        else:
            matcher = cv.BFMatcher(norm)
        return detector, matcher


    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        mkp1, mkp2 = [], []
        for m in matches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        return p1, p2, list(kp_pairs)

    def explore_match(self, win, img1, img2, kp_pairs, status = None, H = None):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1+w2] = img2
        vis = cv.cvtColor(vis, cv.COLOR_GRAY2BGR)
        center = []

        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32( cv.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
            ###############################################################
            center = [sum(x) for x in zip(*corners)]        # Compute the center of the features 
            center = (center[0]/4, center[1]/4)
            # Draw the center of the features
            cv.circle(vis,center, 10, (0,0,255), -1)
            #print(center)
            ##############################################################
            cv.polylines(vis, [corners], True, (255, 255, 255))

        if status is None:
            status = np.ones(len(kp_pairs), np.bool_)
        p1, p2 = [], []  # python 2 / python 3 change of zip unpacking
        for kpp in kp_pairs:
            p1.append(np.int32(kpp[0].pt))
            p2.append(np.int32(np.array(kpp[1].pt) + [w1, 0]))
        
        #cv.imshow(win, vis)
        # return center of the arm and the frame with some drawings on it
        if center:
            return center, vis
        else:
            return [], vis
        
    def arm_detector(self, frame):
        #print(__doc__)
        # I kept the usage as it was but only for reference frame !
        import sys, getopt


        opts, args = getopt.getopt(sys.argv[1:], '', ['feature='])
        opts = dict(opts)
        feature_name = opts.get('--feature','brisk')
        try:
            fn1, _ = args
        except:
            fn1 = 'ref.png'
            #fn2 = '../data/box_in_scene.png'
        
        img1 = cv.imread(fn1, 0)
        #img2 = cv.imread(fn2, 0)
        detector, matcher = self.init_feature(feature_name)
        
        if img1 is None:
            print('Failed to load fn1:', fn1)
            sys.exit(1)

        if detector is None:
            print('unknown feature:', feature_name)
            sys.exit(1)

        #If empty frame is received from the main class, return empty list
        img2 = frame

        img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        kp1, desc1 = detector.detectAndCompute(img1, None)
        kp2, desc2 = detector.detectAndCompute(img2, None)
        #print('img1 - %d features, img2 - %d features' % (len(kp1), len(kp2)))

        def match_and_draw( win):
            #print('matching...')
            raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2) #2
            p1, p2, kp_pairs = self.filter_matches(kp1, kp2, raw_matches)
            if len(p1) >= 4:
                H, status = cv.findHomography(p1, p2, cv.RANSAC, 5.0)
                #print('%d / %d  inliers/matched' % (np.sum(status), len(status)))
            else:
                H, status = None, None
                #print('%d matches found, not enough for homography estimation' % len(p1))

            return self.explore_match(win, img1, img2, kp_pairs, status, H)

        position, arm_frame = match_and_draw('find_arm')

        return position, arm_frame
