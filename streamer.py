from flask import Flask, render_template, Response
from CAMERA import Camera
from socket import gethostbyname,gethostname

#recording the IPV4 address of the current device on network
hostname = gethostname()
ip_address = gethostbyname(hostname)

app = Flask(__name__)

@app.route('/')
def security():
    return render_template('//public//security.html')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/home')
def video_feed():
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host=ip_address, debug=True)