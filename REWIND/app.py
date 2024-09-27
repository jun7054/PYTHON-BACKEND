from flask import Flask, jsonify, request, render_template;
import jinja2
app = Flask(__name__)
app.users = {}
app.posts = []
app.idCnt = 1

@app.route('/')
def root():
    return "기본"

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', users = app.users)

@app.route('sign-up', methods=['GET'])
def signUpPage():
    return render_template('signup.html')

# 회원가입
@app.route("/sign-up", methods=['POST'])
def signUp():
    newUser = request.json
    newUser["id"] = app.idCnt
    app.users[app.idCnt] = newUser
    app.idCnt += 1
    return jsonify(newUser)

# 유저 확인
@app.route("/check-users", methods=['GET'])
def check_users():
    return app.users

# 메세지
@app.route("/post", methods=['POST'])
def post():
    payload = request.json
    userID = int(payload['id'])
    msg = payload['msg']

    if userID not in app.users:
        return "사용자가 존재하지 않습니다.", 400
    if len(msg) > 300:
        return "300자를 초과했습니다.", 400

    app.posts.append({
        'user_id': userID,
        'tweet': msg
    })
    return '성공', 200

# 팔로우
@app.route("/follow", methods=['POST'])
def follow():
    payload = request.json
    userID = int(payload['id'])
    userIDtoFollow = int(payload['follow'])

    if userID not in app.users or userIDtoFollow not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    
    user = app.users[userID]
    if user.get('follow'):
        user['follow'].append(userIDtoFollow)
        user['follow'] = list(set(user['follow']))
    else:
        user['follow'] = [userIDtoFollow]
    return jsonify(user)

# 언팔로우
@app.route("/unfollow", methods=['POST'])
def unfollow():
    payload = request.json
    userID = int(payload['id'])
    userIdTofollow = int(payload['unfollow'])
    if (userID or userIdTofollow) not in app.users:
        return '사용자가 존재하지 않습니다.'
    user = app.users[userID]
    if user.get('follow'):
        try: user['follow'].remove(userIdTofollow)
        except: pass
    else:
        user['follow'] = []

    return jsonify(user)

# 타임라인
@app.route('/timeline/<int:userID>', methods=['GET'])
def timeline(userId):
    if userId not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if app.users[userId].get('follow'):
        followList = set(app.users[userId]['follow'])
    else:
        followList = set()
    followList.add(userId)
    timeline = [msg for msg in app.posts if msg['userId'] in followList]

    return jsonify({
        'userId' : userId,
        'timeline' : timeline
    })

if __name__ == "__main__":
    app.run()