from flask import Flask, request, jsonify, render_template, send_file, Response
from flask_socketio import SocketIO

from io import BytesIO

from file_manager import FileManager
from conversation import Conversation

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json
import random
import io

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
        role = request.json.get("role")
        message = request.json.get("message")

        message = {
            "role": role,
            "content": message
        }

        try:
            conversation.send_message(message)
        except Exception as e:
            print(e)

        plot()
        
        # Return the response as JSON
        return jsonify({
            "response": conversation.message_history[len(conversation.message_history) - 1]["content"],
            "command": conversation.message_history[len(conversation.message_history) - 1]["command"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define API endpoint to get conversation history
@app.route('/get_conversation_context', methods=['GET'])
def get_conversation():
    try:
        return jsonify(conversation.context.message["content"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Define API endpoint to handle start button click
@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    try:
        system_message = conversation.context.message["content"]
        message = {
            "role": "system",
            "content": system_message
        }
        conversation.send_message(message)
        return jsonify({
            "response": conversation.message_history[len(conversation.message_history) - 1]["content"],
            "command": conversation.message_history[len(conversation.message_history) - 1]["command"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.after_request
def save_message_history(response):
    try:
        with open('message_history.json', 'w') as file:
            json.dump(conversation.message_history, file)
    except Exception as e:
        print(f"Error saving message history: {str(e)}")
    return response

@app.route('/plot')
def plot():
    # Generate a simple plot using Matplotlib
    # plt.figure(figsize=(5, 4))
    # plt.plot([0, 1, 2, 3], [10, 20, 25, 30], color='blue', marker='o')
    # plt.title("Sample Plot")
    # plt.xlabel("X Axis")
    # plt.ylabel("Y Axis")

    df = conversation.context.df

    try:
        print("executing...")
        exec(conversation.message_history[len(conversation.message_history) - 1]["command"])
    except Exception as e:
        print(f"Error {e}")


    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the image as a response with MIME type 'image/png'
    return Response(buf, mimetype='image/png')

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)
