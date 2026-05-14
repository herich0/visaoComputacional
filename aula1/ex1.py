import cv2
import sys

img_l = cv2.imread('esquerda.png', cv2.IMREAD_GRAYSCALE)
img_r = cv2.imread('direita.png', cv2.IMREAD_GRAYSCALE)

if img_l is None or img_r is None:
    print("Erro ao carregar as imagens. Verifique o caminho.")
    sys.exit()

bm = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disp_bm = bm.compute(img_l, img_r)

disp_bm_vis = cv2.normalize(disp_bm, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
cv2.imwrite('resultado_bm.png', disp_bm_vis)

sgbm = cv2.StereoSGBM_create(minDisparity=0, numDisparities=16, blockSize=3)
disp_sgbm = sgbm.compute(img_l, img_r)

disp_sgbm_vis = cv2.normalize(disp_sgbm, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
cv2.imwrite('resultado_sgbm.png', disp_sgbm_vis)