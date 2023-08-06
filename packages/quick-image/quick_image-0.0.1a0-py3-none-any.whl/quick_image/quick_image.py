import requests
import os
from sklearn.externals._pilutil import imresize
import matplotlib.image as mat_img
import math
from skimage.color import rgb2lab, deltaE_cie76
import cv2
import matplotlib.pyplot as plt
from skimage import morphology
import numpy as np
import skimage
from skimage.metrics import structural_similarity
from sentence_transformers import SentenceTransformer, util
from PIL import Image

from quick_image.image_point_picker import ImagePointPicker


def quick_download_image(pic_url,save_path):

    if os.path.exists(save_path):
        return
    response = requests.get(pic_url, stream=True)

    if not response.ok:
        print(response)
        return

    with open(save_path, 'wb') as handle:
        if response.ok:
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

def quick_show_image(image_path):
    img = Image.open(image_path)
    img.show()

def quick_show_image_by_grayscale(image_path):
    # Setup maximum factors for each channel
    r_max = 255
    g_max = 255
    b_max = 255

    # Window title
    title_window = 'Custom gray scale'

    # Event for R trackbar change
    def on_r_trackbar(val):
        dst[:, :, 2] = val / r_max * src[:, :, 2]
        cv2.imshow(title_window, dst)

    # Event for G trackbar change
    def on_g_trackbar(val):
        dst[:, :, 1] = val / g_max * src[:, :, 1]
        cv2.imshow(title_window, dst)

    # Event for B trackbar change
    def on_b_trackbar(val):
        dst[:, :, 0] = val / b_max * src[:, :, 0]
        cv2.imshow(title_window, dst)

    # Read some input image
    src = cv2.imread(image_path)
    dst = src.copy()

    # Setup window and create trackbars for each channel
    cv2.namedWindow(title_window)
    cv2.createTrackbar('R', title_window, 100, r_max, on_r_trackbar)
    cv2.createTrackbar('G', title_window, 100, g_max, on_g_trackbar)
    cv2.createTrackbar('B', title_window, 100, b_max, on_b_trackbar)

    # Show something, and wait until user presses some key
    cv2.imshow(title_window, dst)
    cv2.waitKey()

def quick_show_image_by_grayscale2(image_path):
    # Setup maximum factor for the saturation
    s_max = 100

    # Window title
    title_window = 'Custom gray scale'

    # Event for S (saturation) trackbar change
    def on_s_trackbar(val):
        dst[:, :, 1] = val / s_max * hsv[:, :, 1]
        cv2.imshow(title_window, cv2.cvtColor(dst, cv2.COLOR_HSV2BGR))

    # Read some input image, and convert to HSV color space
    src = cv2.imread(image_path)
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    dst = hsv.copy()

    # Setup window and create trackbar for the S (saturation) channel
    cv2.namedWindow(title_window)
    cv2.createTrackbar('S', title_window, 100, s_max, on_s_trackbar)

    # Show something, and wait until user presses some key
    cv2.imshow(title_window, cv2.cvtColor(dst, cv2.COLOR_HSV2BGR))
    cv2.waitKey()

def quick_show_image_gray(image_path):
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray image", img_gray)
    cv2.waitKey()

def _matrix2uint8(matrix):
  '''
matrix must be a numpy array NXN
Returns uint8 version
  '''
  m_min= np.min(matrix)
  m_max= np.max(matrix)
  matrix = matrix-m_min
  return(np.array(np.rint( (matrix-m_min)/float(m_max-m_min) * 255.0),dtype=np.uint8))
  #np.rint, Round elements of the array to the nearest integer.

def _preprocess(img, crop=True, resize=True, dsize=(224, 224)):
  if img.dtype == np.uint8:
    img = img / 255.0

  if crop:
    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
  else:
    crop_img = img

  if resize:
    norm_img = imresize(crop_img, dsize)
  else:
    norm_img = crop_img

  return (norm_img).astype(np.float32)

def quick_convert_12bit_gray(image_path,save_path):
    img = mat_img.imread(image_path)

    img = _matrix2uint8(_preprocess(img=img, crop=False, resize=False))
    status = cv2.imwrite(save_path, img)
    return status

def quick_show_canny(image_path):

    TOP_SLIDER = 10
    TOP_SLIDER_MAX = 200
    t1 = 100
    T1 = 10
    edges = 0

    def setT1(t1):
        global T1
        T1 = t1
        print(t1)
        if T1 < TOP_SLIDER:
            T1 = 10
        edges = cv2.Canny(image, T1, 3 * T1)
        cv2.imshow("canny", edges)

    image = cv2.imread(image_path, 0)
    edges = cv2.Canny(image, T1, 3 * T1)
    cv2.imshow("canny", edges)
    cv2.createTrackbar("T1", "canny", t1, TOP_SLIDER_MAX, setT1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def quick_replace_image_color(image_path,color_value=255,show=False,low1=None,high1=None):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.

    # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
    # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
    # 明度（V），取0-100%。
    # OpenCV中H,S,V范围是0-180,0-255,0-255
    low = np.array([0, 0, 0])
    high = np.array([180, 255, 46])
    if low1!=None:
        low=low1
    if high1!=None:
        high=high1

    dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

    # 寻找白色的像素点坐标。
    # 白色像素值是255，所以np.where(dst==255)
    xy = np.column_stack(np.where(dst == color_value))

    # 在原图的红色数字上用 金黄色 描点填充。
    for c in xy:
        # 注意颜色值是(b,g,r)，不是(r,g,b)
        # 坐标:c[1]是x,c[0]是y
        cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 215, 255), thickness=1)

    if show:
        cv2.imshow('dst', dst)
        cv2.imshow('result', img)
        cv2.waitKey(0)
    return dst,img

