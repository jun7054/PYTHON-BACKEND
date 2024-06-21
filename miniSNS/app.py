from flask import Flask, render_template
app = Flask(__name__)
app.users = {}
app.posts = []
app.idCnt = 1

@app.route('/')
def root():
    return """
<h1>miniSNS</h1>
<div>
            <h1> miniSNS </h1>
            <button>메인 페이지</button>
            <button>회원 가입</button>
            <button>포스팅</button>
</div>
           """
@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', name="minjun")

if __name__ == '__main__':
    app.run()