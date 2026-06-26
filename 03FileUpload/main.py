# 모듈 임포트
import os # 업로드 경로 생성
import uuid # UUID 를 생성하기 위한 모듈
# 플라스크 관련 모듈
from flask import (Flask, render_template, request, redirect)
from flask import (url_for, send_from_directory)

# 플라스크 초기화
# Flask 앱 인스턴스를 생성
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 파일 업로드 경로 생성. 정적 파일 저장을 위해 static 하위로 설정.
# 업로드 경로 (static/uploads)
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
# 해당 디렉토리가 없다면 생성.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 메인 페이지 (파일 업로드 폼)
@app.route('/')
def index():
  return render_template('index.html')

'''
UUID(Universally Unique Identifier)
  : 직역하면 '범용 고유 식별자'로 중복되지 않는 고유한 문자열을
  생성해준다. 4개의 하이픈으로 구성된 32자의 숫자+영문 형식으로 생성됨.
'''

# UUID 생성 함수
def generate_uuid_filename(filename):
  # 매개변수로 전달된 파일명에서 확장자를 추출. 파일명의 우측 첫번째
  # 마침표를 기준으로 분할한 후 1번 요소를 선택학, 소문자로 변경한다.
  ext = filename.rsplit('.',1)[1].lower()
  # 랜덤 기반의 UUID를 생성한 후 확장자와 결합. 생성한 고유값은
  # hex 속성을 사용해서 32자의 16진수 문자열로 변환한다.
  return f"{uuid.uuid4().hex}.{ext}"

# 파일 업로드 처리. 전송방식은 반드시 POST로 지정해야한다. 
@app.route('/upload', methods=['POST'])
def upload_file():
  # 업로드 폼에서 userfile이라는 input요소가 없는 경우를 검사
  if 'userfile' not in request.files:
    return "파일이 없습니다."
  # 사용자가 파일을 선택하지 않은 경우를 검사
  file = request.files['userfile']
  if file.filename == '':
    return "파일명이 없습니다."
  # 첨부된 파일이 있다면 업로드 처리.
  if file:
    # UUID 를 이용해서 변경할 파일명 생성. 매개변수로 원본파일명 전달
    filename = generate_uuid_filename(file.filename)
    print('생성된파일명:', filename) #콘솔에서 확인하기
    # 파일이 저장될 디렉토리와 파일명을 결합해서 전체 경로 생성
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # 디렉토리에 파일 저장
    file.save(save_path)
    # 파일 목록 페이지로 이동
    return redirect(url_for('file_list'))
  
  return "업로드 실패"

# 파일 다운로드 처리(경로 변수 형식 사용)
@app.route('/download/<filename>')
def download_file(filename):
  # 파일명 변경 없이 다운로드 처리
  # as_attachment : 다운로드시 파일명을 변경함
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
  # download_name : 다운로드 시 파일명을 변경함
  # return send_from_directory(app.config['UPLOAD_FOLDER'],
  #                            filename, as_attachment=True
  #                            download_name='내이미지.png) 
  
# 업로드된 파일 목록 보기
@app.route('/fileList')
def file_list():
  # 업로드 디렉토리에 있는 모든 파일의 목록을 가져옴
  file_list = os.listdir(app.config['UPLOAD_FOLDER'])
  # 리스트 컴프리헨션으로 폴더를 제외한 파일만 반환해서 리스트 형식으로 저장한다.
  file_list = [f for f in file_list if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
  # 템플릿을 렌더링할때 파일목록을 변수로 전달한다.
  return render_template('list.html', files=file_list)

if __name__=='__main__':
  app.run(host='127.0.0.1', port=8181, debug=True)
# 만약 아래쪽에 함수가 정의되어 있으면 오류가 발생된다. 
