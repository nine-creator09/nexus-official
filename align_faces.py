import cv2
import glob
from PIL import Image
import os

files = glob.glob('images/*.jpg')
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

OUT_W, OUT_H = 1200, 1600
FACE_TARGET_W = 400
TARGET_CX = OUT_W // 2
TARGET_CY = 500

for filename in files:
    img = cv2.imread(filename)
    if img is None: continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(100, 100))
    
    if len(faces) == 0:
        print(f"No face found in {filename}, falling back to center crop.")
        # fallback: assume face is at top center
        fw = img.shape[1] // 3
        cx = img.shape[1] // 2
        cy = img.shape[0] // 3
    else:
        # take largest face
        faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
        x, y, fw, fh = faces[0]
        cx = x + fw // 2
        cy = y + fh // 2
        
    scale = FACE_TARGET_W / fw
    new_img_w = int(img.shape[1] * scale)
    new_img_h = int(img.shape[0] * scale)
    
    resized = cv2.resize(img, (new_img_w, new_img_h), interpolation=cv2.INTER_LANCZOS4)
    new_cx = int(cx * scale)
    new_cy = int(cy * scale)
    
    # We want new_cx to be mapped to TARGET_CX
    # We want new_cy to be mapped to TARGET_CY
    left = new_cx - TARGET_CX
    top = new_cy - TARGET_CY
    
    # We create out canvas using PIL to handle boundary padding easily (it pads black if negative)
    pil_img = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    # crop can take negative coordinates and > width coordinates in PIL, it pads!
    pil_cropped = pil_img.crop((left, top, left + OUT_W, top + OUT_H))
    
    # Cache busted name shouldn't change here since index.html expects these exact names
    pil_cropped.save(filename, quality=95)
    print(f"Successfully aligned and saved {filename}")

