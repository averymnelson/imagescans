# import libraries
import csv
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pre_processing(image):
    """
    This function take one argument as
    input. this function will convert
    input image to binary image
    :param image: image
    :return: thresholded image
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # converting it to binary image
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # saving image to view threshold image
    cv2.imwrite('thresholded.png', threshold_img)

    cv2.imshow('threshold image', threshold_img)
    # Maintain output window until
    # user presses a key
    cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()

    return threshold_img

def parse_text(pro_image):
    img = cv2.imread(pro_image)
    d = pytesseract.image_to_data(pro_image, output_type=pytesseract.Output.DICT)
    print(d.keys())
    return d
    # text = str(pytesseract.image_to_string(img))
    # print(text)

def format_text(details):
    """
    This function take one argument as
    input.This function will arrange
    resulted text into proper format.
    :param details: dictionary
    :return: list
    """
    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == details['text'][-1]):
            parse_text.append(word_list)
            word_list = []

    return parse_text

def findsku(formatted):
    search_key = 'GP'
    res = [val for key, val in formatted.items() if search_key in key]
    return (str(res))

if __name__ == "__main__":
    # reading image from local
    image = cv2.imread('GP00111811.JPG')
    # calling pre_processing function to perform pre-processing on input image.
    thresholds_image = pre_processing(image)
    parsed = parse_text("thresholded.png")
    print("\n\n")
    formatted = format_text(parsed)
    print(formatted)
    print("\n\n")
    choices = findsku(formatted)
    print(choices)