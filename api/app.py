from flask import Flask, request, jsonify
import os 

# Initialize app
app = Flask(__name__)

# Add routes 
@app.route('/', methods=['GET'])
def get():
  return jsonify({'msg': 'Hello World'})

# Run Server
if __name__ == '__main__':
  app.run(debug=True)