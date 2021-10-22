# 미니 포토샵 프로젝트
# 포토샵과 같은 소프트웨어를 '영상처리(Image Processing) 프로그램' 이라 함
# 원칙적으로 영상처리에 대한 이론과 알고리즘을 익힌 후 미니 포토샵 프로그램을 작성하면 좋음
# 현실적으로 이론을 배제하고 화면에 구현되는 것 위주로 진행

# 주의 사항1. 이미지 파일명이나 저장된 경로에 한글이 들어가면 안됨
# 주의 사항2. 이미지 크기는 가로와 세로가 동일해야 함
# 주의 사항3. 처리하는 속도가 다소 오래 걸림

# 사용할 라이브러리 또는 모듈을 임포트


# 윈도우 프로그래밍을 하기 위한 모듈
from tkinter import *

# 파일 입출력을 위한 모듈
from tkinter.filedialog import *

# 숫자나 문자를 입력 받기 위한 모듈
from tkinter.simpledialog import *

# 설치한 이미지 처리 기능을 제공하는 이미지매직의 라이브러리 임포트
# GIF, PNG 뿐 아니라 JPG 같은 이미지를 모두 처리하기 위해 외부 라이브러리 이미지 매직 사용 
from wand.image import *


# 모든 함수들이  공통적으로 사용할 전역 변수 선언부
window, canvas, paper=None, None, None
photo, photo2=None, None #photo는 처음 불러들인 원본 이미지, photo2는 처리 결과를 저장할 변수
oriX,oriY= 0,0 # 원본 이미지의 폭과 높이를 저장하는 함수



# 함수 정의 부분
# 이미지를 화면상에 출력하는 사용자 정의 함수 선언
def displayImage(img, width, height) :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    # 이전 캔버스가 존재한다면 이전 캔버스를 삭제하여 기존에 이미지가 출력된 캔버스를 깨끗하게 처리
    if canvas != None:
        canvas.destroy()

    # 새 캔버스 생성, 처리된 이미지의 가로 세로 사이즈대로 생성 
    canvas = Canvas(window, width=width, height=height, bd=0, highlightthickness = 0)

    # 새 캔버스에 붙일 종이(paper) 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    # 새 종이는 다양한 이미지 파일 포맷이 아닌 단순히 빈 이미지를 보여줄 것이라 PhotoImage()로 생성
    paper=PhotoImage(width=width, height=height)

    # 새 캔버스에 종이(paper)를 붙임 ( 차후 그 종이 위에 처리된 이미지를 출력)
    # 생성될 위치는 가로 세로의 사이즈의 중간 위치
    canvas.create_image( (width/2, height/2), image=paper, state="normal") 
    

    blob = img.make_blob(format='RGB')  # 이미지를 바이너리 코드로 변환해주는 함수, 배열의 형태로 저장
    #print(type(blob)) # blob 자료형 출력 테스트, blob 의 자료형은 bytes 로 리스트형태의 문자열 데이터타입
    #print(blob)
    #print(blob[0],blob[1],blob[2],blob[3],blob[4],blob[5]) # blob 리스트 값 출력 테스트


    # 이미지의 폭과 높이만큼 반복해서 픽셀의 RGB 값을 추출
    for i in range(0,width) :
        for k in range(0, height) :
            r = blob[(i*3*width)+(k*3) + 0]   # blob[0],blob[3],blob[6],blob[9]...의 값을 r에 저장
            g = blob[(i*3*width)+(k*3) + 1]  # blob[1],blob[4],blob[7],blob[10], 의 값을 g에 저장
            b = blob[(i*3*width)+(k*3) + 2]  # blob[2],blob[5],blob[8],blob[11]의 값을 g에 저장
            # paper에 칼라로 점을 찍어줌, 세로로 높이만큼 찍고 가로를 너비만큼 반복
            paper.put("#%02x%02x%02x" % (r,g,b) , (k,i)) # r,g,b값 을 (02x)에 의해 각각 두자리 16진수로 변환하여 rgb 값으로 결합한 후 (k,i)에 찍어줌
            #print(r,g,b)  # r,g,b값 출력 테스트
            #print("#%02x%02x%02x, (%d, %d)" % (r,g,b, k,i)) # r,g,b값 을 16진수로 변환 결과 출력 테스트 
    # 처리된 결과 이미지의 픽셀을 찍어둔 종이paper가 붙여있는 캔버스를 화면에 출력

    #canvas.pack()
    canvas.place(x=(1500-width)/2-50, y=(850-height)/2)   # 파일 열기로 연 이미지를 화면 가운데에맞춰 출력하기
    

