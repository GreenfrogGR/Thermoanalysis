import cv2
import numpy as np
from skimage.color import rgb2lab

def load_image(path):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Image not loaded; check path or file format.")
    return image

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_color_rgb = param['image'][y, x][:3]
        clicked_color_lab = rgb2lab(np.uint8(np.array([[clicked_color_rgb]])))[0][0]
        print(f"Clicked RGB: {clicked_color_rgb}, Clicked Lab: {clicked_color_lab}")
        closest_color_index, closest_color_y = find_closest_color(clicked_color_lab, param['color_bar_lab'], param['color_bar'].shape[1])
        print(f"Closest color position: ({closest_color_index}, {closest_color_y})")
        mapped_value = map_value(closest_color_y, param['color_bar'].shape[0], 20, 35)
        print(f"Mapped value at position: {mapped_value}")
        show_color_bar_with_marker(param['color_bar'], (closest_color_index, closest_color_y))

def find_closest_color(target_color, color_bar_lab, width):
    distances = np.sqrt(np.sum((color_bar_lab - target_color)**2, axis=1))
    index = np.argmin(distances)
    return index % width, index // width  # x, y 좌표 반환

def map_value(y, height, min_val, max_val):
    # Linearly map the y coordinate to a value between min_val and max_val
    return max_val - (y / (height - 1) * (max_val - min_val))

def show_color_bar_with_marker(color_bar_array, position):
    marked_color_bar = color_bar_array.copy()
    cv2.circle(marked_color_bar, position, 5, (0, 0, 255), -1)  # 빨간색 원을 그림
    cv2.imshow('Color Bar with Marker', marked_color_bar)

main_image_path = r"C:\Users\Gyurin\Desktop\Github\IR camera\11.tif"
color_bar_path = r"C:\Users\Gyurin\Desktop\Github\IR camera\colorbar.tif"

main_image = load_image(main_image_path)
color_bar = load_image(color_bar_path)

# RGB 이미지를 Lab 컬러 스페이스로 변환
main_image_lab = rgb2lab(main_image[:, :, :3])
color_bar_lab = rgb2lab(color_bar[:, :, :3]).reshape(-1, 3)  # 2D 이미지를 1D로 변환

cv2.imshow('Main Image', main_image)
params = {
    'image': main_image,
    'color_bar': color_bar,
    'color_bar_lab': color_bar_lab
}
cv2.setMouseCallback('Main Image', click_event, params)
cv2.waitKey(0)
cv2.destroyAllWindows()
