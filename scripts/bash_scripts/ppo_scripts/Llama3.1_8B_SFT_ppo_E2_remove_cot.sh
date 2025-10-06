lm_eval \
  --model vllm \
  --model_args pretrained=/data/rasta/models/PPO/Llama-3.1-8B-Instruct_ppo_LR1e-05_BS1_E2_DF0.8_remove_cot_policy_only,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path results/ppo/Llama-3.1-8B-v2_ppo_remove_cot \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
