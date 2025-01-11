import cv2

# Reference and examined photo
photo = ('Foto/Test.jpg')
image = cv2.imread(photo)
image2 = cv2.imread(photo)
reference_image = cv2.imread('Foto/Full.jpg')


def find_bottle_height(image, cap_height=0):
    # Change the photo to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Reduce noise by blurring using a Gaussian filter
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Canny algorithm for edge detection
    edges = cv2.Canny(blurred, 50, 150)
    # findContours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Finding the contour with the largest area -> fluid contour
    max_area = 0
    max_contour = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > max_area:
            max_area = area
            max_contour = contour

    liquid_height = 0
    if max_contour is not None:
        # Bounding box (green)
        x, y, w, h = cv2.boundingRect(max_contour)
        liquid_height = h
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Finding the bounding box for all contours -> bottle contour
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), 0, 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)

    # Bounding box (blue)
    cv2.rectangle(image, (min_x, min_y + cap_height), (max_x, max_y), (255, 0, 0), 2)
    bottle_height = max_y - min_y

    return liquid_height, bottle_height


def find_cap(image, ref_liquid_height):
    # Cutting out a cap from a photo
    crop_ref_img = image[:(image.shape[0] - ref_liquid_height) - 200, :]
    # Change the photo to gray
    gray = cv2.cvtColor(crop_ref_img, cv2.COLOR_BGR2GRAY)
    # Reduce noise by blurring using a Gaussian filter
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Canny algorithm for edge detection
    edges = cv2.Canny(blurred, 75, 150)
    # findContourse
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Finding the contour with the largest area -> cork contour
    cv2.imshow("contours", edges)
    max_area = 0
    max_contour = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > max_area:
            max_area = area
            max_contour = contour

    # Bounding boxa (red) and determining its height
    if max_contour is not None:
        # Classification whether there is a cap or not
        if max_area < 7000:
            print("Missing cap")
        else:
            print("Cap present")
            x, y, w, h_ref = cv2.boundingRect(max_contour)
            cv2.rectangle(image, (x, y), (x + w, y + h_ref), (0, 0, 255), 2)
    return crop_ref_img


# Finding the base, maximum liquid level
ref_liquid_height, ref_bottle_height = find_bottle_height(reference_image)
cap_height = ref_bottle_height - ref_liquid_height
# Execution of find_bottle_height function with known cap_height
liquid_height, bottle_height = find_bottle_height(image, cap_height)

if liquid_height <= cap_height:
    print("The bottle is empty")
    find_cap(image2, ref_liquid_height)
    cv2.imshow("Solution", image2)
    cv2.imwrite("Foto/Solution.jpg", image2)


else:
    print("The amount of liquid in the bottle is", round(liquid_height / (bottle_height - cap_height) * 100, 2), "%")
    # Displaying the examined photo with bounding boxes
    find_cap(image, ref_liquid_height)
    cv2.imshow("Solution", image)
    cv2.imwrite("Foto/Solution.jpg", image)

cv2.imshow('Reference', reference_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
