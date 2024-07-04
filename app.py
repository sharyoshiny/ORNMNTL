from flask import Flask, request, jsonify
from flask_cors import CORS
import io
from PIL import Image
from OrnamentalAPI import process_image_to_3d_mesh  # Import your image processing function

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in the request'}), 400

    image = request.files['image']
    img = Image.open(io.BytesIO(image.read()))

    try:
        result = process_image_to_3d_mesh(img)  # Process the image
        return jsonify({'message': 'Image processed successfully', 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)