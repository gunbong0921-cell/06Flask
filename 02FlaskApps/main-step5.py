# HTML 파일을 템플릿으로 사용하기 위한 모듈 임포트
from collections import UserDict
import email
import html
from os import error, name
from pickle import GET
from unittest.result import failfast

from flask import Flask, render_template, request
# 폼값 처리를 위한 모듈 임포트
from flask import redirect, session, url_for
# 페이지 이동
from markupsafe import escape
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
    
# URL 패스 Variable 1
'''
경로변수는 쿼리스트링 형식이 아닌 경로 자체를 사용해서 파라미터를
전달할 수 있다.
'''
# URL Path Variable : 타입을 생략하면 String 형식으로 전달
@app.route('/hello/<name>')
def hello(name):
  return "내 이름은 {}".format(name)

# URL 패스 Variable 2 : 정수형으로 지정
@app.route('/input/<int:num>')
def input(num):
  name = ''
  if num == 1:
    name = '홍길동'
  elif num == 2:
    name = '전우치'
  elif num == 3:
    name = '손오공'
  return "내 선택은 {}".format(name)   

# session 사용시 필수사항인 시크릿키 생성(랜덤한 문자열로 구성)
app.secret_key = 'ADeff/45dsfDFgdadasd/FA?sda'

# 예시 사용자를 딕셔너리로 정의 (실제 DB 연결 대신 하드코딩)
users = {
  'admin': '1234',
  'user': '9876'
} 

# 세션을 획득해야 진입할 수 있는 마이페이지
@app.route('/mypage')
def mypage():
  # 페이지로 진입하면 세션정보가 있는지 확인(로그인 되었는지 확인)
  if 'username' in session:
    # 로그인 된 상태라면 welcome 페이지를 렌더링
    # 템플릿으로 회원의 아이디를 전달한다.
    return render_template('welcome.html',
                           username=escape(session['username']))
    # 로그인이 안된 상태라면 login 페이지로 이동시킨다.
    # url_for() 함수의 인수는 라우팅 처리된 '함수명'을 지정한다.
  return redirect(url_for('login'))

# 로그인 페이지 
@app.route('/login', methods=['GET', 'POST'])
def login():
  # 로그인 페이지는 GET방식이 아닌 POST방식으로 제작한다.
  if request.method == 'POST':
    # POST방식의 전송이므로 form속성을 이용해서 폼갑을 받는다.
    input_id = request.form['username'] 
    input_pw = request.form['password']
    '''
    첫번째로 user 딕셔너리에 입력받은 아이디가 존재하는지 확인하고,
    두번째로 일치하는 패스워드가 있는지 확인한다.
    '''
    # 사용자 인증
    if input_id in users and users[input_id] == input_pw:
      # 로그인 정보가 일치하면 session객체에 사용자의 아이디를
      # 입력하고
      session['username'] = input_id
      # 마이페이지로 이동한다.
      return redirect(url_for('mypage'))
    else:
      # 로그인 정보가 일치하지 않는 경우에는 로그인 페이지로 이동한다.
      # 이때 error라는 인수에 오류메세지를 전달한다.
      return render_template('login.html',
                             error='아이디 또는 비밀번호가 틀렸습니다.')
      # 첫 진입시에는 링크를 클릭해서 이동하게 되므로 GET방식의 요청임
      # 따라서 로그인 페이지를 렌더링한다.
  return render_template('login.html')

# 로그아웃 처리
@app.route('/logout')
def logout():
  # session에 저장된 사용자 정보를 삭제한다.
  session.pop('username', None)
  # 삭제가 완료되면 index 페이지로 이동한다.
  return redirect(url_for('root'))     
    
# 플라스크 애플리케이션 작성시 모든 함수를 정의한 후 app.run()을
# 실행한다.
if __name__=='__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
  