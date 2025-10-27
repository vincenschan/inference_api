#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :llm_infra.py
# @Time         :2025/10/1 10:35
# @Author       :https://github.com/vincenschan/
# @Description  : 


import torch
import os
from modelscope import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
from .base import InfrenceBase


class LocalInference(InfrenceBase):
    def __init__(self, model_dir=None, device="auto"):

        self.model_dir = model_dir
        self.device = device
        self.init_model()

    def init_model(self):
        # device = "cuda:0"  # 也可以通过"cuda:2"指定GPU or auto
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_dir,
                                                          device_map=self.device,
                                                          torch_dtype="auto",
                                                          trust_remote_code=True)

    def inference(self, prompt, text):
        """LLM推理"""
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        """
        gen_kwargs = {"max_length": 512, "do_sample": True, "top_k": 1}
        with torch.no_grad():
            outputs = model.generate(**model_inputs, **gen_kwargs)
            #print(tokenizer.decode(outputs[0],skip_special_tokens=True))
            outputs = outputs[:, model_inputs['input_ids'].shape[1]:] #切除system、user等对话前缀
            print(tokenizer.decode(outputs[0], skip_special_tokens=True))
        """
        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=1024
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(f">> response: {response}")
        return response


if __name__ == "__main__":
    model_dir = "/home/jovyan/vincens/models/models/Qwen3-14B"
    model_ins = LocalInference(model_dir)
    prompt = "你是一位专业的客服助手"
    text = "你有什么产品推荐么"
    res = model_ins.inference(prompt, text)