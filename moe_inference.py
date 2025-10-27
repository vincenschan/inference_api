#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :deepbank_inference.py
# @Time         :2025/10/9 17:35
# @Author       :https://github.com/vincenschan/
# @Description  : 

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import deepspeed
from .base import InfrenceBase


class MOEInference(InfrenceBase):
    def __init__(self, model_name=None, device="auto"):
        self.model_name = model_name
        self.device = device
        self.init_model()

    def init_model(self):

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # 加载模型
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )

# DeepSpeed 推理优化
ds_engine = deepspeed.init_inference(
    model,
    mp_size=2,             # 张量并行数
    dtype=torch.float16,
    replace_method="auto",
    replace_with_kernel_inject=True,
    moe=True,              # 启用 MOE
    moe_top_k=1,           # 激活 top-1 专家
)

# 推理示例
inputs = tokenizer("你好，帮我写一段故事。", return_tensors="pt").to("cuda:0")
outputs = ds_engine.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0]))



if __name__ == "__main__":
    pass
