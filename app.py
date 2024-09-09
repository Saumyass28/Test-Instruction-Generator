from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

OCR_API_KEY = 'K87979299588957'

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/describe-testing-instructions', methods=['POST'])
def describe_testing_instructions():
    context = request.form.get('context', '')
    screenshots = request.files.getlist('screenshots')

    extracted_texts = []
    for screenshot in screenshots:
        files = {'file': screenshot}
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files=files,
            data={'apikey': OCR_API_KEY}
        )

        if response.status_code == 200:
            result = response.json()
            text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
            extracted_texts.append({
                'filename': screenshot.filename,
                'text': text
            })
        else:
            return jsonify({'error': 'OCR API error', 'details': response.text}), 500

    # Example logic to generate test cases from extracted text
    def generate_test_cases(text):
        test_cases = []
        if 'example condition' in text:
            test_cases.append('Verify condition X is met.')
        return test_cases

    test_cases = [generate_test_cases(item['text']) for item in extracted_texts]

    return jsonify({'context': context, 'extracted_texts': extracted_texts, 'test_cases': test_cases}), 200

if __name__ == '__main__':
    app.run(debug=True)