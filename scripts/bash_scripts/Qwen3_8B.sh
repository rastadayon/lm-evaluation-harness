lm_eval \
  --model vllm \
  --model_args pretrained=Qwen/Qwen3-8B,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --gen_kwargs "max_gen_toks=1024,until=None" \
  --batch_size auto \
  --tasks nutribench_v2_baseline \
  --output_path results/Qwen3_8b \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
