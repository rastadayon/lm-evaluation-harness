lm_eval \
  --model vllm \
  --model_args pretrained=/data/nmysore/ppo_8r_vo_v4_novhead,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
  --batch_size auto \
  --tasks nutribench_v2_base \
  --output_path /data/rasta/lm-evaluation-harness/results/ppo/naveen/ppo_8r_vo_v4_novhead \
  --seed 42 \
  --log_samples \
  --apply_chat_template \