# 파일 열기
def func_open():
    global Window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    
    # askopenfilename() 함수로 파일 열기 대화상자를 나타내어 그림 파일 선택
    readFp = askopenfilename(parent=window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif;"),("모든 파일", "*.*") ))

    # 이미지는 GIF, JPG, PNG를 불러와 모두 처리하기 위해 PhotoImage() 가 아닌
    # Wand 라이브러리에서 제공하는 Image()를 사용

    #이미지를 준비하는 단계
    # photo는 처음 불러들인 원본 이미지
    photo = Image(filename=readFp) 
    oriX = photo.width  # 원본 이미지의 가로 사이즈를 oriX에 저장
    oriY = photo.height # 원본 이미지의 세로 사이즈를 oriX에 저장

    # photo2는 처리 결과를 저장할 변수
    photo2 = photo.clone()  # 원본 이미지의 photo를 복사하여 photo2에 저장
    newX = photo2.width
    newY = photo2.height
    # 복제된 photo2를 캔버스의 페이퍼에 디스플레이하는 사용자 정의 함수 실행
    displayImage(photo2, newX, newY)

    photo_Label=Label(window, text=readFp, fg="white", bg="black")
    photo_Label.place(x=36, y=30)


# 파일 저장
def func_save():
    
    global window, canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    # photo2는 func_open() 함수를 실행하면 생성됨
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None :
        return
    
    # 대화 상자로부터 넘겨받은 파일의 정보를 saveFp에 저장
    saveFp = asksaveasfile(parent=window, mode="w", defaultextension=".jpg", filetypes=(("JPG 파일", "*.jpg;*.jpeg"), ("모든 파일", "*.*") )) 
    savePhoto = photo2.convert("jpg") # 결과 이미지인 photo2를 jpg로 변환
    savePhoto.save(filename=saveFp.name)  # 파일 저장 대화창에서 입력받은 파일 이름으로 저장

# 되돌리기
def func_revert():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    
    photo2 = photo.clone()  # 원본을 복제해서 photo2 덮어쓰기
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 프로그램 종료
def func_exit():
    window.quit()
    window.destroy()

# 이미지 확대
def func_zoomin():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None :
        return
    
    # askinteger() 함수를 실행해 대화 상자로 확대할 배수 입력받음
    scale = askinteger("확대배수", "확대할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    #photo2 = photo.clone()  # 원본 이미지 photo를 복제하여 photo2에 저장
    photo2.resize(int(newX * scale), int(newY * scale))  # 원본 이미지의 가로 세로 사이즈에 배수를 곱하여 크기 변경    
    newX = photo2.width # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)


# 이미지 축소
def func_zoomout():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None :
        return
    
    # askinteger() 함수를 실행해 대화 상자로 축소할 배수 입력받음
    scale = askinteger("축소배수", "축소할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    #photo2 = photo.clone()  # 원본 이미지 photo를 복제하여 photo2에 저장
    photo2.resize(int(newX / scale), int(newY / scale))  # 원본 이미지의 가로 세로 사이즈에 배수를 나누어 크기 변경    
    newX = photo2.width # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)



# 상하 반전, flip() 함수 사용
def func_mirror1() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    if photo2 == None :
        return

    photo2.flip()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 좌우 반전, flop() 함수 사용
def func_mirror2() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    if photo2 == None :
        return


    photo2.flop()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)




# 이미지 처리1 > 회전
# 대화창을 통해 정수를 입력받아 그 수만큼 회전
# Wand 라이브러리에서 제공하는 rotate(각도)함수를 사용
def func_rotate() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    if photo2 == None :
        return


    degree = askinteger("회전", "회전할 각도를 입력하세요(0~360)", minvalue=0, maxvalue=360) 
    photo2.rotate(degree)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리2 > 밝게/어둡게
# Wand 라이브러리에서 제공하는 modulate(명도값,채도값,색상값)함수를 사용
# 명도는 modulate(명도값, 100, 100) 함수를 사용
# 원본의 명도값이 100이므로 100이상은 '밝게', 100 이하는 '어둡게' 처리
# 밝게, modulate(밝기값, 100, 100) 함수에 100~200 값 입력
def func_bright():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("밝게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


def func_dark():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("어둡게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)
    

# 이미지 처리2 > 선명하게/탁하게
# Wand 라이브러리에서 제공하는 modulate(100,채도값,100)함수를 사용
# 원본의 채도값이 100이므로 100 이상은 '선명하게', 100 이하는 '탁하게' 처리
def func_clear():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("선명하게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


def func_unclear():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("탁하게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)

    
# 이미지 처리2 > 흑백이미지
# 이미지의 type 값을 "grayscale"로 설정
def func_bw():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    photo2.type="grayscale"
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리3 > 이미지 색조 변경
def func_hue():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("색조", "값을 입력하세요(0~200)", minvalue=0, maxvalue=200)
    photo2.modulate(100, 100, value)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리3 > 이미지 반전
def func_reverse():
    import cv2

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    img = cv2.imread('image/travel3.png')
    out = 255 - img.copy()
    cv2.imshow('origin', img)
    cv2.imshow('reverse', out)
    cv2.waitKey(0)

    cv2.imwrite('image/travel3.png', out)

    
"""
# 이미지 처리3 > 이미지 블러
def func_blur():

    from PIL import Image
    from PIL import ImageFilter
    
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    
    photo2 = photo.clone()
    photo2 = photo2.filter(ImageFilter.BLUR)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)
    

# 이미지 처리3 > 이미지 엠보싱
def func_embo():
    
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY     # 전역 변수 선언

    #파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    photo2 = photo.clone()
    photo2 = photo2.filter(ImageFilter.EMBOSS)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)
"""

# 이미지 처리 3 > 이미지 모자이크 처리
def func_mosaic():
    import cv2

    # askopenfilename() 함수로 파일 열기 대화상자를 나타내어 그림 파일 선택
    readFp = askopenfilename(parent=window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif;"),("모든 파일", "*.*") ))

    rate = 15               # 모자이크에 사용할 축소 비율 (1/rate)
    win_title = 'mosaic'    # 창 제목
    img = cv2.imread(readFp)    # 이미지 읽기

    while True:
        x,y,w,h = cv2.selectROI(win_title, img, False) # 관심영역 선택
        if w and h:
            roi = img[y:y+h, x:x+w]   # 관심영역 지정
            roi = cv2.resize(roi, (w//rate, h//rate)) # 1/rate 비율로 축소
            # 원래 크기로 확대
            roi = cv2.resize(roi, (w,h), interpolation=cv2.INTER_AREA)  
            img[y:y+h, x:x+w] = roi   # 원본 이미지에 적용
            cv2.imshow(win_title, img)
        elif cv2.waitKey(0) & 0xFF == 27:
            break
        
    cv2.destroyAllWindows()

# 원그리기
def func_circle():
    import cv2
    
    readFp = askopenfilename(parent=window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif;"),("모든 파일", "*.*") ))
    title = 'mouse event'                   # 창 제목
    img = cv2.imread(readFp)                # 이미지 읽기
    cv2.imshow(title, img)                  # 이미지 표시

    colors = {'black':(0,0,0),
             'red' : (0,0,255),
             'blue':(255,0,0),
             'green': (0,255,0) } # 색상 미리 정의

    def onMouse(event, x, y, flags, param): # 마우스 콜백 함수 구현 ---①
        #print(event, x, y, flags)                # 파라미터 출력
        color = colors['black']
        if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 누름인 경우 ---②
            # 컨트롤키와 쉬프트 키를 모두 누른 경우
            if flags & cv2.EVENT_FLAG_CTRLKEY and flags & cv2.EVENT_FLAG_SHIFTKEY : 
                color = colors['green']
            elif flags & cv2.EVENT_FLAG_SHIFTKEY : # 쉬프트 키를 누른 경우
                color = colors['blue']
            elif flags & cv2.EVENT_FLAG_CTRLKEY : # 컨트롤 키를 누른 경우
                color = colors['red']
            # 지름 30 크기의 검은색 원을 해당 좌표에 그림
            cv2.circle(img, (x,y), 30, color, -1) 
            cv2.imshow(title, img)          # 그려진 이미지를 다시 표시 ---③

    cv2.setMouseCallback(title, onMouse)    # 마우스 콜백 함수를 GUI 윈도우에 등록 ---④

    while True:
        if cv2.waitKey(0) & 0xFF == 27:     # esc로 종료
            break
    cv2.destroyAllWindows()


# 동영상 출력
def func_video():
    import cv2

    readFp = askopenfilename(parent=window, filetypes=(("모든 영상 파일", "*.avi;*.mp4"),  ("모든 파일", "*.*") ))
    
    #video_file="Movies/0001.mp4"                    # 동영상 파일 경로

    video_file=str(readFp)

    cap = cv2.VideoCapture(video_file)              # 동영상 캡쳐 객체 생성
    if cap.isOpened():
        while True:
            ret, img = cap.read()                   # 다음 프레임 읽기
            if ret:                                 # 프레임 읽기 정상
                cv2.imshow(video_file, img)         # 화면에 표시
                cv2.waitKey(1)                     # 1ms 지연 숫자 높을수록 동영상 느려짐
                
            elif cv2.waitKey(0) & 0XFF == 27:
                break

            else:                                   # 다음 프레임을 읽을 수 없는 경우
                break                               # 재생 완료
    else:
        print("Can't open video.")
    cap.release()
    cv2.destroyAllWindows()




# 메인 코드부
window = Tk()   # 부모 윈도우
window.geometry("1500x850")
window.title("미니 포토샵(Ver 0.1)")


# 배경이미지 출력
bgPhoto = PhotoImage(file ="bg.png")     # 배경 이미지 준비
bg_Image = Label(window, image = bgPhoto)       # 이미지 생성
bg_Image.place(x=-2, y=-2)                       # 이미지 디스플레이


# 1.메뉴 자체 생성
# 메뉴 자체 = Menu(부모 윈도우)
# 부모 윈도우.config(menu = 메뉴 자체)
mainMenu = Menu(window)     # 메뉴자체
window.config(menu = mainMenu)


# 2. 상위 메뉴 생성
# 상위 메뉴 = Menu(메뉴자체)
# 메뉴자체.add_cascade(label="상위 메뉴 텍스트", menu=상위메뉴)
# add_cascade() 메소드는 상위 메뉴와 하위 메뉴 연결

fileMenu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="파일", menu=fileMenu)


# 3. 하위 메뉴 생성
# 상위메뉴.add_command(label="하위 메뉴1", command=함수1)
# add_command() 메소드는 기본 메뉴 항목 생성
fileMenu.add_command(label="파일 열기", command=func_open)
fileMenu.add_command(label="파일 저장", command=func_save)
fileMenu.add_separator() # 구분선 삽입
fileMenu.add_command(label="되돌리기", command=func_revert)
fileMenu.add_separator() # 구분선 삽입
fileMenu.add_command(label="프로그램 종료", command=func_exit)



# 두번째 상위 메뉴(이미지 처리1) 생성
image1Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="이미지 처리(1)", menu=image1Menu)
image1Menu.add_command(label="확대", command=func_zoomin)
image1Menu.add_command(label="축소", command=func_zoomout)
image1Menu.add_separator() # 구분선 삽입
image1Menu.add_command(label="상하 반전", command=func_mirror1)
image1Menu.add_command(label="좌우 반전", command=func_mirror2)
image1Menu.add_separator() # 구분선 삽입
image1Menu.add_command(label="회전", command=func_rotate)



# 세번째 상위 메뉴(이미지 처리2) 생성
image2Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="이미지 처리(2)", menu=image2Menu)
image2Menu.add_command(label="밝게", command=func_bright)
image2Menu.add_command(label="어둡게", command=func_dark)
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="선명하게", command=func_clear)
image2Menu.add_command(label="탁하게", command=func_unclear)
image2Menu.add_separator() # 구분선 삽입
image2Menu.add_command(label="흑백이미지", command=func_bw)


# 네번째 상위 메뉴(이미지 처리3) 생성
image3Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="이미지 처리(3)", menu=image3Menu)
image3Menu.add_command(label="색조", command=func_hue)
image3Menu.add_command(label="반전", command=func_reverse)
#image3Menu.add_command(label="블러링", command=func_blur)
#image3Menu.add_command(label="엠보싱", command=func_embo)
image3Menu.add_separator() # 구분선 삽입
image3Menu.add_command(label="모자이크", command=func_mosaic)
image3Menu.add_command(label="원그리기", command=func_circle)
image3Menu.add_command(label="동영상", command=func_video)


window.mainloop()
