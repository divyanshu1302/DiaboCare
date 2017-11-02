from Diabocare.application import app
import os

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	# port = int(os.environ.get("PORT", 5000))
	# app.run(host='0.0.0.0', port=8080, debug=True)
	app.run(port=5001, debug=True)
