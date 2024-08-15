import numpy as np
import imageutils as img
import os

class MC_list:
    matrix_classes = []
    excluded_dirs_list = []
    confidence_list = np.array([])
    img_classification = {}

    def __init__(self, dir_path, num_images=0, excluded_dirs_list=[], threshold=0.01, width=100, height=100):
        self.excluded_dirs_list = excluded_dirs_list
        self.matrix_classes = self.mc_list(dir_path, num_images, threshold, width, height)
        for matrix_class in self.matrix_classes:
            print(f"Matrix class {matrix_class.name} created with {matrix_class.img_count} images.")

    def classify_img(self, img_path):
        sim_dict = {}
        similarities = np.array([])
        img_name = os.path.basename(img_path)

        for matrix_class in self.matrix_classes:
            similarity = matrix_class.proj_img_onto_subspace(img_path)
            sim_dict[matrix_class.name] = similarity
            similarities = np.append(similarities, similarity)

        classification = max(sim_dict, key=sim_dict.get)
        similarities = similarities * 100
        confidence = np.mean(similarities).round(1)

        # print(f"Image {img_path} classified as {classification} with {np.max(similarities).round(1)}% accuracy and {confidence}% confidence.")
        self.img_classification[img_name] = classification
        self.confidence_list = np.append(self.confidence_list, confidence)

    def classify_dir(self, dir_path, num_images=0):
        # The # of images we want to classify
        count = 0

        for file in os.listdir(dir_path):
            img_path = os.path.join(dir_path, file)
            img_name = os.path.basename(os.path.abspath(img_path))
            if os.path.isfile(img_path):
                if num_images and count >= num_images:
                    break
                # Check if the image is in any matrix class dictionary
                if any(img_name in matrix_class.imgs_dict for matrix_class in self.matrix_classes):
                    # print(f"Skipping {img_name} as it is already in a matrix class dictionary.")
                    continue
                self.classify_img(img_path)
                count += 1
    
    def classify_dirs(self, dir_path, num_images=0):
        self.confidence_list = np.array([])
        self.img_classification = {}
        correct = 0
        incorrect = 0

        for dir in os.listdir(dir_path):
            if os.path.basename(dir) not in self.excluded_dirs_list:
                self.classify_dir(os.path.join(dir_path, dir), num_images)

        # Check if each image was classified correctly
        for img_name, classification in self.img_classification.items():
            classified_dir = os.path.join(dir_path, classification)
            img_path = os.path.join(classified_dir, img_name)
            if os.path.exists(img_path):
                correct += 1
            else:
                incorrect += 1

        total = correct + incorrect
        perCorrect = round(correct/total * 100, 1)
        perIncorrect = round(incorrect/total * 100, 1)
        confidence = np.mean(self.confidence_list).round(1)

        print(f"{correct}/{total} ({perCorrect}%) images were correctly classified with {confidence}% confidence.")
        print(f"{incorrect}/{total} ({perIncorrect}%) images were incorrectly classified.")
        return perCorrect, perIncorrect, confidence
    
    def mc_list(self, dir_path, num_images=0, threshold=0.01, width=100, height=100):
        self.matrix_classes = []
        for dir in os.listdir(dir_path):
            if os.path.basename(dir) not in self.excluded_dirs_list:
                self.matrix_classes.append(MatrixClass(os.path.join(dir_path, dir), num_images, threshold, width, height))
        return self.matrix_classes

class MatrixClass:
    name = ""
    width = 100
    height = 100
    imgs_dict = {}
    img_count = 0
    combined_images = np.array([])
    embedding_matrix = np.array([[]])
    U = np.array([[]])

    def __init__(self, dir, num_images=0, threshold=0.01, width=100, height=100):
        self.name = os.path.basename(dir)
        self.width = width
        self.height = height
        self.imgs_dict, self.img_count = img.load_images(dir, width, height, num_images)
        self.combined_images = img.combine_images(self.imgs_dict)
        self.SVD(threshold)
    
    def SVD(self, threshold=0.01):
        U, S, VT = np.linalg.svd(self.combined_images, full_matrices=False)
        minimum = threshold * np.max(S)
        # Find significant eigenvectors
        index = np.where(S >= minimum)[0]
        # This will be our "A" matrix to find the embedding matrix
        self.U = U[:, index]
        temp_matrix = np.dot(self.U.T, self.U)
        pseudoInverse = np.dot(np.linalg.inv(temp_matrix), self.U.T)
        # Using np.lingalg.pinv(self.U) would be the same as the above two lines
        self.embedding_matrix = np.dot(self.U, pseudoInverse)  # A * [[A^T * A]^-1 * A^T]

        # Normalize embedding matrix
        norms = np.linalg.norm(self.embedding_matrix, axis=0)
        norms[norms == 0] = 1  # Avoid division by zero
        self.embedding_matrix = self.embedding_matrix / norms
    
    def proj_img_onto_subspace(self, img_path):
        if not os.path.exists(img_path):
            print(f"File {img_path} does not exist.")
            return

        vectorized_img_normalized = img.load_and_vectorize(img_path, self.width, self.height)

        # Compute the cosine similarities
        cosine_similarities = np.dot(self.embedding_matrix.T, vectorized_img_normalized)

        max_cosine_similarity = np.max(cosine_similarities).round(3)

        return max_cosine_similarity