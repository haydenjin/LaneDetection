import cv2
import numpy as np


def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # blur the image, (optional as canny does this automatically)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # canny changes the picture into change lines which correspond to changes in intensity
    canny = cv2.Canny(blur, 50, 150)

    return canny


# Displaying image of road lines
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


# creating a triangle of interest where the lanes are
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array(
        [
            [(200, height), (1100, height), (550, 250)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    # merging both images together to only focus on the lanes
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


# Running program on a video
cap = cv2.VideoCapture("test2.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while cap.isOpened():
    _, frame = cap.read()

    image = cv2.imread('test_image.jpg')
    # Making a copy of image to convert to gray scale
    lane_image = np.copy(image)

    # creating a class variable
    canny_image = canny(frame)

    cropped_image = region_of_interest(canny_image)

    # Calculating where lines are
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)

    # Creating large single lines instead of smaller separate lines
    averaged_lines = average_slope_intercept(frame, lines)

    line_image = display_lines(frame, averaged_lines)

    # Blending lines output with original image
    combo_image = cv2.addWeighted(frame, 1, line_image, 1, 1)

    # outputting result image
    cv2.imshow('Result', combo_image)


    # Press q to break out of loop
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# Old code for testing on an image

# image = cv2.imread('test_image.jpg')
# # Making a copy of image to convert to gray scale
# lane_image = np.copy(image)
#
# # creating a class variable
# canny_image = canny(lane_image)
#
# cropped_image = region_of_interest(canny_image)
#
# # Calculating where lines are
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
#
# # Creating large single lines instead of smaller separate lines
# averaged_lines = average_slope_intercept(lane_image, lines)
#
# line_image = display_lines(lane_image, averaged_lines)
#
# # Blending lines output with original image
# combo_image = cv2.addWeighted(lane_image, 1, line_image, 1, 1)
#
# # outputting result image
# cv2.imshow('ROI', combo_image)
# cv2.waitKey(0)
