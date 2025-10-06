lm_eval \
  --model vllm \
  --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/Llama-3.1-8B-Instruct_sft_LR2e-05_BS2_E2_DF1.0_remove_cot,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_baseline \
  --output_path results/Llama3.1_8b_0.1train \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
