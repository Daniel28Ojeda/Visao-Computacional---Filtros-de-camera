import cv2
import numpy as np

def aplicar_filtro(frame, filtro):
    if filtro == 'preto_branco':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    elif filtro == 'sepia':
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

    elif filtro == 'negativo':
        return cv2.bitwise_not(frame)

    elif filtro == 'cartoon':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(blur, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        return cv2.bitwise_and(color, color, mask=edges)

    elif filtro == 'desfoque':
        return cv2.GaussianBlur(frame, (15, 15), 0)

    elif filtro == 'brilho':
        return cv2.convertScaleAbs(frame, alpha=1.0, beta=50)

    elif filtro == 'contraste':
        return cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    elif filtro == 'quente':
        increase = np.full(frame.shape, (10, 20, 40), dtype=np.uint8)
        return cv2.add(frame, increase)

    elif filtro == 'frio':
        decrease = np.full(frame.shape, (40, 20, 10), dtype=np.uint8)
        return cv2.subtract(frame, decrease)

    else:
        return frame

def main():
    cap = cv2.VideoCapture(0)
    filtro_atual = 'original'

    print("Pressione:")
    print("  0 - Sem filtro")
    print("  1 - Preto e Branco")
    print("  2 - Sépia")
    print("  3 - Negativo")
    print("  4 - Cartoon")
    print("  5 - Desfoque")
    print("  6 - Brilho")
    print("  7 - Contraste")
    print("  8 - Filtro Quente")
    print("  9 - Filtro Frio")
    print("  q - Sair")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if filtro_atual == 'preto_branco':
            frame = aplicar_filtro(frame, 'preto_branco')
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif filtro_atual != 'original':
            frame = aplicar_filtro(frame, filtro_atual)

        cv2.imshow('Filtro Instagram - OpenCV', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('0'):
            filtro_atual = 'original'
        elif key == ord('1'):
            filtro_atual = 'preto_branco'
        elif key == ord('2'):
            filtro_atual = 'sepia'
        elif key == ord('3'):
            filtro_atual = 'negativo'
        elif key == ord('4'):
            filtro_atual = 'cartoon'
        elif key == ord('5'):
            filtro_atual = 'desfoque'
        elif key == ord('6'):
            filtro_atual = 'brilho'
        elif key == ord('7'):
            filtro_atual = 'contraste'
        elif key == ord('8'):
            filtro_atual = 'quente'
        elif key == ord('9'):
            filtro_atual = 'frio'
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
