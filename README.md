# imagescans

This program scans jpgs in the current directory to locate strings within, and if one appears to match the format required of a given SKU, renames and moves the image. 
This program utilizes pytesseract, the python edition of tesseract, an industry standard optical character recognition engine. It also uses openCV and pillow_heif to handle images and convert High Efficiency Image File Format images to jpg files respectively. 
One challenge with the project was handling the heic/heif conversion. The leading method is the package pyheif, which is not available on windows. To develop a program that will work across operating systems, a different package had to be used. 

Installation Instructions
Python: Make sure you have Python installed on your system. You can download Python from the official [Python website](https://www.python.org/downloads/). This code is compatible with Python 3.x versions, preferably Python 3.6 or later.

Tesseract OCR: This code uses Tesseract OCR for text recognition. Install Tesseract OCR by following the instructions provided on the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract). Make sure to add Tesseract to your system PATH during installation.

Python Libraries: Install the required Python libraries using pip. Open a terminal or command prompt and run the following command:

pip install opencv-python pytesseract pillow pillow-heif

Usage Instructions
After installing the dependencies, you can run the script. Here's how to use it:

Place your image files (JPEG, JPG, or HEIC) in the same directory as the script.

Run the script using Python:

python image.py
Follow the prompts provided by the script. Enter the starting character sequence for the SKU when prompted.

The script will process the images, extract text, and attempt to find SKUs based on the provided character sequence. Renamed images will be moved to a "renamed" folder, and images with errors will be moved to an "errors" folder.

Check the "renamed" folder for successfully renamed images and the "errors" folder for any images that couldn't be processed. The renamed folder should be checked to ensure no characters were missed.

Notes
Make sure your images have clear text that can be recognized by Tesseract OCR. Please see the image instructions. 
Ensure that Tesseract OCR is correctly configured and its executable path (tesseract_cmd) is set appropriately in the script.

Credits
The GitHub project can be found at https://github.com/averymnelson/imagescans. Please let me know at averynelson2021@gmail.com if you find any issues or have difficulty with the program. 