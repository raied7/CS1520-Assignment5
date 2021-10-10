import datetime
import flask
import message


app = flask.Flask(__name__)
cm = message.ChatManager()


def clear_old_messages():
    now = datetime.datetime.now()
    one_hour_ago = now - datetime.timedelta(hours=1)
    cm.clear_messages_before(one_hour_ago)


@app.route('/')
def root():
    clear_old_messages()
    chat = cm.get_messages_html()
    return flask.render_template('index.html', chat_messages=chat)


@app.route('/send', methods=['POST','GET'])
def send_message():
    user = flask.request.form['user']
    text = flask.request.form['text']
    if user and text:
        cm.create_message(user, text)
    clear_old_messages
    chat = cm.get_messages_html()

    return flask.render_template('index.html', chat_messages=chat, username=user)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
