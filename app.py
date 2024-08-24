from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import matrixclass as mc  # Assuming mc is a module you have

app = Flask(__name__)
matrix_classes = None
dir_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_directories', methods=['GET'])
def get_directories():
    global dir_dict
    base_path = 'imgs'
    dirs = os.listdir(base_path)
    for dir in dirs:
        full_path = os.path.join(base_path, dir)
        if os.path.isdir(full_path):  # Ensure it's a directory
            dir_dict[dir] = os.listdir(full_path)
    print(dir_dict)
    return jsonify(success=True, dir_dict=dir_dict)

@app.route('/settings', methods=['POST'])
def least_num_imgs():
    data = request.json
    dirs = data['dirs']
    
    # Assuming all directories share the same parent directory
    parent_dir = next(iter(dirs.values()))
    
    base_path = os.path.join('imgs', parent_dir)
    min_images = float('inf')
    
    for dir in dirs.keys():
        full_path = os.path.join(base_path, dir)
        if os.path.isdir(full_path):
            image_count = len([f for f in os.listdir(full_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
            if image_count < min_images:
                min_images = image_count
    
    # Return the result as a JSON response
    return jsonify(success=True, min_images=min_images)

@app.route('/train', methods=['POST'])
def train():
    global matrix_classes
    data = request.json
    dir = data['dir']
    folders = data['folders']
    num_images = data['num_images']
    threshold = data['threshold']
    width = data['width']
    height = data['height']
    matrix_classes = mc.MC_list('imgs/' + dir, num_images, folders, threshold, width, height)
    
    # Gather image paths
    image_paths = []
    for matrix_class in matrix_classes.matrix_classes:
        for img_name in matrix_class.imgs_dict:
            img_path = 'imgs/' + dir + '/' + matrix_class.name + '/' + img_name
            image_paths.append((img_path, matrix_class.name))

    return jsonify(success=True, image_paths=image_paths)

@app.route('/classify_imgs', methods=['POST'])
def classify_imgs():
    global matrix_classes
    data = request.json
    num_images = data['num_images']
    img_paths = []
    if not matrix_classes:
        return jsonify(success=False, message="Matrix classes not set"), 400

    try:
        predictions, confidence = matrix_classes.classify_dirs('imgs/mnist', num_images)
        wrong_classification = matrix_classes.wrong_classification
        for img_name in wrong_classification:
            img_path = 'imgs/mnist/' + wrong_classification[img_name][1] + '/' + img_name
            img_paths.append((img_path, wrong_classification[img_name][0]))
        return jsonify(success=True, 
                       predictions=predictions,  
                       confidence=confidence,
                       wrong_classification=wrong_classification,
                       img_paths=img_paths)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route('/imgs/mnist/<path:filename>')
def serve_images(filename):
    return send_from_directory('imgs/mnist', filename)

if __name__ == '__main__':
    app.run(debug=True)