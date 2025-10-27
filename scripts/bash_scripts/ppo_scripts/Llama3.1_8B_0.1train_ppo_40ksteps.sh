lm_eval \
  --model vllm \
  --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/PPO/Llama-3.1-8B-Instruct_ppo_DeepValueHead_simple_reward_steps30k_vfcoef0.5_lr5e-4_0.1sfttrain/policy_only,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_baseline \
  --output_path results/Llama3.1_8b_0.1train_ppo_40ksteps \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
