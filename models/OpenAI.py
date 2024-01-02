import openai
import time
import logging

logger = logging.getLogger(__name__)

class OpenAICall:
    def __init__(self, args, config) -> None:
        self.args = args
        self.settings = config
        openai.api_type = config.api_type
        openai.api_key = config.api_key
        openai.api_base = config.api_base
        openai.api_version = config.api_version

    def conversation(self, message, history):
        messages = []
        for item1, item2 in history:
            messages.append({"role": "user", "content": item1})
            messages.append({"role": "assistant", "content": item2})
        messages += [{"role": "user", "content": message}]

        retry_flag = 0
        while retry_flag < self.settings.max_retry_num:
            try:
                completion = openai.ChatCompletion.create(deployment_id="gpt4", model="gpt-4", messages=messages)
                response = completion.choices[-1].message['content']
                retry_flag = -1
                break
            except Exception as e:
                retry_flag += 1
                time.sleep(self.settings.retry_time)
                logger.info("Time out of OpenAI, Retrying...")
                continue
        if retry_flag >= self.settings.max_retry_num:
            response = "Unable to get output from openai."
            raise TimeoutError()
        return response
