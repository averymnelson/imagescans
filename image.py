import os
import re
import shutil
import time
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pre_processing(image):
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
    # img = cv2.imread(pro_image)
    d = pytesseract.image_to_data(pro_image, output_type=pytesseract.Output.DICT)
    print(d.keys())
    return d
    # text = str(pytesseract.image_to_string(img))
    # print(text)

def format_text(details):
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

def findsku(formatted, errors, title):
    res = []
    for s in formatted:
        for t in s:
            if re.search('GP', t):
                res.append(t)
    if not res or len(res)>1:            
        errors.append(title)
    sku = res[0]
    return sku

def cleanup(test_str):
    bad_char = [';', ':', '!', "*", " "]
    temp = ''
    for i in bad_char:
        temp += i
    res = re.sub(rf'[{temp}]', '', test_str)
    return res

def renaming(sku, img, dest):
    # split_tup = os.path.splitext(img)
    # print(split_tup)
    # file_name = split_tup[0]
    file_extension = '.jpg'
    # file_extension = split_tup[1]
    new_sku = sku + file_extension
    source_path = os.path.join(os.getcwd(), img)
    destination_path = os.path.join(dest, new_sku)
    
    # Move the file to the destination directory and rename it
    shutil.move(source_path, destination_path)

def createdirectories():
    timestr = time.strftime("%Y%m%d")
    path = './renamed_'
    path1 = path+timestr
    if not os.path.exists(path1):
        os.mkdir(path1)
    path = './errors_'
    path2=path+timestr
    if not os.path.exists(path2):
        os.mkdir(path2)
    paths = []
    paths.append(path1)
    paths.append(path2)
    return paths

def mverrors(errors, paths):
    for img in errors:
        source_path = os.path.join(os.getcwd(), img)
        destination_path = os.path.join(paths[1], img)
        shutil.move(source_path, destination_path)

def runimg(curr, paths, errors):
    image = cv2.imread(curr)
    # calling pre_processing function to perform pre-processing on input image.
    thresholds_image = pre_processing(image)
    parsed = parse_text(thresholds_image)
    print("\n\n")
    formats = format_text(parsed)
    formatted = [ele for ele in formats if ele != []]
    print(formatted)
    if formatted:
        print("\n\n")
        choices = findsku(formatted, errors, curr)
        print(choices)
        attempt = cleanup(choices)
        print("\n\n")
        print(attempt)
        renaming(attempt, curr, paths[0])
    else: 
        errors.append(curr) 

if __name__ == "__main__":
    # reading image from local
    errors = []
    paths = []
    paths = createdirectories()
    for images in os.listdir(os.getcwd()):
        if (images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".heic") or images.endswith(".HEIC")):
            curr = images
            runimg(curr, paths, errors)
    mverrors(errors, paths)