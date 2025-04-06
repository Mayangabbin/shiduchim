from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # הפעל את הסקריפט באמצעות subprocess
        result = subprocess.run(['python3', 'shiduchimai.py'], capture_output=True, text=True)

        # אם הסקריפט רץ בהצלחה, תחזור עם תוצאה
        if result.returncode == 0:
            return f'Script ran successfully! Output: {result.stdout}', 200
        else:
            return f'Error: {result.stderr}', 500
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

