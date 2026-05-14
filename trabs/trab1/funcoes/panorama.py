import cv2
import numpy as np
import time

def gerar_panoramica(caminho_img1, caminho_img2, detector_tipo, matcher_tipo):
    inicio = time.time()

    img1 = cv2.imread(caminho_img1)
    img2 = cv2.imread(caminho_img2)

    if img1 is None or img2 is None:
        raise ValueError("Erro ao carregar as imagens.")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    if detector_tipo == 'ORB':
        detector = cv2.ORB_create()
    elif detector_tipo == 'SIFT':
        detector = cv2.SIFT_create()
    else:
        raise ValueError("Detector inválido.")

    kp1, des1 = detector.detectAndCompute(gray1, None)
    kp2, des2 = detector.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        raise ValueError("Não foi possível extrair descritores.")

    if detector_tipo == 'SIFT':
        des1 = np.float32(des1)
        des2 = np.float32(des2)

    good_matches = []

    if matcher_tipo == 'BF':
        if detector_tipo == 'ORB':
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            good_matches = sorted(matches, key=lambda x: x.distance)[:50]
        else:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)

    elif matcher_tipo == 'FLANN':
        if detector_tipo == 'ORB':
            index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1)
            search_params = dict(checks=50)
        else:
            index_params = dict(algorithm=1, trees=5)
            search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        for match in matches:
            if len(match) == 2:
                m, n = match
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)

    if len(good_matches) >= 4:
        src_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        cantos_img1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
        cantos_img2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
        cantos_img2_transformados = cv2.perspectiveTransform(cantos_img2, H)

        todos_cantos = np.concatenate((cantos_img1, cantos_img2_transformados), axis=0)

        [xmin, ymin] = np.int32(todos_cantos.min(axis=0).ravel() - 0.5)
        [xmax, ymax] = np.int32(todos_cantos.max(axis=0).ravel() + 0.5)

        t = [-xmin, -ymin]
        Ht = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])

        resultado = cv2.warpPerspective(img2, Ht.dot(H), (xmax - xmin, ymax - ymin))

        resultado[t[1]:h1+t[1], t[0]:w1+t[0]] = img1

        gray_res = cv2.cvtColor(resultado, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_res, 1, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contornos:
            x, y, w, h = cv2.boundingRect(contornos[0])
            resultado = resultado[y:y+h, x:x+w]

        fim = time.time()
        tempo_proc = fim - inicio

        return resultado, tempo_proc
    else:
        raise ValueError(f"Apenas {len(good_matches)} correspondências encontradas (mínimo 4).")