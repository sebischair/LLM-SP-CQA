# Evaluating Large Language Models in Semantic Parsing for Conversational Question Answering over Knowledge Graphs

This GitHub repository hosts the code and data resources accompanying the paper titled "Evaluating Large Language Models in Semantic Parsing for Conversational Question Answering over Knowledge Graphs".

## Structure of the Repository
* **spice_dataset_preparation.ipynb**: Was have created a processed dataset called SPICE_dataset_pp. This is a processed version of the original SPICE dataset that resolves Wikidata references and adds them explicitly to speed up inference e.g. _{'Q1238570': 'political scientist'}_ instead of only _'Q1238570'_
    * You only need to use this if you want to reproduce the processed dataset or if you increase the size of the subset from the test set for the predictions
* **spice_finetune_dataset.ipynb**: This was utilized to create the fine-tuning dataset. It results in spice_finetune_dataset_chat_30000_v02.json which we use to create the LoRA-7B model based on LLaMA
    * This is only needed if you want to change the size of the existing fine-tuning dataset
* **spice_finetuning.ipynb**: Contains the code to fine-tune the LLaMA model using spice_finetune_dataset_chat_30000_v02.json as data and the LoRA approach
* **spice_predictions.ipynb**: This is the code to create SPARQL query predictions with models running on a local server (i.e. LLaMA, Vicuna, LoRA) and from the OpenAI API (i.e. GPT-3.5-Turbo). It selects the number of samples for each question sub-category according to the distribution of the full test set.
* **spice_evaluation.ipynb**: It first merges all predictions of one model-prompt combination into a dedicated file. Afterwards it is used to execute the official evaluation script for each question type.
* **human_evaluation/human_evaluation_script.ipynb**: This was used to select random instances for labeling and to analyze the annotated data.
* **lora_adapter**: Adapter for LLaMA to create the LoRA model fine-tuned on SPICE
* **Results**: Contains predictions and evaluations for all model prompt combinations
* **SPICE_dataset_pp**: A processed version of the SPICE dataset that contains resolved references to entities

## Setup
1. Download the SPICE data set (available [here](https://github.com/EdinburghNLP/SPICE/tree/main))
2. Clone this repository to your workspace
3. Setup the [LLaMA](https://github.com/facebookresearch/llama) Large Language Model (LLM)
4. Setup the Vicuna LLM using [FastChat](https://github.com/lm-sys/FastChat)
5. If you want to use OpenAI (i.e. GPT-3.5-turbo), rename the _.env.dist_ file to _.env_ and add your OpenAI API key there
6. To fine-tune a LLaMA model with LoRA and our data, follow the instructions in spice_finetuning.ipynb
7. Create predictions with the spice_predictions.ipynb script
8. The automatic evaluation can be executed using the spice_evaluation.ipynb script
