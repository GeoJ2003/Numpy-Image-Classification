import time
import concurrent.futures
import threading
import numpy as np
import imageutils as img
import os

class MC_list:
    matrix_classes = []
    excluded_dirs_list = []
    confidence_list = np.array([])
    img_classification = {}
    wrong_classification = {}

    def __init__(self, dir_path, num_images=0, excluded_dirs_list=[], threshold=0.01, width=100, height=100):
        start_time = time.time()  # Start time
        self.excluded_dirs_list = excluded_dirs_list
        self.matrix_classes = self.mc_list(dir_path, num_images, threshold, width, height)
        for matrix_class in self.matrix_classes:
            print(f"Matrix class {matrix_class.name} created with {len(matrix_class.imgs_dict)} images.")
        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Time taken creation of subspaces: {elapsed_time:.2f} seconds")

    def classify_img(self, img_path):
        proj_dict = {}
        projections = []
        img_name = os.path.basename(img_path)
        lock = threading.Lock()

        def project_onto_subspace(matrix_class):
            projection = matrix_class.proj_img_onto_subspace(img_path)
            with lock:
                proj_dict[matrix_class.name] = projection
                projections.append(projection)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(project_onto_subspace, matrix_class) for matrix_class in self.matrix_classes]
            concurrent.futures.wait(futures)

        classification = max(proj_dict, key=proj_dict.get)
        confidence = np.mean(projections / np.max(projections)) * 100

        # print(f"Image {img_path} classified as {classification} with {np.max(projections).round(1)}% accuracy and {confidence}% confidence.")
        self.img_classification[img_name] = [classification, os.path.basename(os.path.dirname(img_path))] # [classified, actual]
        self.confidence_list = np.append(self.confidence_list, confidence)

    def classify_dir(self, dir_path, num_images=0):
        # The # of images we want to classify
        count = 0
        lock = threading.Lock()

        def classify_file(file):
            nonlocal count
            img_path = os.path.join(dir_path, file)
            img_name = os.path.basename(os.path.abspath(img_path))
            if os.path.isfile(img_path):
                with lock:
                    if num_images and count >= num_images:
                        return
                    if any(img_name in matrix_class.imgs_dict for matrix_class in self.matrix_classes):
                        return
                    count += 1
                self.classify_img(img_path)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(classify_file, file) for file in os.listdir(dir_path)]
            concurrent.futures.wait(futures)
    
    def classify_dirs(self, dir_path, num_images=0):
        self.confidence_list = np.array([])
        self.img_classification = {}
        self.wrong_classification = {}
        start_time = time.time()  # Start time
        correct = 0
        incorrect = 0
        lock = threading.Lock()

        def classify_single_dir(dir):
            if os.path.basename(dir) not in self.excluded_dirs_list:
                self.classify_dir(os.path.join(dir_path, dir), num_images)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(classify_single_dir, dir) for dir in os.listdir(dir_path)]
            concurrent.futures.wait(futures)

        # Check if each image was classified correctly
        with lock:
            for img_name, classification in self.img_classification.items():
                if classification[0] == classification[1]:
                    correct += 1
                else:
                    self.wrong_classification[img_name] = classification
                    incorrect += 1

        total = correct + incorrect
        perCorrect = round(correct/total * 100, 1)
        perIncorrect = round(incorrect/total * 100, 1)
        confidence = np.mean(self.confidence_list).round(1)

        print(f"{correct}/{total} ({perCorrect}%) images were correctly classified with {confidence}% confidence.")
        print(f"{incorrect}/{total} ({perIncorrect}%) images were incorrectly classified.")
        print(f"Wrong classifications: {self.wrong_classification}")

        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Time taken for classification: {elapsed_time:.2f} seconds")

        return [correct, incorrect], confidence
    
    def mc_list(self, dir_path, num_images=0, threshold=0.01, width=100, height=100):
        self.matrix_classes = []
        lock = threading.Lock()

        def create_matrix_class(dir):
            if os.path.basename(dir) not in self.excluded_dirs_list:
                matrix_class = MatrixClass(os.path.join(dir_path, dir), num_images, threshold, width, height)
                with lock:
                    self.matrix_classes.append(matrix_class)
                return matrix_class
            return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(create_matrix_class, dir) for dir in os.listdir(dir_path)]
            concurrent.futures.wait(futures)

        return self.matrix_classes

class MatrixClass:
    name = ""
    width = 100
    height = 100
    imgs_dict = {}
    combined_images = np.array([])
    embedding_matrix = np.array([[]])
    U = np.array([[]])

    def __init__(self, dir, num_images=0, threshold=0.01, width=100, height=100):
        self.name = os.path.basename(dir)
        self.width = width
        self.height = height
        self.imgs_dict = img.load_images(dir, width, height, num_images)
        self.combined_images = img.combine_images(self.imgs_dict)
        self.create_embedding_matrix(threshold)
    
    def create_embedding_matrix(self, threshold=0.01):
        U, S, VT = np.linalg.svd(self.combined_images, full_matrices=False)
        minimum = threshold * np.max(S)
        # Find significant eigenvectors
        index = np.sum(S > minimum)
        # This will be our "A" matrix to find the embedding matrix
        self.U = U[:, :index]
        temp_matrix = np.dot(self.U.T, self.U)
        pseudoInverse = np.dot(np.linalg.inv(temp_matrix), self.U.T)
        # Using np.lingalg.pinv(self.U) would be the same as the above two lines
        self.embedding_matrix = np.dot(self.U, pseudoInverse)  # A * [[A^T * A]^-1 * A^T]
    
    def proj_img_onto_subspace(self, img_path):
        if not os.path.exists(img_path):
            print(f"File {img_path} does not exist.")
            return

        vectorized_img = img.load_and_vectorize(img_path, self.width, self.height)

        # Project the image onto the subspace
        magnitude = np.dot(self.embedding_matrix, vectorized_img)

        max_magnitude = np.max(np.linalg.norm(magnitude))

        return max_magnitude