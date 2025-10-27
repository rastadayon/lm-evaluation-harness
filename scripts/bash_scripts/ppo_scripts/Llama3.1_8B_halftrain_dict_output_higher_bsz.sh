export CUDA_VISIBLE_DEVICES=1,2,3,4 
lm_eval \
  --model vllm \
  --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/PPO/Llama-3.1-8B-Instruct_ppo_halftrain_dict_output_larger_bsz/policy_only,tensor_parallel_size=4,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path results/Llama3.1_8B_ppo_halftrain_dict_output_higher_bsz \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
