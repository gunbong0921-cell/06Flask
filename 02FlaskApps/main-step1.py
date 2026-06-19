# HTML 파일을 템플릿으로 사용하기 위한 모듈 임포트
from flask import Flask, render_template
# 플라스크 앱 초기화 및 객체생성
app = Flask(__name__)

# 앱을 최초로 실행했을때의 화면. 주로 index페이지라고 표현한다.
@app.route('/')
def root():
  # 페이지 진입시 순수 텍스트만 웹브라우저에 출력됨.
  return 'Hello Flask Apps'
# 이미지 사용을 위한 static 폴더 확인용 페이지
# 요청명과 함수명은 일반적으로 동일하게 작성하는게 좋다.
@app.route('/image')
def image():
  # render_template() 함수로 템플릿에서 사용할 HTML파일을 렌더링
  # 한다. 프로젝트에 생성한 templates 폴더 하위로 자동저장된다.
  return render_template('static.html')

# 플라스크 애플리케이션 작성시 모든 함수를 정의한 후 app.run()을
# 실행한다.
if __name__=='__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
  