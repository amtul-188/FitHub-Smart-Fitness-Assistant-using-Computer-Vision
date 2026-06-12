from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise/biceps-curl')
def exerciseBicepsCurl():
    return render_template('exerciseBicepsCurl.html')

@app.route('/exercise/push-ups')
def exercisePushUps():
    return render_template('exercisePushUps.html')

@app.route('/exercise/triceps')
def exerciseTriceps():
    return render_template('exerciseTriceps.html')

@app.route('/exercise/squats')
def exerciseSquats():
    return render_template('exerciseSquats.html')

@app.route('/yoga/t-pose')
def yogaT():
    return render_template('yogaT.html')

@app.route('/yoga/tree-pose')
def yogaTree():
    return render_template('yogaTree.html')

@app.route('/yoga/warrior-pose')
def yogaWarrior():
    return render_template('yogaWarrior.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')

if __name__ == '__main__':
    app.run(debug=True)