import cv2

img = cv2.imread('drawing.png')
red = (0, 0, 255)

start_point = (405, int(1286.125))
end_point = (405+730, int(1286.125+22))
img = cv2.rectangle(img, start_point, end_point, red, 1)

start_point = (405, int(1286.125))
end_point = (405+730, int(1286.125+103))
img = cv2.rectangle(img, start_point, end_point, red, 1)

start_point = (405, int(1286.125))
end_point = (405+730, int(1286.125+184))
img = cv2.rectangle(img, start_point, end_point, red, 1)

cv2.imwrite('line.png', img)
