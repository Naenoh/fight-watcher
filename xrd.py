# This file contains functions i wrote to process Guilty Gear Xrd vods
# I have stopped trying to do that as https://ggsnap.yasashii.world/en is a thing (and i suspect its automated)
# I still kept them here in case i need to do something similar for another game

def find_timer(img, template):
    # Apply template Matching
    res = cv.matchTemplate(img,template,cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    return max_val

def find_timer_all_methods(imgpath, templatepath):
    template = cv.imread(templatepath,0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    #methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED','cv.TM_CCORR',
    #            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    methods = ['cv.TM_CCORR_NORMED']
    img = cv.imread(imgpath,0)
    img2 = img.copy()
    for meth in methods:
        start = time.time()
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        end = time.time()
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            res = min_val
            top_left = min_loc
        else:
            res = max_val
            top_left = max_loc
        print(meth, res, end - start)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 4)
        plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()