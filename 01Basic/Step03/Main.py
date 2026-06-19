# flask 모듈 입포트
from flask import Flask
# flask 객체 생성
app = Flask(__name__)

'''
데코레이터를 이용해서 요청명에 대한 매핑을 하낟. 이때 실행할 함수를
엔드포인트(End-point)로 등록한다. 즉 root 경로로 요청이 들어오면
이 함수를 실행하겠다는 의미이다.
'''
@app.route('/')
def root():
  return 'Hello Flask(Main.py)'

'''
이 파일 자체를 python 명령으로 실행했을때 아래 지정한 옵션이
적용된 상태로 Flask 애플리케이션이 구동된다.
'''
if __name__=='__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)

# 실행
# python Main.py
