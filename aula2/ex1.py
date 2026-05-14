import cv2

def criar_panorama(caminho_img1, caminho_img2, caminho_saida):
    img1 = cv2.imread(caminho_img1)
    img2 = cv2.imread(caminho_img2)

    stitcher = cv2.Stitcher_create()
    status, panorama = stitcher.stitch([img1, img2])

    if status == cv2.Stitcher_OK:
        cv2.imwrite(caminho_saida, panorama)
        print("Panorama salvo em:", caminho_saida)
    else:
        print("Falha ao criar o panorama. Erro:", status)

criar_panorama('img1.jpeg', 'img2.jpeg', 'panorama.jpg')