def quick_save_edges(img_path, save_path, t=120):
    image = cv2.imread(img_path, 0)
    edges = cv2.Canny(image, t, 3 * t)

    cv2.imwrite(save_path,edges)

def quick_get_edges(img_path,  t=120):
    image = cv2.imread(img_path, 0)
    edges = cv2.Canny(image, t, 3 * t)
    return edges

def _dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def quick_filter_by_dist(image_path,show=True,c_x=0,c_y=0,max_dist=200):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 色彩空间转换为hsv，分离.

    # 色相（H）是色彩的基本属性，就是平常所说的颜色名称，如红色、黄色等。
    # 饱和度（S）是指色彩的纯度，越高色彩越纯，低则逐渐变灰，取0-100%的数值。
    # 明度（V），取0-100%。
    # OpenCV中H,S,V范围是0-180,0-255,0-255
    low = np.array([0, 0, 0])
    high = np.array([180, 255, 46])

    dst = cv2.inRange(src=hsv, lowerb=low, upperb=high)  # HSV高低阈值，提取图像部分区域

    # 寻找白色的像素点坐标。
    # 白色像素值是255，所以np.where(dst==255)
    xy = np.column_stack(np.where(dst == 0))
    # print(xy)


    # 在原图的红色数字上用 金黄色 描点填充。
    for c in xy:

        x=c[0]
        y=c[1]

        if _dist(x,y,c_x,c_y)<=max_dist:
            # print(c, _dist(c_x, c_y, x, y))
            # 注意颜色值是(b,g,r)，不是(r,g,b)
            # 坐标:c[1]是x,c[0]是y
            cv2.circle(img=img, center=(int(c[1]), int(c[0])), radius=1, color=(0, 0, 255), thickness=1)
    if show:
        cv2.imshow('dst', dst)
        cv2.imshow('result', img)
        cv2.waitKey(0)
    return dst,img

def quick_pick_image_color(image_path,point_file=None,color_file=None):
    ipp = ImagePointPicker()
    return ipp.start_to_pick_color(img_path=image_path, save_points_file=point_file,save_colors_file=color_file)

def quick_remove_pix_color(image_path,target_color,save_path=None):

    # target_color = [37, 86, 115]

    image = Image.open(image_path)
    # image.show()
    image_data = image.load()
    height, width = image.size
    for loop1 in range(height):
        for loop2 in range(width):
            r, g, b = image_data[loop1, loop2]
            if r == target_color[0] and g == target_color[1] and b == target_color[2]:
                image_data[loop1, loop2] = 0, 0, 0
    if save_path!=None:
        image.save(save_path)
    return image


def quick_remove_pix_color_by_range(image_path,lower_color,upper_color,show=True):
    #lower_blue = np.array([100, 150, 0])
    #upper_blue = np.array([140, 255, 255])

    img = cv2.imread(image_path)
    # img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lower_color, upper_color)
    mask = 255 - mask
    res = cv2.bitwise_and(img, img, mask=mask)
    if show:
        cv2.imshow("mask", mask)
        cv2.imshow("cam", img)
        cv2.imshow("res", res)
        cv2.waitKey()
    return mask,img,res

def quick_color_similarity(color1,color2):
    return math.sqrt(sum((color1[i] - color2[i]) ** 2 for i in range(3)))

def get_pct_color(img_rgb, rgb_color, threshold=10):
    img_lab = rgb2lab(img_rgb)
    rgb_color_3d = np.uint8(np.asarray([[rgb_color]]))
    rgb_color_lab = rgb2lab(rgb_color_3d)
    delta = deltaE_cie76(rgb_color_lab, img_lab)
    x_positions, y_positions = np.where(delta < threshold)
    nb_pixel = img_rgb.shape[0] * img_rgb.shape[1]
    pct_color = len(x_positions) / nb_pixel
    return pct_color

def quick_remove_noise1(image_path,save_path=None,intensity=5,rect1=5,rect2=2):
    img = cv2.imread(image_path)

    # cv2.imshow('Original', img)

    img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > intensity).astype('uint8')

    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect1, rect1))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect2, rect2))
    mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

    mask = np.dstack([mask, mask, mask]) / 255
    out = img * mask

    # cv2.imshow('Output', out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if save_path!=None:
        cv2.imwrite(save_path, out)
    return out

def quick_remove_noise2(image_path,save_path=None,min_size=2,connectivity=2,thresold=0.1):
    # read the image, grayscale it, binarize it, then remove small pixel clusters
    im1 = plt.imread(image_path)
    im = skimage.color.gray2rgb(im1)
    grayscale = skimage.color.rgb2gray(im)

    binarized = np.where(grayscale > thresold, 1, 0)
    processed = morphology.remove_small_objects(binarized.astype(bool), min_size=min_size, connectivity=connectivity).astype(int)

    # black out pixels
    mask_x, mask_y = np.where(processed == 0)
    im[mask_x, mask_y, :3] = 0

    # plot the result
    # plt.figure(figsize=(10, 10))
    # plt.imshow(im)
    if save_path!=None:
        plt.imsave(save_path, im)
    return im

