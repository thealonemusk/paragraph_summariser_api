from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from localhost during development
app.add_middleware(
    CORSMiddleware,
    #  allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest

# Download the 'punkt' and 'stopwords' resources
nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

@app.post('/summarize/')
async def summarize_text(text: str = Form(...)):
    try:
        # Tokenize the text into sentences and words
        sentences = sent_tokenize(text)
        words = word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Calculate word frequencies
        word_freq = FreqDist(filtered_words)

        # Calculate sentence scores based on word frequencies
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]

        # Get the top N sentences with the highest scores as the summary
        summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)

        # Combine the summary sentences into the final summary
        summary = ' '.join(summary_sentences)

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
