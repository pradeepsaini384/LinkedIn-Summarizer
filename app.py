import openai
from linkedin_scraper import Person, actions
from selenium import webdriver
from flask import Flask,request , render_template , redirect, url_for
import os 
import json
app = Flask(__name__)

file_name = "data.json"
def load_from_json(file_name):
    try:
        with open(file_name, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None
def check_user_in_json(url):
    data= load_from_json(file_name)
    for i in data:
        if url in i['name']:
            return i['details']
    else:
        return None
def user_data_in_json(url):
    data= load_from_json(file_name)
    for i in data:
        if url in i['name']:
            return i['output']
        else:
            return None
def check_user_len_in_json(url):
    data= load_from_json(file_name)
    for i in data:
        if url in i['name']:
            return len(i['output'])
        else:
            return None
def save_new_user_in_json(url,person):
    dic = {
        "name": url ,
        "details": person,
        "output":[]
    }
    data = load_from_json(file_name)
    data.append(dic)
    with open(file_name, 'w') as json_file:
            json.dump(data, json_file)
def save_output_in_json(url,output):
    data = load_from_json(file_name)
    for i in data :
        if url in i['name']:
            if len(i['output']) <2:
                i['output'].insert(0,output)
                with open(file_name, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                output_saved = i['output']
                return output_saved
            else:
                return i['output']
       
            
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/output',methods=['GET','POST']) 
def output():
    url = request.form.get('url')
    already_Store = check_user_in_json(url)
    if already_Store is None:
        email = os.environ.get('email')
        password = os.environ.get('password')
        driver = webdriver.Chrome()
        actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
        person = str(Person(f"{url}", driver=driver))
        save_new_user_in_json(url,person)
        output = call_ai(already_Store,url)
        return output
    else :
        output = call_ai(already_Store,url)
        return output
def call_ai(person,url):
    user_len= check_user_len_in_json(url)
    if(user_len)==2:
        answer = user_data_in_json(url)
        return redirect(url_for('result',url= url,answer=answer))
    else:
        api_key = os.environ.get('OPENAI_API_KEY')
        # Initialize the OpenAI API client
        openai.api_key  = api_key
        prompt = f"""You Are A Best Ai Tool who can generate a short paragraph for linkedin About section .
                You have the ability to understand the parameter according to a list or python generated output . 
                this output have very short details on about his name ,college , Experience and his skills .
                so being a smart reader you have to understand all parameters in details and generate a summary of  on his given details and make sure the output format  is like a person expressing about himself or give a interview and interviewer asking tell me about yourself.
                details = {person}
        """
        # Generate a response using the OpenAI GPT-3.5 Turbo model
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5 Turbo engine
            prompt=prompt,
            max_tokens=500,  # Adjust the length of the generated response
            stop=None, 
            temperature= 0.5 # You can specify a stop word to end the response if needed
        )

        # Extract and print the generated answer
        answer = response.choices[0].text.strip()
        return redirect(url_for('result',url= url,answer=answer))
@app.route('/result')
def result():
    url = request.args.get('url')
    answer  = request.args.get('answer')
    data = save_output_in_json(url,answer)
    return render_template('output.html',url= url, output= data)

if __name__ == "__main__":
    app.run(debug=True)
