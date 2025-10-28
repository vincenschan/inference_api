#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName     :lora_inference.py
# @Time         :2025/10/27 10:04
# @Author       :https://github.com/vincenschan/
# @Description  :

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
from huggingface_hub import snapshot_download


class LoraInference:
    def __init__(self):
        pass

    def load_inference(self, model_path, lora_name, lora_path, prompt, **kwargs):

        # 1) 下载/准备 LoRA adapter（如果 adapter 已在本地则直接用本地路径）
        lora_repo = "your-username/your-lora-repo"  # 例如 alignment-handbook/zephyr-7b-sft-lora
        lora_local_path = snapshot_download(repo_id=lora_repo)  # 会返回本地缓存路径

        # 2) 创建 vLLM LLM（注意 enable_lora=True）
        llm = LLM(model="meta-llama/Llama-2-7b-hf", enable_lora=True)

        # 3) 构造 LoRARequest: (human_name, unique_id, local_path)
        lora_req = LoRARequest(lora_name, 1, lora_local_path)

        # 4) 生成
        prompt = "写一首关于秋天的中文诗（四行）"

        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 128)

        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)

        # 如果需要多 adapter，可以为每次请求传不同的 LoRARequest / 多个 LoRARequest（参见多-LoRA示例）
        results = llm.generate(prompt, sampling_params, lora_request=lora_req)

        # 打印输出（results 的具体 API 取决于 vLLM 版本；通常可以遍历 tokens/chunks）
        for r in results:
            print(r.text)





if __name__ == "__main__":
    pass
