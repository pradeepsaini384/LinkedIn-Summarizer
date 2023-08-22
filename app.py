import openai
from linkedin_scraper import Person, actions
from selenium import webdriver
from flask import Flask,request , render_template
import os 
app = Flask(__name__)


memory =  []
def add_memory(url,person):
    dic = {
        "name": url ,
        "details": person
    }
    
    memory.append(dic)
    print(memory)
def check_memory(name):
    for i in memory:
        if name in i['name']:
            return i['details']
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/run',methods=['GET','POST']) 
def run():
    url = request.form.get('url')
    already_Store = check_memory(url)
    if already_Store is None:
        email = os.environ.get('email')
        password = os.environ.get('password')
        driver = webdriver.Chrome()
        actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
        person = Person(f"{url}", driver=driver)
        add_memory(url,person)
        output = call_ai(already_Store)
        return output
    else :
        output = call_ai(already_Store)
        return output
def call_ai(person):
    api_key = os.environ.get('OPENAI_API_KEY')

# Initialize the OpenAI API client
    openai.api_key = api_key
    prompt = f"""You Are A Best Ai Tool who can generate a short paragraph for linkedin About section .
             You have the ability to understand the parameter according to a list or python generated output . 
             this output have very short details on about his name ,college , Experience and his skills .
             so being a smart reader you have to understand all parameters and generate a summary of  on his given details and make sure the output format  is like a person expressing about himself or give a interview and interviewer asking tell me about yourself.
             details : {person}
    """

    # Generate a response using the OpenAI GPT-3.5 Turbo model
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo engine
        prompt=prompt,
        max_tokens=500,  # Adjust the length of the generated response
        stop=None,  # You can specify a stop word to end the response if needed
    )

    # Extract and print the generated answer
    answer = response.choices[0].text.strip()
    return(f"Generated Answer: {answer}")

if __name__ == "__main__":
    app.run(debug=True)
