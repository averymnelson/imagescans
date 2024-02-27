import os
import re
import shutil
import time
import cv2
import pytesseract
from PIL import Image
import pillow_heif
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pre_processing(image):
    """convert image to greyscale and threshold it so tesseract can detect strings better

    Parameters:
    image (jpg): regular color image

    Returns:
    png: image converted to greyscale and thresholded

   """

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite('thresholded.png', threshold_img)
    cv2.imshow('threshold image', threshold_img)
    cv2.destroyAllWindows()
    return threshold_img

def parse_text(pro_image):
    """parse image created by pre_processing function to return strings detected in a list

    Parameters:
    pro_img (png): greyscaled and thresholded png image

    Returns:
    list: data detected in image

   """

    d = pytesseract.image_to_data(pro_image, output_type=pytesseract.Output.DICT)
    return d

def format_text(details):
    """format and clean text found in parse_text

    Parameters:
    details (list): text located in thresholded image

    Returns:
    list: cleaned data detected in image

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

def findsku(formatted, errors, title, form):
    """parse formatted text to find anything containing particular sku characters

    Parameters:
    formatted (list): data returned by format_text that contains data found in image
    errors (list): list for failures
    title (jpg): current image
    form (string): characters the sku should contain

    Returns:
    string: string found in label that is estimated to be the sku

   """

    res = []
    sku = None
    for s in formatted:
        for t in s:
            if re.search(form, t):
                res.append(t)
    res = sorted(res, reverse=True)
    if not res:            
        errors.append(title)
    else:
        sku = res[0]
    return sku

def cleanup(test_str):
    """remove special characters from text found in findsku function

    Parameters:
    test_str (string): estimated sku returned by findsku

    Returns:
    string: estimated sku without particular special characters

   """

    res = None
    bad_char = [';', ':', '!', "*", " "]
    temp = ''
    for i in bad_char:
        temp += i
    if temp:
        res = re.sub(rf'[{temp}]', '', test_str)
    return res

def renaming(sku, img, dest):
    """rename jpg and move to folder

    Parameters:
    sku (string): cleaned sku to be the new name of the jpg file
    img (jpg): original image
    dest (string): destination path

    Returns:
    None

   """

    file_extension = '.jpg'
    new_sku = sku + file_extension
    source_path = os.path.join(os.getcwd(), img)
    destination_path = os.path.join(dest, new_sku)
    shutil.move(source_path, destination_path)

def createdirectories():
    """create folders for errors and renamed to be moved to

    Parameters:
    None

    Returns:
    list: paths to errors folder and renamed folder

   """

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
    """move all items in errors list to errors directory

    Parameters:
    errors (list): list of errors added to by other functions
    paths (list): error and renamed folder paths

    Returns:
    None

   """

    for img in errors:
        source_path = os.path.join(os.getcwd(), img)
        destination_path = os.path.join(paths[1], img)
        shutil.move(source_path, destination_path)

def runimg(curr, paths, errors, form):
    """full function for parsing one image

    Parameters:
    curr (jpg): image being processed
    paths (list): paths for error and renamed folders
    errors (list): list containing detected failures
    form (string): starting letters for sku

    Returns:
    None

   """

    image = cv2.imread(curr)
    thresholds_image = pre_processing(image)
    parsed = parse_text(thresholds_image)
    if parsed:
        formats = format_text(parsed)
        formatted = [ele for ele in formats if ele != []]
        print("Text found: ", formatted)
        if formatted:
            print("\n")
            choices = findsku(formatted, errors, curr, form)
            if choices:
                attempt = cleanup(choices)
                print("SKU found: ", attempt)
                if attempt:
                    renaming(attempt, curr, paths[0])
        else: 
            errors.append(curr) 
    else: 
            errors.append(curr) 
#create docstrings
    def documentation(self):
        f = open("docstrings.txt", "a")
        f.write(time.strftime("%Y%m%d"))
        f.write(pre_processing.__doc__)
        f.write(parse_text.__doc__)
        f.write(format_text.__doc__)
        f.write(findsku.__doc__)
        f.write(cleanup.__doc__)
        f.write(renaming.__doc__)
        f.write(createdirectories.__doc__)
        f.write(mverrors.__doc__)
        f.write(runimg.__doc__)
        f.close()
# change format for heic photos, then for all jpg in current directory, run parsing function
if __name__ == "__main__":
    errors = []
    paths = []
    paths = createdirectories()
    directory = os.getcwd()
    files = [f for f in os.listdir(directory) if f.endswith('.heic') or f.endswith('.HEIC')]
    for filename in files:
        filen = filename.split('.')
        heif_file = pillow_heif.read_heif(os.path.join(directory, filename))
        image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw",)
        image.save(f"{(filen)[0]}.jpg", format("JPEG"))
        os.remove(filename)
    form = input("What character sequence should the SKU start with?\n")
    for images in os.listdir(os.getcwd()):
        if (images.endswith(".jpg") or images.endswith(".JPG") or images.endswith(".JPEG") or images.endswith(".jpeg")):
            curr = images
            runimg(curr, paths, errors, form)
    mverrors(errors, paths)