from flask import Flask, request, render_template, jsonify
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

set(stopwords.words('english'))

app = Flask(__name__)

output ={}

@app.route('/')
def index():
    return render_template('form.html')


@app.route('/', methods=['GET','POST'])
def success():
    stop_words = stopwords.words('english')
    
    #convert to lowercase
    text1 = request.form['text1'].lower()
    
    text_final = ''.join(c for c in text1 if not c.isdigit())
        
    #remove stopwords    
    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

    dd= TextBlob(text=processed_doc1).sentiment.polarity
    if dd<0:
        return render_template('form.html', final="Negative", text1=text_final)
        
    elif dd==0:
        return render_template('form.html', final="Neutral", text1=text_final)
        
    elif dd>0:
        return render_template('form.html', final="Positive", text1=text_final)

def Sentiment(sentence):
    score = TextBlob(sentence).sentiment.polarity
    if(score > 0):
        return 'Positive'
    else:
        return "Negative"


@app.route('/sentiment/', methods=['GET','POST'])
def SentimentAnalysis():
    if request.method=='POST':
        sentence =request.form['text']
    else:
        sentence = request.args.get('text')

    sent = Sentiment(sentence)
    output['Sentiment'] =sent
    return jsonify(output)
    
if __name__ == "__main__":
    app.run(debug=True)
