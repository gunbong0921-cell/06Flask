# HTML 파일을 템플릿으로 사용하기 위한 모듈 임포트
from collections import UserDict
import email
import html
from os import name
from pickle import GET
from unittest.result import failfast

from flask import Flask, render_template, request
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

'''
Jinja2는 flask에서 사용하는 템플릿 엔진으로, 웹개발에서 사용되는 HTML
문서에 동적인 데이터를 삽입할 수 있게 해준다.
즉 HTML문서에 Python 코드를 사용할 수 있게 해주는 엔진이다.
'''
@app.route('/jinja2')
def jinja2():
  return render_template('jinja2.html',
                         title = 'Jinja2',
                         home_str = 'Jinja2를 알아봅시다',
                         home_list = [1, 2, 3, 4, 5])  

# 폼값을 입력하고 전송하기 위한 페이지 설정 
@app.route('/form')
def info():
  # 별도의 처리없이 템플릿 파일을 렌더링
  return render_template('form.html')

# 랑우팅 설정시 methods 속성에 사용할 전송방식을 list로 전송
@app.route('/method', methods=['GET', 'POST'])
def method():
  if request.method == 'GET':
    # GET 방식 : form 데이터를 request.srgs 로 받음
    # to_dict() 메서드를 사용하면 딕셔너리 형식으로 반환해준다
    args_dict = request.args.to_dict()
    print("args_dict (GET):", args_dict)
    # 반환된 값을 로그로 출력해서 확인
    userid = request.args["userid"] # 방법1
    # get() 함수의 인수로 접근하여 가져옴
    name = request.args.get("name") # 방법2
    email = request.args.get("email")
    # POST방식에서 사용하는 form은 사용할 수 없으므로 None으로 출력됨
    fail = request.form.get("name") # 의도적 오류 (None)
    print("실패예시 request.form.get(name):", fail)
    # 텔플릿을 렌더링하면서 필요한 변수를
    return render_template(
      'get.html',
      userid=userid,
      name=name,
      email=email,
      fail=fail
      )
  else:
    # POST 방식 : form 데이터를 request.form 으로 받음
    form_dict = request.form.to_dict()
    print("form_dict (POST):", form_dict)
    userid = request.form["userid"] # 방법1
    name = request.form.get("name") # 방법2
    email = request.form.get("email")
    # args는 GET방식에서만 사용할 수 있어 None으로 출력됨
    fail = request.args.get("name") # 의도적 오류
    print("실패예시 request.args.get(name):", fail)
    return render_template(
      'post.html',
      userid=userid,
      name=name,
      email=email,
      fail=fail
    ) 
    
# 플라스크 애플리케이션 작성시 모든 함수를 정의한 후 app.run()을
# 실행한다.
if __name__=='__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
  