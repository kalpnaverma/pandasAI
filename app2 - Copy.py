import io
from base64 import encodebytes
from PIL import Image
from flask import Flask, request, jsonify
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM
import os
app = Flask(__name__)
# Initialize the local LLM model
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="llama3:latest"
)
@app.route('/')
def home():
    return "Welcome to the PandasAI API!"
@app.route('/upload', methods=['POST'])
def upload():
            user = request.args.get('chart-type') 
            if not user:
                 return jsonify({"error": "Missing 'chart-type' parameter"}), 400
            print(f"User parameter: {user}")  
            data = pd.read_csv('RECORDS.csv')  # Read the CSV data
            df = SmartDataframe(data, config={"llm": model})  # Use PandasAI to process the data
            data_json = request.get_json()  # Get the JSON request data
            prompt = data_json.get("prompt", "")  # Extract the prompt
            response = df.chat(prompt)  # Get the response from PandasAI
            print(response)
            file_path='C:\\Users\\vermak\\Documents\\pandasAI\\exports\\charts\\temp_chart.png'
            encoded_img = get_response_image(file_path)
            if os.path.exists(file_path):  # Check if the file exists
                 os.remove(file_path)  # Delete the file
                 print(f"File {file_path} deleted successfully.")
            return encoded_img
def get_response_image(image_path):
    try:
        pil_img = Image.open(image_path)  # Open the image
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='png')  # Convert image to byte array
        encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # Encode as base64
        return encoded_img
    except Exception as e:
        return f"Error: {str(e)}"   
if __name__ == '__main__':
    app.run(debug=True)
