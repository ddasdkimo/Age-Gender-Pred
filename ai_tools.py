from age_pred_model import AgePredModel
import torch
import torch.nn as nn
import torch.optim as optim
import cv2


class AiTools:

    model = None

    def eval_single(self, img):
        if type(img) == str:
            img = cv2.imread(img)

        if not self.model:
            self.model = AgePredModel(eval_use_only=True)
        int2gender = {0: 'Female', 1: 'Male'}

        # input image
        preds, rects, scores = self.model.getAgeGender(img,
                                                       transformed=False,
                                                       return_all_faces=True,
                                                       return_info=True)
        gen_pred_arr = []
        age_pred_arr = []
        point_arr = []
        gen_pred, age_pred = -1, -1
        for pred, (x, y, w, h), score in zip(preds, rects, scores):
            # model predictions
            gen_pred, gen_prob, age_pred, age_var = pred
            age_pred, gen_pred = float(age_pred), int(gen_pred)
            age_var, gen_prob = int(age_var), float(gen_prob)
            # vars

            color = (255, 0, 0) if gen_pred == 1 else (0, 0, 255)
            fontscale = min(1.5, max(0.3, max(w, h) / 500))
            fill_h = int(35 * fontscale)
            font_h = int(6 * fontscale)
            thickness = 1 if fontscale <= 1 else 2

            # draw a rectange to bound the face
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 4)
            point_arr.append({
                "xmax": x,
                "xmin": x + w,
                "ymax": y,
                "ymin": y + h
            })
            # fill an area with color for text show
            cv2.rectangle(img, (x, y + h - fill_h),
                          (x + w, y + h), color, cv2.FILLED)

            # put text
            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(img,
                        "{:.0f}% {}, {:.0f} +/- {}".format(100 * gen_prob,
                                                           int2gender[gen_pred],
                                                           age_pred,
                                                           age_var),
                        org=(x + 6, y + h - font_h),
                        fontFace=font,
                        fontScale=fontscale,
                        color=(255, 255, 255),
                        thickness=thickness)
            gen_pred_arr.append(gen_pred)
            age_pred_arr.append(age_pred)
        return img, gen_pred_arr, age_pred_arr, point_arr

    def eval_live(self):
        # 使用鏡頭測試
        cap = cv2.VideoCapture(0)
        self.model = AgePredModel(eval_use_only=True)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            labeled, _, _ = eval_single(frame, self.model)

            # Display the resulting frame
            cv2.imshow('frame', labeled)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def detect(self, image):
        # 圖片辨識
        labeled, gen_pred, age_pred, point_arr = self.eval_single(image)
        return labeled, gen_pred, age_pred, point_arr
