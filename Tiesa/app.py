import os,cv2,pytesseract
from flask import Flask, render_template, request,jsonify,send_file
from PIL import Image
import numpy as np


pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/extract', methods=['POST','GET'])
def upload_file():
    if request.method == "GET":
        return "This is the BLah blah"
    elif request.method == "POST":
        file = request.files['image']

        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
        file.save(f)
        # print(file.filename)

        image = cv2.imread(UPLOAD_FOLDER+"/"+file.filename)
        os.remove(UPLOAD_FOLDER+"/"+file.filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we should apply thresholding to preprocess the
        # image
        preprocess = request.form["preprocess"]
        if  preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


        # make a check to see if median blurring should be done to remove
        # noise



        elif preprocess == "blur":
            gray = cv2.medianBlur(gray, 3)
        elif preprocess == "scale":
            gray=cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        elif preprocess == "skew":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bitwise_not(gray)
 
# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
            thresh = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#grab the (x, y) coordinates of all pixel values that
# are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all
# coordinates
            coords = np.column_stack(np.where(thresh > 0))
            angle = cv2.minAreaRect(coords)[-1]
 
# the `cv2.minAreaRect` function returns values in the
# range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we
# need to add 90 degrees to the angle
            if angle < -45:
                angle = -(90 + angle)
 
# otherwise, just take the inverse of the angle to make
# it positive
            else:
                angle = -angle


# rotate the image to deskew it
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            gray = cv2.warpAffine(gray, M, (w, h),
                flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# draw the correction angle on the image so we can validate it
 
# show the output image
        
            
            
        print(preprocess)
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        cv2.imshow(filename, gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # load the image as a PIL/Pillow image, apply OCR, and then delete
        # the temporary file
        # print("C:/Users/mzm/PycharmProjects/My_website/ocr_using_video/"+filename,Image.open("C:\\Users\mzm\PycharmProjects\My_website\ocr_using_video\\"+filename))
        text = pytesseract.image_to_string(Image.open(filename))
        #os.remove(filename)
        print("Text in Image :\n",text)

        return jsonify({"text" : text})
        

app.run("0.0.0.0",5000,threaded=True,debug=True)


