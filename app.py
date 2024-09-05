from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from graphanator import Conversation, get_latest_file  # Assuming you move your conversation class into a separate file
import pandas as pd
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Load the latest CSV file
f_path = 'data/' + get_latest_file(f"{os.getcwd()}/data")[0][0]
df = pd.read_csv(f_path)

# Initialize conversation
conversation = Conversation(context=df)


@app.route('/')
def index():
    return render_template('index.html')


# Define API endpoint to receive messages
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json.get("message")
        conversation.message('user', user_message)
        
        # Check if a command was found and needs execution
        if conversation.response["command"]:
            conversation.execute_code()

        # Return the response as JSON
        return jsonify({
            "response": conversation.response["response"],
            "command": conversation.response["command"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)
