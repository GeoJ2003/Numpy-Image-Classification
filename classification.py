from flask import Flask, render_template_string
import numpy as np
import imageutils as img

# Finds the cosine similarity between each pair of vectors in the matrix
# Each column in the matrix represents a vector (image)
def cosine_similarity(matrix):
    # Normalize the columns (vectors)
    d = np.linalg.norm(matrix, axis=0)
    matrix_normalized = matrix / d
    
    # Compute the cosine similarity
    similarity = np.dot(matrix_normalized.T, matrix_normalized)
    
    # Ensure the diagonal is exactly 1
    np.fill_diagonal(similarity, 1)
    
    return similarity

# Finds the cosine similarities between all vectorized images in the images_dict
def find_image_cosine_similarities(images_dict):
    # Combine images into a matrix where each column is a vectorized image
    combined_matrix = img.combine_images(images_dict)
    
    # Calculate cosine similarities
    similarities = cosine_similarity(combined_matrix)
    
    return similarities

# Serves an HTML table showing the cosine similarity comparisons on a local web server
def serve_similarity_table(images_dict, similarities):
    """
    Serve an HTML table showing the cosine similarity comparisons on a local web server.
    
    :param images_dict: Dictionary of images used in find_image_cosine_similarities.
    :param similarities: 2D NumPy array of cosine similarities from find_image_cosine_similarities.
    """
    # Extract image identifiers
    image_ids = list(images_dict.keys())
    
    # Start the HTML table
    html = "<style>td, th {font-weight: normal;}</style>"
    html += "<table border='1'><tr><th></th>"
    
    # Header row for image identifiers
    for id in image_ids:
        html += f"<th>{id}</th>"
    html += "</tr>"
    
    # Rows for cosine similarities
    for i, row_id in enumerate(image_ids):
        html += f"<tr><td>{row_id}</td>"
        for j in range(len(image_ids)):
            html += f"<td>{similarities[i, j]:.2f}</td>"
        html += "</tr>"
    
    html += "</table>"
    
    # Flask app
    app = Flask(__name__)
    
    @app.route('/')
    def display_table():
        return render_template_string(html)
    
    # Run the Flask app
    app.run(debug=True, use_reloader=False)  # use_reloader=False to prevent running the script twice

# Example usage
if __name__ == '__main__':
    # Mock data for demonstration
    images_dict = {'Image1': None, 'Image2': None}
    similarities = np.array([[1, 0.8], [0.8, 1]])
    
    serve_similarity_table(images_dict, similarities)