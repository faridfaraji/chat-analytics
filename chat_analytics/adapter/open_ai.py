
import openai
import tenacity
import json
import logging
import re


def let_us_parse(summary):
    lines = summary.strip().split("\n")

    conversations_list = []
    conv_dict = {}

    # Iterate over lines
    for line in lines:
        # Split line into key and value
        splitted = line.split(":")
        if len(splitted) == 2:
            key, value = splitted
            key = key.strip()
            value = value.strip()
            if key.lower() == "conversation_id" and conv_dict:
                # If a new conversation is starting and the dictionary is not empty
                # Add the old dictionary to the list and create a new one
                conversations_list.append(conv_dict)
                conv_dict = {key.lower(): value}
            else:
                conv_dict[key.lower()] = value
    # Add the last conversation to the list
    conversations_list.append(conv_dict)
    return conversations_list


class OpenAI:

    @classmethod
    @tenacity.retry(stop=tenacity.stop_after_delay(5))
    def completion_with_backoff(cls, **kwargs):
        return openai.ChatCompletion.create(**kwargs)

    @classmethod
    def summarize(cls, prompt):
        ai_answer = cls.completion_with_backoff(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        summaries = ai_answer["choices"][0]["message"]["content"]
        return let_us_parse(summaries)
