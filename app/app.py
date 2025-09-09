import os
import random
import cloudinary
import cloudinary.api
import requests as requests
from flask import Flask, jsonify, request
from flask.cli import load_dotenv

app = Flask(__name__)
load_dotenv()

try:
    cloud_name = os.environ['CLOUDINARY_CLOUD_NAME']
    api_key = os.environ['CLOUDINARY_API_KEY']
    api_secret = os.environ['CLOUDINARY_API_SECRET']

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
except KeyError as e:
    print(f"環境變數 {e} 未設定，請檢查您的 Cloudinary 設定。")


def get_random_image_url(folder_name):
    """從 Cloudinary 圖片庫中隨機選擇指定資料夾或整個媒體庫的圖片。"""
    try:
        # 如果提供了資料夾名稱，就只從該資料夾中搜尋
        if folder_name:
            result = cloudinary.api.resources_by_asset_folder(folder_name)
        # 如果沒有提供資料夾名稱，則搜尋整個媒體庫
        else:
            result = cloudinary.api.resources(
                type="upload",
                max_results=50
            )

        images = result.get('resources', [])

        if not images:
            return None

        # 隨機選擇一張圖片
        random_image = random.choice(images)

        # 取得圖片的公開 URL
        image_url = random_image.get('secure_url')
        return image_url

    except Exception as e:
        print(f"Error getting random image from Cloudinary: {e}")
        return None


@app.route('/api/random-image')
def random_image_endpoint():
    folder_name = request.args.get('dir')
    image_url = get_random_image_url(folder_name)
    if image_url:
        try:
            # 取得圖片內容
            response = requests.get(image_url)
            response.raise_for_status()  # 檢查請求是否成功

            # 取得圖片的 MIME Type
            content_type = response.headers.get('content-type', 'image/jpeg')

            # 直接回傳圖片內容
            return response.content, 200, {'Content-Type': content_type}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image from Cloudinary: {e}")
            return jsonify({"error": "Failed to fetch image."}), 500
    else:
        return jsonify({"error": "No images found or an error occurred."}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
