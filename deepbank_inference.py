#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :deepbank_inference.py
# @Time         :2025/10/10 10:47
# @Author       :https://github.com/vincenschan/
# @Description  : 

import json
from deepbank_adk import Client


class DeepBankInference:
    def __init__(self, api_key, model_name):
        """LLM初始化"""
        self.api_key = api_key
        self.model_name = model_name
        client = Client.build(self.api_key)
        self.llm = client.models.chat_openai(self.model_name)

    def inference(self, prompt):
        """
        推理
        :param prompt:
        :return:
        """
        response = self.llm.invoke(prompt)
        resp = json.loads(response.content)
        return resp


if __name__ == "__main__":
    pass
