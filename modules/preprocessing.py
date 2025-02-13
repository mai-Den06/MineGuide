import cv2

def image_preprocessing(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # 画像サイズ取得
    h, w, _ = image.shape

    # 切り取りサイズ（中央70%）
    crop_w, crop_h = int(w * 0.7), int(h * 0.7)

    # 切り取り範囲 (中央)
    x1, y1 = (w - crop_w) // 2, (h - crop_h) // 2
    x2, y2 = x1 + crop_w, y1 + crop_h

    # 画像を切り取る
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image