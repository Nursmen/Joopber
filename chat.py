import openai
import translators as ts

def predict(text):
    openai.api_key = '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'

    trans = ts.translate_text(text, translator='deepl', from_language='ru', to_language='en')
    prompt = [{'role': 'user', 'content': trans}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613", 
        messages=prompt, 
        temperature=0.2, 
        max_tokens=1024
    )

    answer = response['choices'][0]['message'].content
    return ts.translate_text(answer, translator='google', from_language='en', to_language='ru')
