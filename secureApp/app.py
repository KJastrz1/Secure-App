from secureApp import create_app

app = create_app()

if __name__ == '__main__':  
    # app.run(debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
    app.run(debug=True, threaded=True)
