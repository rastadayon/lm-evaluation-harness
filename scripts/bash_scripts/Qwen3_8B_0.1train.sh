lm_eval \
  --model vllm \
  --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/Qwen3-8B_sft_LR2e-05_BS5_E2_DF0.8_remove_cot,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --gen_kwargs "max_gen_toks=1024,until=None" \
  --batch_size auto \
  --tasks nutribench_v2_baseline \
  --output_path results/Qwen3_8b_0.1train \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
