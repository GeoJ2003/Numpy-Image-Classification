import numpy as np
import imageutils as img
import classification as cls
import os

class MatrixClass:
    name = ""
    width = 100
    height = 100
    imgs_dict = {}
    combined_images = np.array([])
    embedding_matrix = np.array([[]])
    U = np.array([[]])
    S = np.array([])

    def __init__(self, dir, name, width=100, height=100):
        self.name = name
        self.width = width
        self.height = height
        self.imgs_dict = img.load_images(dir, width, height)
        self.combined_images = img.combine_images(self.imgs_dict)
        self.SVD()
    
    def SVD(self, threshold=0.01):
        U, S, VT = np.linalg.svd(self.combined_images, full_matrices=False)
        minimum = threshold * np.max(S)
        # Find significant eigenvectors
        index = np.where(S >= minimum)[0]
        # This will be our "A" matrix to find the embedding matrix
        self.U = U[:, index]
        self.S = S
        self.embedding_matrix = np.dot(self.U, np.linalg.pinv(self.U))  # U*UT
    
    def proj_img_onto_subspace(self, img_path):
        if not os.path.exists(img_path):
            print(f"File {img_path} does not exist.")
            return

        vectorized_img = img.load_and_vectorize(img_path, self.width, self.height)

        # Normalize the columns (vectors) of the embedding matrix
        norms = np.linalg.norm(self.embedding_matrix, axis=0)
        norms[norms == 0] = 1  # Avoid division by zero
        embedding_normalized = self.embedding_matrix / norms

        # Normalize the vectorized image
        vectorized_img_normalized = vectorized_img / np.linalg.norm(vectorized_img)

        # Compute cosine similarities
        cosine_similarities = np.dot(embedding_normalized.T, vectorized_img_normalized)

        # Find the largest cosine similarity
        max_cosine_similarity = np.max(cosine_similarities)

        print(f"Max cosine similarity: {max_cosine_similarity}")
        return max_cosine_similarity