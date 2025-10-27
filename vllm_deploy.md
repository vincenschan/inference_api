
```angular2html
gpu-memory-utilization 0.7    --trust-remote-code  --root-path /1b  --port 8801

nohup python3 -m vllm.entrypoints.openai.api_server   --model /root/autodl-tmp/vincens/Qwen3-14B-FP8  --max-num-seqs  64 --gpu-memory-utilization 0.75  --trust-remote-code  --root-path /14b  --port 8802 
>> output.Qwen3-14B-FP8.out 2>&1 &

CUDA_VISIBLE_DEVICES=0,1 python3 -m vllm.entrypoints.openai.api_server --model /data/oceanus_ctr/j-zhanxiaojie-jk/models/Qwen/Qwen2.5-72B-Instruct/Qwen2___5-72B-Instruct/ --trust-remote-code --tensor-parallel-size 2 --port 8002 --max-num-batched-tokens 8192
```


