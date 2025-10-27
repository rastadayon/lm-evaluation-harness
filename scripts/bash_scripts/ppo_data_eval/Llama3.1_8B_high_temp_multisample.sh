for seed in 0 1 2 3 4 5 6 7 8 9 10; do
  lm_eval \
    --model vllm \
    --model_args pretrained=/data/qs4-data2/PPO-with-Confidence/models/Llama-3.1-8B-Instruct_sft_LR2e-05_BS16_E2_DF1.0_md_sft_halftrain_dict_output,tensor_parallel_size=4,dtype=auto,gpu_memory_utilization=0.8,data_parallel_size=1 \
    --batch_size auto \
    --tasks ppo_data_baseline \
    --output_path results/dict_output_halftrain_sft_multisample \
    --log_samples \
    --apply_chat_template \
    --seed $seed \
    --gen_kwargs '{"temperature": 1.9, "top_p": 0.95, "top_k": 100, "do_sample": true}'

done