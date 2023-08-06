import cv2
from skimage.metrics import structural_similarity
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import logging


def ssim(image1,image2):
    baseline = cv2.imread(image1)
    baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
    second = cv2.imread(image2)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)
    score2, diff2 = structural_similarity(baseline_gray, second_gray, full=True)
    return score2

def dvsim(image1,image2,model=None):
    if model==None:
        model = SentenceTransformer('clip-ViT-B-32')
    # Load the OpenAI CLIP Model

    # Next we compute the embeddings
    # To encode an image, you can use the following code:
    # from PIL import Image
    # encoded_image = model.encode(Image.open(filepath))
    image_names = [image1,image2]
   #  print(image_names)
    # print("Images:", len(image_names))
    encoded_image = model.encode([Image.open(filepath) for filepath in image_names], batch_size=128,
                                 convert_to_tensor=True, show_progress_bar=True)

    # Now we run the clustering algorithm. This function compares images aganist
    # all other images and returns a list with the pairs that have the highest
    # cosine similarity score
    processed_images = util.paraphrase_mining_embeddings(encoded_image)
    NUM_SIMILAR_IMAGES = 10

    # =================
    # DUPLICATES
    # =================
    # print('Finding duplicate images...')
    # Filter list for duplicates. Results are triplets (score, image_id1, image_id2) and is scorted in decreasing order
    # A duplicate image will have a score of 1.00
    # It may be 0.9999 due to lossy image compression (.jpg)
    # duplicates = [image for image in processed_images if image[0] >= 0.9999999]
    duplicates = processed_images
    # print(duplicates)
    # Output the top X duplicate images
    for score, image_id1, image_id2 in duplicates[0:NUM_SIMILAR_IMAGES]:
        # print("\nScore: {:.3f}%".format(score * 100))
        # print(image_names[image_id1])
        # print(image_names[image_id2])
        return score
