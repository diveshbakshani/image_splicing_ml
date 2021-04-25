import cv2
import numpy as np
import os


def rgbavg(image_path,part):
    src = cv2.imread(image_path)
    w,h,c = src.shape
    #print(w,h,c)
    red_channel = src[:, :, 2]
    green_channel = src[:, :, 1]
    blue_channel = src[:, :, 0]

    red = []
    green = []
    blue = []


    for i in range(w):
        for j in range(h):

            red.append(red_channel[i,j])
            green.append(green_channel[i, j])
            blue.append(blue_channel[i, j])

    red.sort()
    blue.sort()
    green.sort()

    r_mean = []
    g_mean = []
    b_mean = []
    step = int(len(red) / int(part))
    #print(len(red))
    j = 0
    k = step

    r = []
    g = []
    b = []

    while (k <= len(red)):
        for i in range(j, k):
            r.append(red[i])
            g.append(green[i])
            b.append(blue[i])

        r_m = np.mean(r)
        g_m = np.mean(g)
        b_m = np.mean(b)
        r_mean.append(r_m)
        g_mean.append(g_m)
        b_mean.append(b_m)
        r.clear()
        g.clear()
        b.clear()
        #print("mean = ", mean)
        j += step
        k += step

    #print(r_mean,g_mean,b_mean)

    return(r_mean,g_mean,b_mean)

#rgbavg('Au_ani_0021.jpg')