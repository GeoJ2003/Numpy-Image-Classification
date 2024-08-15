from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import matrixclass as mc  # Assuming mc is a module you have

app = Flask(__name__)
matrix_classes = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_variable', methods=['POST'])
def set_variable():
    global matrix_classes
    data = request.json
    folders = data['folders']
    num_images = data['num_images']
    matrix_classes = mc.MC_list('imgs/mnist', num_images, folders)
    
    # Gather image paths
    image_paths = []
    for matrix_class in matrix_classes.matrix_classes:
        for img_name in matrix_class.imgs_dict:
            # img_path = os.path.join('imgs/mnist', matrix_class.name, img_name)
            image_paths.append('imgs/mnist/' + matrix_class.name + '/' + img_name)

    return jsonify(success=True, image_paths=image_paths)

@app.route('/classify_dirs', methods=['POST'])
def classify_dirs():
    global matrix_classes
    data = request.json
    num_images = data['num_images']
    if not matrix_classes:
        return jsonify(success=False, message="Matrix classes not set"), 400

    try:
        perCorrect, perIncorrect, confidence = matrix_classes.classify_dirs('imgs/mnist', num_images)
        return jsonify(success=True, perCorrect=perCorrect, perIncorrect=perIncorrect, confidence=confidence)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route('/imgs/mnist/<path:filename>')
def serve_images(filename):
    return send_from_directory('imgs/mnist', filename)

if __name__ == '__main__':
    app.run(debug=True)