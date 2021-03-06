import scipy
from scipy import ndimage
from scipy import misc
import numpy as np
import sys
import datetime

class Segmentation(object):

    # Parameters
    # ----------
    # img_path : string
    def __init__(self,path):
        blur_radius = 1.0
        threshold = 50

        img = misc.imread(path)
        self.origin = img
        # smooth the image (to remove small objects)
        imgf = ndimage.gaussian_filter(img, blur_radius)
        threshold = 50
        # find connected components
        self.img, self.count = ndimage.label(imgf > threshold)
        self.labels = self.calculate_labels()


    # Return
    # ----------
    # labels : dictionary, key = label, value = list of bounding in order y1, y2, x1, x2
    def get_labels(self):
        return self.labels


    def calculate_labels(self):
        labels = {}
        for label in range(1, self.count + 1):
            labels[label] = [sys.maxint,-1,sys.maxint,-1]

        img = self.img
        for row in range(img.shape[0]):
            for col in range(img.shape[1]):
                value = img[row][col]
                if value != 0:
                    bounding = labels[value]
                    if bounding[0] > row:
                        bounding[0] = row
                    if bounding[2] > col:
                        bounding[2] = col
                    if bounding[1] < row:
                        bounding[1] = row
                    if bounding[3] < col:
                        bounding[3] = col

        to_del = []
        for label in labels:
            bounding = labels[label]
            if (bounding[1] - bounding[0]) * (bounding[3] - bounding[2]) < 50:
                to_del.append(label)
        for key in to_del:
            del labels[key]
        return labels


    # Parameters
    # ----------
    # label : int
    #     Label of the stroke to be found
    #
    # Returns
    # -------
    # np.ndarray
    # the stroke image in format of np array
    def get_stroke(self,label):
        l = self.labels[label]

        stroke = np.copy(self.img[l[0]:l[1] + 1,l[2]:l[3] + 1])

        """
        following is binary stroke
        """
        # for data in np.nditer(stroke, op_flags=['readwrite']):
        #     if data != label:
        #         data[...] = 0
        #     else:
        #         data[...] = 255

        """
        following is the stroke from origin image
        """
        shape = stroke.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                if stroke[i][j] != label:
                    stroke[i][j] = 0
                else:
                    stroke[i][j] = self.origin[i+l[0]][j+l[2]]

        return stroke


    # Parameters
    # ----------
    # l_labels : list
    #     A list of stroke labels representing the strokes to be combined
    #
    # Returns
    # -------
    # np.ndarray
    # the combined stroke image in format of np array
    def get_combined_strokes(self,l_labels):
        bounding = self.get_combined_bounding(l_labels)
        stroke = np.copy(self.img[bounding[0]:bounding[1]+1,bounding[2]:bounding[3]+1])

        """
        following is binary stroke
        """
        # for data in np.nditer(stroke, op_flags=['readwrite']):
        #     if data in l_labels:
        #         data[...] = 255
        #     else:
        #         data[...] = 0

        """
        following is the stroke from origin image
        """
        shape = stroke.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                if stroke[i][j] in l_labels:
                    stroke[i][j] = self.origin[i+bounding[0]][j+bounding[2]]
                else:
                    stroke[i][j] = 0

        return stroke


    # Parameters
    # ----------
    # l_labels : list
    #     A list of stroke labels representing the strokes to be combined
    #
    # Returns
    # -------
    # list
    # the list of bounding of combined strokes
    def get_combined_bounding(self,l_labels):
        l = [sys.maxint,-1,sys.maxint,-1]
        for label in l_labels:
            bounding = self.labels[label]
            if bounding[0] < l[0]:
                l[0] = bounding[0]
            if bounding[1] > l[1]:
                l[1] = bounding[1]
            if bounding[2] < l[2]:
                l[2] = bounding[2]
            if bounding[3] > l[3]:
                l[3] = bounding[3]
        return l


if __name__ == '__main__':
    fname='annotated/SKMBT_36317040717280_eq3.png'
    seg = Segmentation(fname)

    print seg.labels

    for label in seg.labels.keys():
        print label
        stroke = seg.get_stroke(label)
        scipy.misc.imsave('./tmp/'+ str(label)+'.png', stroke)

    #
    origin = seg.origin
    scipy.misc.imsave('./tmp/origin.png', origin)


    # combined = seg.get_combined_strokes([1,2])
    # scipy.misc.imsave('./tmp/combined.png', combined)
