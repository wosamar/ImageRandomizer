import os
import random
from flask import Flask, jsonify, send_from_directory

# 建立 Flask 應用程式
app = Flask(__name__)

# 定義圖片資料夾的絕對路徑
# 這裡假設圖片資料夾 'images' 與 app.py 在同一個目錄下
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')


@app.route('/api/random-image', methods=['GET'])
def get_random_image():
    """
    這個 API endpoint 會隨機回傳一張圖片。
    """
    try:
        # 獲取圖片資料夾中的所有檔案名稱
        images = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]

        if not images:
            # 如果資料夾是空的，回傳錯誤訊息
            return jsonify({"error": "No images found in the directory."}), 404

        # 從檔案列表中隨機選擇一個圖片
        random_image_name = random.choice(images)

        # 直接回傳圖片檔案
        return send_from_directory(IMAGE_FOLDER, random_image_name)

    except Exception as e:
        # 處理任何可能發生的錯誤
        return jsonify({"error": str(e)}), 500


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
