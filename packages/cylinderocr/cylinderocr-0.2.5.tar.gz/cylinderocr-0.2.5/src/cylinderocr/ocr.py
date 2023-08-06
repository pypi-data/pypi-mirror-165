from getmac import get_mac_address as gma
from cv2 import dnn_superres
from statistics import mode
import numpy as np
import warnings
import cv2
import re
warnings.filterwarnings("ignore")

def predark(img):
    im_nr = cv2.detailEnhance(img, sigma_s=10, sigma_r=1)
    im_nr = cv2.fastNlMeansDenoisingColored(im_nr, None, 3,3, 7, 20)
    return im_nr 

def upsacale(image,cvdnn_path):

# Create an SR object
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(cvdnn_path)
    sr.setModel("fsrcnn", 3)
    result = sr.upsample(image)
    return result

def inference(img_path,ocr,cvdnn_path):
    try:
        macadd=gma()
        uniqueadd =["60:e3:2b:34:66:ce","a8:7e:ea:41:ad:34","1c:69:7a:ae:44:32"]
        if macadd in uniqueadd:
            print("Configured Sucessfully")
            image= cv2.imread(img_path)
            img_path=upsacale(image,cvdnn_path)
            img_path=predark(img_path)
            result = ocr.ocr(img_path, cls=True)
            txts = [line[1][0] for line in result]
            scores = [line[1][1] for line in result]
            if len(txts)==0:          #no object detected
                return "-1",float(0.0)  #object not found
            try: 
                regex = '^[+-]?[0-9]+\.[0-9]$'
                for i in range(0,len(txts)):# most repeating txts
                    if(re.search(regex, txts[i])): 
                            if float(txts[i]) > 20.0 or float(txts[i]) <= 15.0:
                                txts.pop(i)
                                scores.pop(i)
                            else:
                                pass
                                              
                    else:
                        txts.pop(i)
                        scores.pop(i)
                if len(txts)==0:
                   return "-2",float(0.0) 
                txts=[mode(txts)]
                scores=[max(scores)]
            except:
                pass    
            if len(txts)>1:           # if both txts are different
                case=np.argmax(scores)
                scores=[scores[case]]
                txts=[txts[case]]
            if(re.search(regex, txts[0])):
                    return str(txts[0]),float(scores[0])
            else:
                    return "-2",float(0.0)
        else:
            return "-3",float(0.0)  #could not configured
    except Exception as E:
        return "-4",float(0.0) # could not process,Exception

'''if __name__ == "__main__":
    txts,scores=inference("img2.jpg","en")
    print(txts," ",type(txts)," ",scores," ",type(scores))'''
    

