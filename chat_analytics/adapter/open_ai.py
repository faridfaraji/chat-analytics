
import openai
import tenacity
import json


class OpenAI:

    @classmethod
    @tenacity.retry(stop=tenacity.stop_after_delay(5))
    def completion_with_backoff(cls, **kwargs):
        return openai.ChatCompletion.create(**kwargs)

    @classmethod
    def summarize(cls, prompt):
        ai_answer = cls.completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        summaries = ai_answer["choices"][0]["message"]["content"]
        return json.loads(summaries.replace("\'", '\"'))
