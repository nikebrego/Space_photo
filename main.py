import cv2
import overpass
# Координаты углов снимка в пикселях
k1 = 1363, 12
k2 = 7623, 990
k3 = 49, 6029
k4 = 6311, 7010
# Погрешность вычисления, вводится для более точного определения города
E = -750, 600

def reading(word):   # Функция считывает из файла MTL данные для вычисления
    inp = open('LE07_L1TP_015042_20020602_20160929_01_T1_MTL.txt').readlines()
    for i in iter(inp):
        if word in i:
            original = i[4:]
            return float(original.replace(word + " = ", ""))
def get_point(p1,p2,coeff):     #Функция для определения координаты M
    l = coeff / (1 - coeff) 
    if coeff>0.5:
        l = 1/l
        xm = int((p2[0] + l * p1[0]) / (1 + l))
        ym = int((p2[1] + l * p1[1]) / (1 + l))
        M = xm, ym
        return M
    else:
        xm = int((p1[0] + l * p2[0]) / (1 + l))
        ym = int((p1[1] + l * p2[1]) / (1 + l))
        M = xm,ym
        return M
def show_result(result):
    #Функция выводит изображение
    cv2.namedWindow('Miami', cv2.WINDOW_NORMAL)
    cv2.imshow('Miami', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def make(POINT):
    # Посылаем функции чтения задачу, считать необходимые данные
    CORNER_UL = reading('CORNER_UL_LAT_PRODUCT'), reading('CORNER_UL_LON_PRODUCT')
    CORNER_UR = reading('CORNER_UR_LAT_PRODUCT'), reading('CORNER_UR_LON_PRODUCT')
    CORNER_LL = reading('CORNER_LL_LAT_PRODUCT'), reading('CORNER_LL_LON_PRODUCT')
    CORNER_LR = reading('CORNER_LR_LAT_PRODUCT'), reading('CORNER_LR_LON_PRODUCT')
    delta_lat = (CORNER_UL[0] + CORNER_UR[0]) / 2 - (CORNER_LL[0] + CORNER_LR[0]) / 2
    delta_lon = abs((CORNER_UL[1] + CORNER_LL[1]) / 2 - (CORNER_UR[1] + CORNER_LR[1]) / 2)
    kx = (abs((CORNER_UL[1] + CORNER_LL[1]) / 2) - abs(POINT[1])) / delta_lon
    ky = (POINT[0] - (CORNER_LL[0] + CORNER_LR[0]) / 2) / delta_lat
    m1 = get_point(k1, k2, kx)
    m2 = get_point(k4, k1, ky)
    img = cv2.imread("LE07_L1TP_015042_20020602_20160929_01_T1_B1.tif")
    img = cv2.circle(img, (m1[0] + E[0], m2[1] + E[1]), 800, (250, 0, 0), thickness=20)
    show_result(img)
City_K = 26.2417, -80.1419
make(City_K)
