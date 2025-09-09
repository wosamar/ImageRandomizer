import os
import random
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')


def get_random_image_path():
    """從圖片資料夾中隨機選擇一個圖片檔案路徑。"""
    try:
        # 確保資料夾存在
        full_path = os.path.join(app.root_path, IMAGE_FOLDER)
        if not os.path.exists(full_path):
            return None

        # 定義圖片的副檔名清單
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.tiff', '.jfif')

        # 取得所有圖片檔案，並過濾掉非圖片檔案
        images = [f for f in os.listdir(full_path)
                  if os.path.isfile(os.path.join(full_path, f)) and f.lower().endswith(image_extensions)]

        if not images:
            return None

        # 隨機選擇一張圖片
        random_image = random.choice(images)
        return random_image

    except Exception as e:
        print(f"Error getting random image: {e}")
        return None


@app.route('/api/random-image')
def random_image_endpoint():
    """回傳隨機圖片的 JSON 資料。"""
    image_name = get_random_image_path()
    if image_name:
        # 將圖片檔案包裝成 URL 回傳
        image_url = f"/api/images/{image_name}"
        return jsonify({"image_url": image_url})
    else:
        return jsonify({"error": "No images found or an error occurred."}), 404


@app.route('/images/<filename>')
def get_image(filename):
    """
    這個 endpoint 用來提供圖片檔案本身。
    """
    try:
        # 從圖片資料夾安全地發送圖片
        return send_from_directory(IMAGE_FOLDER, filename)
    except Exception as e:
        return jsonify({"error": "Image not found."}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
