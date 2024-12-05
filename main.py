from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from model import Dishes, db, Exercise
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/cal', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        dish_name = request.form.get('dish')
    
        # Find the calories for the dish
        calories = Dishes.query.filter_by(name=dish_name).first()
    
        if calories:
            result = []
            exercises = Exercise.query.all()
            for exercise in exercises:
                calories_burn = exercise.calories_burn
                if calories_burn >= calories.calories:
                    result.append(f"{exercise.name} : {exercise.time_spent} min")
                else:
                    for i in range(5):
                        if calories_burn * i >= calories.calories:    
                            result.append(f"{exercise.name} : {int(exercise.time_spent) * i} min")
                            break
            return render_template('home.html', dish_name=dish_name, calories=calories.calories, result=result)
        
        else:
            return render_template('home.html', dish_name=dish_name, calories=None, result=["Sorry, the calorie information for this dish is not available."])
    else:   
        return render_template('home.html')
    
@app.route('/')
def landing_page():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
