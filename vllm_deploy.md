
```angular2html
gpu-memory-utilization 0.7    --trust-remote-code  --root-path /1b  --port 8801

nohup python3 -m vllm.entrypoints.openai.api_server   --model /root/autodl-tmp/vincens/Qwen3-14B-FP8  --max-num-seqs  64 --gpu-memory-utilization 0.75  --trust-remote-code  --root-path /14b  --port 8802 
>> output.Qwen3-14B-FP8.out 2>&1 &

CUDA_VISIBLE_DEVICES=0,1 python3 -m vllm.entrypoints.openai.api_server --model /data/oceanus_ctr/j-zhanxiaojie-jk/models/Qwen/Qwen2.5-72B-Instruct/Qwen2___5-72B-Instruct/ --trust-remote-code --tensor-parallel-size 2 --port 8002 --max-num-batched-tokens 8192
```


## 主参数说明

| 参数                         | 类型 / 默认值                              | 说明                                                                                   |
| -------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------ |
| `--model`                  | `str`                                 | **必填**。模型路径或 HuggingFace 名称，例如：`meta-llama/Llama-2-7b-hf` 或本地路径 `/data/model/llama`。 |
| `--tokenizer`              | `str / None`                          | 指定 tokenizer（默认随模型自动加载）。                                                             |
| `--dtype`                  | `auto / float16 / bfloat16 / float32` | 模型精度，默认 `auto`（vLLM 自动选择）。                                                           |
| `--port`                   | `8000`                                | HTTP 服务端口。                                                                           |
| `--host`                   | `0.0.0.0`                             | 监听地址。                                                                                |
| `--max-num-batched-tokens` | `None`                                | 控制单批最大 token 数，防止过大 batch 占显存。                                                       |
| `--max-num-seqs`           | `256`                                 | 最大同时处理的 sequence 数。                                                                  |
| `--gpu-memory-utilization` | `0.9`                                 | GPU 显存利用率上限（1.0 表示最大化使用）。                                                            |
| `--max-model-len`          | `4096`                                | 最大上下文长度（tokens）。                                                                     |
| `--tensor-parallel-size`   | `1`                                   | 启动时使用的 GPU 数量（张量并行数）。                                                                |
| `--worker-use-ray`         | `False`                               | 是否通过 Ray 管理 worker。一般本地部署不需要。                                                        |
| `--pipeline-parallel-size` | `1`                                   | 管线并行数。多机部署时使用。                                                                       |
| `--trust-remote-code`      | `False`                               | 如果模型使用自定义代码（HuggingFace Hub 上带自定义模块），需设为 True。                                       |


## 多LORA支持参数说明
| 参数                         | 说明                                                                                       |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| `--enable-lora`            | 开启 LoRA 支持。                                                                              |
| `--lora-modules name=path` | 注册一个或多个 LoRA adapter，例如：<br>`--lora-modules finance=/data/lora/finance-lora`<br>可重复使用多次。 |
| `--max-loras`              | 控制最多同时加载的 LoRA 数量（超出后会自动卸载旧的）。                                                           |
| `--lora-buffer-size`       | 控制 GPU buffer 为 LoRA 占用的缓存大小（一般自动）。                                                      |
| `--load-format`            | 指定加载权重的格式（`auto`, `safetensors`, `pt`）。                                                  |
| `--disable-lora-cache`     | 不缓存 LoRA 权重（每次重新加载）。                                                                     |

### example
```angular2html
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-2-7b-hf \
  --enable-lora \
  --lora-modules finance=/data/lora/finance-lora \
  --lora-modules customer=/data/lora/customer-lora \
  --max-loras 4 \
  --gpu-memory-utilization 0.92 \
  --port 8000

payload = {
    "model": "finance",  # 或 "medical"
    "messages": [{"role": "user", "content": "请写一份理财建议"}]
}
```

## 性能调优参数说明
| 参数                        | 默认值     | 说明                                |
| ------------------------- | ------- | --------------------------------- |
| `--swap-space`            | `4`     | 用于 CPU/GPU 之间交换的空间（GB）。           |
| `--block-size`            | `16`    | 内部 block 分配单位（token 块大小）。         |
| `--seed`                  | `None`  | 固定随机数种子。                          |
| `--max-logprobs`          | `5`     | 控制返回的最大 logprob 数量。               |
| `--enable-prefix-caching` | `False` | 启用 prefix cache，提高重复 prompt 推理速度。 |
| `--disable-log-stats`     | `False` | 不打印统计信息。                          |
| `--served-model-name`     | `str`   | 指定暴露给 API 的模型名（覆盖 `model` 字段）。    |


## 接口说明
| Endpoint               | 说明    | 对应 OpenAI 接口                     |
| ---------------------- | ----- | -------------------------------- |
| `/v1/completions`      | 文本生成  | `openai.Completion.create()`     |
| `/v1/chat/completions` | 聊天式对话 | `openai.ChatCompletion.create()` |
| `/v1/models`           | 模型列表  | `openai.Model.list()`            |

## 快速验证
```angular2html
curl http://localhost:8000/v1/models
```

