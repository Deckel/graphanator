from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO

from file_manager import FileManager
from conversation import Conversation

import pandas as pd
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize conversation
context = FileManager()
conversation = Conversation(context.latest_file)


@app.route('/')
def index():
    return render_template('index.html')


# Define API endpoint to receive messages
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json.get("message")

        message = {
            "role": "user",
            "content": user_message
        }

        try:
            conversation.send_message(message)
        except Exception as e:
            print(e)
        
        # Return the response as JSON
        return jsonify({
            "response": conversation.message_history[len(conversation.message_history) - 1]["content"],
            "command": conversation.message_history[len(conversation.message_history) - 1]["command"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)
