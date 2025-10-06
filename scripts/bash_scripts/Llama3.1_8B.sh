lm_eval \
  --model vllm \
  --model_args pretrained=meta-llama/Meta-Llama-3.1-8B-Instruct,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_baseline \
  --output_path results/nutribench_v2_baseline_llama3.1_8b \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
