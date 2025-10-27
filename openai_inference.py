#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :openai_inference.py
# @Time         :2025/10/9 17:29
# @Author       :https://github.com/vincenschan/
# @Description  : 


import openai
from .base import InfrenceBase


class OpenAIInference(InfrenceBase):
    @classmethod
    def inference(cls, prompt, model="openai/gpt-4.1",
                  api_key="sk-0d7fc462-8730-4866-b990-8792ad5a0ec7",
                  base_url="https://deepbank-llm.daikuan.qihoo.net"):
        client = openai.OpenAI(
          api_key=api_key,  # 请替换为您创建的个人key
          base_url=base_url # 模型网关提供的访问接口
        )
        response = client.chat.completions.create(
          model=model,
          messages=[
            {
              "role": "user",
              "content": prompt
            }
          ]
        )
        # print(response)
        return response


if __name__ == "__main__":
    pass
