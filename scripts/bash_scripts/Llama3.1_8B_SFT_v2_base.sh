CUDA_VISIBLE_DEVICES=2 \
lm_eval \
  --model vllm \
  --model_args pretrained=/data/rasta/models/SFT/Llama-3.1-8B-Instruct_sft_LR2e-05_BS5_E2_DF0.8,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path results/Llama3.1_8B_SFT_v2_base \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
