lm_eval \
  --model vllm \
  --model_args pretrained=/data/rasta/models/naveen_settings_my_sft_2E/policy_only,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path results/Llama3.1_8B_v2_SFT_PPO_E2 \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
