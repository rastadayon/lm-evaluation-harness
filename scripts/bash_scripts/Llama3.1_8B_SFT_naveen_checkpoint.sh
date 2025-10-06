lm_eval \
  --model vllm \
  --model_args pretrained=/data/nmysore/out/fine_tuned_model_8r,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path results/Llama3.1_8B_SFT_naveen \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
