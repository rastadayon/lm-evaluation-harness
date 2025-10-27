lm_eval \
  --model vllm \
  --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/PPO_lora_models/Llama-3.1-8B-Instruct_sft_LR2e-05_BS2_E2_DF1.0_remove_cot_ppo_lora_True_steps_3000_lr_5e-06_Adamw_kl_0.05_temperature_0.1/policy_only,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --gen_kwargs "max_gen_toks=8" \
  --tasks nutribench_v2_baseline \
  --output_path results/Llama3.1_8B_ppolora_temp0.1 \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
