# LLMOps Pipeline

This project showcase LLMOps pipeline that fine-tune a small sized LLM model to prepare the outage of the service type LLM. For this project, we choose [Gemini 1.0 Pro](https://deepmind.google/technologies/gemini/) for service type LLM and [Gemma](https://blog.google/technology/developers/gemma-open-models/) 2B/7B for small sized LLM model.

For this project, the following tech stacks are chosen:
- [TensorFlow Extended](https://www.tensorflow.org/tfx?hl=ko) (TFX) for building Machine Learning pipeline.
- [KerasNLP](https://keras.io/keras_nlp/) and [Keras](https://keras.io/) in general to fine-tune Gemma 2B/7B.
- [Gemini API](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) on Google Cloud/Vertex AI.

> When we finish up the project, there is possibility that we could add [Gemini API](https://ai.google.dev/) from Google AI Studio instead of Vertex AI. Also, we could showcase how to fine-tune Mistral-7B instead of Gemma models. We will see.

## Overview

We assume that small sized LLM could show comparable performance to that of service type LLM on a certain task, and this project is to prove such possibility. Furthermore, this project shows how to smoothly migrate from service type LLM to small sized LLM when 
- we experience the outage of service type LLM which could cause disasters on many service/applications that rely on the service type LLM.
- we want decide to use small sized LLM hosted on local servers for the cost savings or privacy issues.
- ......

We are going to extend the previous project, [GPT2Alpaca Pipeline](https://github.com/deep-diver/gpt2-ft-pipeline) which showcased how to fine-tune [KerasNLP's GPT2](https://keras.io/api/keras_nlp/models/gpt2/) model on [Alpaca dataset](https://github.com/gururise/AlpacaDataCleaned). Based on that, this project aims to add the following features (only the code snippets to build end to end TFX pipeline is reused from the previous project):

- Replacing GPT2 with Gemma 2B/7B
- Introducing coverage dataset
  - coverage dataset consists of a handful of `[prompt, output]` pairs. This data represents what we believe as desired `[prompt, output]` from service type LLM. That means fine-tuned model would be deployable if it could generate similar quality of outputs based on the give prompts.
  - There are two main purpose of coverage dataset
    - evaluate a fine-tuned model. To do this, we ask larger model like "Consider the score of the first output is 100/100, then what would be the score of the second output?".
    - seed to generate similar but not exactly the same dataset. Since the main focus to fine-tune a model is the achieve 100/100 score ideally, the coverage dataset could be a good source to generate synthetic dataset.
    - However, there could be a sort of generalization issue here if we use all of the coverage dataset for synthetic data generation. Hence, splitting it into seed and validation datasets should be considered.
- Replacing Alpaca Dataset to synthetically generated dataset by introducing `SynthDataGen` custom TFX component.
  - converage dataset is going to be used as seed data to generate diverse synthetic dataset. Synthetic dataset is generated by service type LLM.
- Introducing `LLMEvaluator` custom TFX component
  - The purpose of `LLMEvaluator` component is to assess the outputs of the fine-tuned small sized LLM. This component asks this assessment to service type LLM based on the outputs from the coverage dataset and the outputs generated by the fine-tuned small sized LLM.
  - `LLMEvaluator` component outputs the assessment results in percentage. With this, we could decide the coverage rate. 
- Continuous pipeline
  - If the converage rate from the `LLMEvaluator` is still below a certain threshold, we could ask `SynthDataGen` component to generate more of synthetic data.

## Todos

- [ ] Notebook to define coverage dataset.
- [ ] Notebook to define `SynthDataGen` component's functionality.
- [ ] Notebook to define `LLMEvaluator` component's functionality.
- [ ] Implement `SynthDataGen` and `LLMEvaluator` as custom TFX component.
- [ ] Notebook to define a portion of TFX pipeline with the custom component to fine-tune Gemma 2B/7B models.
- [ ] Implement a whole TFX pipeline including automatically exporting models and application to Hugging Face Hub.