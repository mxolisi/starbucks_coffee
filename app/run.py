import json
import pandas as pd
from flask import Flask
from flask import render_template, request, jsonify
from sklearn.externals import joblib
import math

app = Flask(__name__)



model = joblib.load("../classifier.pkl")


@app.route('/')
@app.route('/index')
def index():
    
   
   
    return render_template('master.html')



@app.route('/go',methods=['GET','POST'])
def go():
    
    myform= request.form
    
    gender = myform.getlist('gender')[0]
    age = int(myform.getlist('age')[0])
    
    income = int(myform.getlist('income')[0])

    
    difficulty = int(myform.getlist('difficulty')[0])
    reward = int(myform.getlist('reward')[0])
   
    years_active=int(myform.getlist('years_active')[0])
    duration=int(myform.getlist('duration')[0])
    social= 0
    if(myform.getlist('social')):
        social=1
    web=0
    if(myform.getlist('web')):
        web=1
    
    email=0
    if(myform.getlist('email')):
        email=1
    

    mobile=0
    if(myform.getlist('mobile')):
        mobile=1
    offer_type_bogo= int(myform.getlist('offer_type')[0]=='bogo')
    offer_type_discount=int(myform.getlist('offer_type')[0]=='discount')
    offer_type_informational=int(myform.getlist('offer_type')[0]=='informational')

    inputs=[[age, income, int(age>=10 and age <20), int(age>=20 and age <30),
       int(age>=30 and age <40), int(age>=40 and age <50),int(age>=50 and age <60),
       int(age>=60 and age <70), int(age>=70 and age <80), int(age>=80 and age <90),
       int(age>=90 and age <100), int(age>=100 and age <120), int(gender=='F'), int(gender=='M'),
       int(gender=='O'), years_active, difficulty, duration, reward,
       social, web, email, mobile, offer_type_bogo,
       offer_type_discount, offer_type_informational]]

    df=pd.DataFrame(inputs,columns=['age', 'income', 'age_group_10_to_20', 'age_group_20_to_30',
       'age_group_30_to_40', 'age_group_40_to_50', 'age_group_50_to_60',
       'age_group_60_to_70', 'age_group_70_to_80', 'age_group_80_to_90',
       'age_group_90_to_100', 'age_group_100_to_120', 'gender_F', 'gender_M',
       'gender_O', 'years_active', 'difficulty', 'duration', 'reward_original',
       'social', 'web', 'email', 'mobile', 'offer_type_bogo',
       'offer_type_discount', 'offer_type_informational'])

    pred=model.predict(df)
   
    return render_template(
        'go.html',
        classification_result=str(pred[0])
    )
   
    
    
    
   

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
