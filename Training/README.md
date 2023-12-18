This folder contains EasyPhoto_training log and weights.

```
Folder Hierarchy:
    - user_id_folder/
        - original_backup 
            - source imgs

        - processed_images
            - train
                - source img (after preprocess)
                - source img.txt (caption)
            - metadata.jsonl
        
        - user_weights
            - best_outputs
                - best_img
                - best.safetensors

            - text2image-fine-tune
                - hypertune event folder
                    - hyper_params.yml
            
            - validation
                - validation imgs
    
            - checkpoint.safetensors
            - best.safetensors
            - pytorch_lora_weights.safetensors
        
        - ref_img

```