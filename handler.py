import numpy as np
import cv2


def viewImage(image, name_of_window='img'):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Center_eval(contours):
    """
    Returns centers of puzzle: numpy ndarray
    contours: list of contours of image
    """
    center_list = [np.mean(contr[:,0,:], axis=0) for contr in contours]
    return np.array(center_list)


def delete_small_objects(image, min_size):
    '''
    Returns image, where small objects deleted
    image: binarized
    min_size: int, minimum square to leave on image
    '''
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
    sizes = stats[1:, -1]; nb_components = nb_components - 1
    
    new_img = np.zeros((output.shape), dtype=np.ubyte)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            new_img[output == i + 1] = 255
    return new_img


def image_get_hands(gray):
    _,tresh = cv2.threshold(gray, 237, 255, cv2.THRESH_BINARY)
    closing = cv2.morphologyEx(tresh, cv2.MORPH_CLOSE, 
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)))
    med = cv2.medianBlur(closing, 15)
    return delete_small_objects(med,6000)


def get_hands_coordinates(img_hands):
    contours, hierarchy = cv2.findContours(img_hands, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        mask = hierarchy[0,:,3] == -1
        new_contrs = [contour for i, contour in enumerate(contours) if mask[i]]
        return Center_eval(new_contrs)
    else:
        return np.array([-1])


def decode_coordinates_comand(cd):
    sim = abs(np.dot(cd[:, 1], [-1,1]))

    if sim < 35:
        if cd[0,1] < 192: #0.4 * 480
            return "Forward"
        else:
            return "Backward"
    else:
        if (cd[:,0] < 320) @ cd[:,1] < 192:
            return "Left"
        else:
            return "Right"


def get_comand_type(coordinates, verbose=False):
    '''
    Returns integer (comand code)
    
    coordinates: ndarray, coordinates of centers of white spots on image
    '''
    if verbose:
        return coordinates.shape[0]
    if coordinates.size == 1:
        return "Raise your hands palms up to the sensor"
    else:
        if coordinates.shape[0] != 2:
            return "Smth other than the hands is captured"
        else:
            return decode_coordinates_comand(coordinates)


def operator_in_right_position(img):
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    d2 = delete_small_objects(th2, 80000)
    contours, hierarchy = cv2.findContours(d2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        mask = hierarchy[0,:,3] == -1

    new_contrs = [contour for i, contour in enumerate(contours) if mask[i]]
    objects = len(new_contrs)

    if objects == 1:
        return 1, ''
    elif objects > 1:
        return 0, 'Some other BIG objects in frame'
    else:
        return 0, 'Get closer to sensor'


def get_start(des_b):
    img = des_b.reshape(480,640,4)
    mask = np.array([True, True, True, False])
    img = img[:,:,mask]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    right, comand_to_man = operator_in_right_position(img)

    if right:
        binarized_img_hands = image_get_hands(img)
        hands_coordinates = get_hands_coordinates(binarized_img_hands)    
        return get_comand_type(hands_coordinates)
    else:
        return comand_to_man

