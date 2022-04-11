import numpy as np
from PIL import Image, ImageOps

def find_u_sigma_v(img_matrix):
    img_matrix_transpose = img_matrix.transpose()
    matrix_product_transpose = img_matrix_transpose @ img_matrix
    
    eigvalues, eigvectors = np.linalg.eig(matrix_product_transpose)
    sorted_eigvalues = np.sort(eigvalues)[::-1]

    eig_val_vec = dict()

    num_of_eigvectors = len(eigvectors)

    for i in range(num_of_eigvectors):
        eigvectors[i] = eigvectors[i] / np.linalg.norm(eigvectors[i])
        eig_val_vec.update({eigvalues[i] : eigvectors[i]})

    small_sigma_values = np.empty((num_of_eigvectors, 0))
    for i in range(num_of_eigvectors):
        if eigvalues[i] >= 0:
            small_sigma_values[i] = eigvalues[i] ** 0.5

    u_matrix, sigma_matrix, vT_matrix = np.linalg.svd(img_matrix)
    u_mat = np.empty((600, 600))
    vT_mat = np.empty((600, 600))
    sigma_matrix = np.diag(sigma_matrix)

    for i in range(num_of_eigvectors):
        if(small_sigma_values[i] != 0):
            u_mat[i] = (img_matrix @ eig_val_vec[sorted_eigvalues[i]]) * (1/small_sigma_values[i])
            vT_mat[i] = eig_val_vec[sorted_eigvalues[i]]

    return u_matrix, sigma_matrix, vT_matrix

img = Image.open('./image.jpg')

img = ImageOps.exif_transpose(img)
img = img.resize((600, 600))
img = img.convert('L')

img_matrix = np.array(img)
u_matrix, sigma_matrix, vT_matrix = find_u_sigma_v(img_matrix)


PRECISION_ARRAY = [1, 10, 25, 50, 100]
for PRECISION in PRECISION_ARRAY:
    compressed_img_matrix = u_matrix[:, 0:PRECISION] @ sigma_matrix[0:PRECISION, 0:PRECISION] @ vT_matrix[0:PRECISION, :]
    compressed_image = Image.fromarray(compressed_img_matrix)
    compressed_image.show()