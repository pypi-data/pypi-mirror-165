![De-Identification Logo](./deid.png)

# Robust DeID: De-Identification of Notes - Removal of Private Information from Text.

**Named Entity Recognition models to identify and remove/replace protected health information (PHI) in text.**

*Version 1.0.0 / 01 September 2022*

*We're working on expanding the documentation and readme. While we work on that, taking a look at the source code may help answer some questions.*

*Most elements of the readme are referenced and used from [BLOOM](https://huggingface.co/bigscience/bloom). We'd like to thank the BLOOM authors for their extensive model card that inspired and helped us develop ours!*

*Comments, feedback and improvements are welcome and encouraged!*

---

# Project Details 

*This section provides information about the project. This includes information about installation, project features, and a general project overview.*
*It is useful for getting a brief understanding of the project and submitting any questions to the project team*

<details>
<summary>Click to expand</summary>

* This repository was used to train and evaluate various de-identification models and strategies. 
* The models and strategies are extensible and can be used on other datasets as well.
* The medical notes from the i2b2 2014 cohort [[Stubbs and Uzuner, 2015]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4978170/) and the Mass General Brigham network (medical notes from 11 institutes) were used to train and test the models.
* The medical notes within the Mass General Brigham network contain private information. To make the models trained on this set of notes available to the public, we replaced all the private information (PHI) in these notes with named-entities generated using the [Faker](https://faker.readthedocs.io/en/stable/) library (e.g. names were replaced with names generated from [Faker](https://faker.readthedocs.io/en/stable/)).
* Trained models are published on huggingface under the [OBI organization](https://huggingface.co/obi). The models trained as part of this project are hosted on HuggingFace with the names: [obi/deberta_deid_i2b2_mgb](https://huggingface.co/obi/deberta_deid_i2b2_mgb), [obi/deberta_deid_i2b2](https://huggingface.co/obi/deberta_deid_i2b2), [obi/deberta_deid_no_augment_i2b2](https://huggingface.co/obi/deberta_deid_no_augment_i2b2)
* The models are token classification models built to identify tokens that contain private information (named entity recognition).
* A token classification model along with a NER notation (e.g. BIO, BILOU etc.) can be used to identify spans from token labels. Spans are a collection of tokens that represent some protected health information (PHI) entity.
* The 11 private entities/spans the models identify are defined by HIPAA and more details about these PHI entities can be found here: [Annotation guidelines](data/AnnotationGuidelines.md)

> *We'd like to thank the authors of [i2b2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4978170/), [Faker](https://faker.readthedocs.io/en/stable/), [HuggingFace](https://huggingface.cohttps://huggingface.co) and the other libraries that made this project possible.*


## Overview
*This section provides information about the project version, license, funders, release date, developers, and contact information.*
*It is useful for anyone who wants to reference the project.*

<details>
<summary>Click to expand</summary>

*All collaborators are either volunteers or have an agreement with their employer.*
  
**Developed by:** One Brave Idea ([website](https://www.onebraveidea.org))

**Authors:** [Prajwal Kailas](https://github.com/prajwal967), [Max Homilius](), [Shinichi Goto](), [Rahul Deo]()

**Version:** 1.0.0

**Languages:** English

**License:** MIT

**Release Date:** Thursday, 01 September 2022

**Send Questions to:** *(Further information forthcoming.)*

**Cite as:** *(Further information forthcoming.)*

**Funded by:** 
    
* *(Further information forthcoming.)*

</details>

## Features
*This section provides the key features of this project. It provides a quick overview of the project.*

<details>
<summary>Click to expand</summary>

1. **Transformer models:** Any transformer model from the [HuggingFace](https://huggingface.co/models) library can be used for training. 
2. **Public Models:** We make available three [DeBERTa](https://arxiv.org/abs/2006.03654) based de-identification models. The models are hosted on HuggingFace with the names: [obi/deberta_deid_i2b2_mgb](https://huggingface.co/obi/deberta_deid_i2b2_mgb), [obi/deberta_deid_i2b2](https://huggingface.co/obi/deberta_deid_i2b2), [obi/deberta_deid_no_augment_i2b2](https://huggingface.co/obi/deberta_deid_no_augment_i2b2)
3. **Recall biased thresholding:** Use a classification bias to aggressively remove PHI from documents. This is a safer and more robust option when working with sensitive data like medical notes.
4. **Augmentations:** Replacing private information with randomly generated information (names, locations etc.) using the [Faker](https://faker.readthedocs.io/en/stable/) library. This opens up the possibility to release models trained on sensitive data to the public.
4. **Context enhancement:** Extract a sentence from the note and add tokens (from the sentences adjacent to the extracted sentence) on either side of the extracted sentence until we have a sequence of 512 sub-tokens. The reason for including context tokens was to provide additional context, especially for peripheral tokens in a given sequence.
5. **Custom clinical tokenizer:** Includes medically relevant regular expressions and abbreviations based on the structure and information generally found in medical notes. This tokenizer resolves common typographical errors and missing spaces that occur in clinical notes.

Since de-identification is a sequence labeling task, this project can be used for other sequence labeling tasks.
More details on how to use the project, the format of data and other useful information is presented in future sections.

</details>

## Installation
*This section provides information on how to install dependencies and set up the project.*

<details>
<summary>Click to expand</summary>

### Source

* Git clone the repository
* Install the dependencies using conda or pip.
* We developed this project using the conda environment specified in [deid.yml](./deid.yml). You can create the environment using this file, and it will install the required dependencies.

```shell
git clone git@github.com:obi-ml-public/ehr_deidentification.git
conda env create -f deid.yml
conda activate deid
```

### Pip

* You can install the **robust_deid** package to use the tools and models for de-identification of text.

#### Option 1:
- Update conda environment file ([deid.yml](./deid.yml)): Add *robust_deid* to the environment file under the pip section.
- Create and activate conda environment
- This will install the dependencies and the package in the conda environment

```shell
vi deid.yml # Update env file
conda env create -f deid.yml
conda activate deid
```

#### Option 2:
- Using only pip.
- Install the *robust_deid* package and the dependencies using pip install along with the [requirments.txt](./requirements.txt) file

```shell
pip install robust_deid -r requirments.txt
```

#### Option 3:
- Install the dependencies using the conda environment ([deid.yml](./deid.yml)) described in the previous section.
- pip install the package

```shell
conda env create -f deid.yml
conda activate deid
pip install robust_deid
```
    

</details>

</details>

---

# Dataset Creation
*This section provides information on how the datasets were annotated, the size of the datasets and the distribution of PHI in the datasets.*

<details>
<summary>Click to expand</summary>

## Annotation guidelines
* The guidelines for the dataset annotation and prodigy setup can be found here: 
[Annotation Guidelines](data/AnnotationGuidelines.md)
  
## Dataset Information
  
* Information about the distribution of PHI and size of the datasets can be found here: [Datasets](data/Datasets.md)

</details>

---

# Training
*This section provides information about the training data, the speed and size of training elements.*
*It is useful for people who want to learn more about the model inputs, objective, architecture, development, training/evaluation/prediction procedure and compute infrastructure.*

<details>
<summary>Click to expand</summary>

## Training Data
*This section provides a high-level overview of the training data. It is relevant for anyone who wants to know the basics of what the model is learning.*

<details>
<summary>Click to expand</summary>

### Overview

-   Language: English
-   Data: Medical notes from the i2b2 2014 cohort [[Stubbs and Uzuner, 2015]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4978170/) and the Mass General Brigham Network (notes from 11 institutes).
- Detailed description of the data, and the distribution of entities can be found here: [Datasets](data/Datasets.md)
-   4 training datasets (one model trianed on each of these datasets):
    1. i2b2 dataset (public dataset - private information has been replaced by the authors/annotators).
    2. Augmented i2b2 dataset.
    3. i2b2 + MGB dataset (contains private data, hence model cannot be released to the public).
    4. Augmented i2b2 + MGB dataset (private data is replaced, hence model can be released to the public).
- To create the augmented version of a dataset we replaced the annotated private information in the dataset with entities generated using [Faker](https://faker.readthedocs.io/en/stable/).

### Dataset Splits

* We used the [dataset_splitter.py](src/robust_deid/dataset_splitter.py) script to create the train and validation datasets.
* We used the script to create the dataset splits. The parameters that we ran the script with can be found here: [train_val_splits.sh](./run/dataset/train_val_splits.sh)

</details>

## Preprocessing
*This section talks about the preprocessing steps.*
*Relevant for those that want to understand how the notes were split and tokenized to fit into the model*

<details>
<summary>Click to expand</summary>

### Data Format

* The data is in the json format, where we store the notes in a jsonl file. Each line in this file is a json object that refers to one sequence.
* Since we had datasets that contained medical notes that would not fit into the model without truncation, we created chunks of size 500 subword tokens that would fit into the model.
* Essentially we are training the de-identification model on sequence chunks from the note as opposed to using the entire note (entire notes would need truncation). However, we can still de-identify the entire note at test time by aggregating the predictions on the chunked sequences back to the note level.
* The format after splitting into chunks was like this:
```json
{ 
  "sentence_text": "Physician Discharge Summary Admit date: 10/12/1982 Discharge date: 10/22/1982 Patient Information Jack Reacher, 54 y.o. male (DOB = 1/21/1928) ...", 
  "current_chunk_start": 20,
  "current_chunk_end": 192, 
  "global_start": 6,
  "spans": [{"id":"0", "start": 40, "end": 50, "label": "DATE"}, {"id":"1", "start": 67, "end": 77, "label": "DATE"}, {"id":"3", "start": 98, "end": 110, "label": "PATIENT"}, {"id":"3", "start": 112, "end": 114, "label": "AGE"}, {"...": "..."}]
}
```
* As long as the input data to the sequence tagger is in this format, the sequence tagger code should work without any errors.
* The global start field is needed to reconstruct the original note from the chunks. This is used when running predictions. We don't need this field for training and evaluation.
* The [sequence_dataset.py](src/robust_deid/sequence_dataset.py) script can be used to create this chunked dataset, given a collection of notes/documents.

### Chunking

* As mentioned, we had datasets that contained medical notes that would not fit into the model without truncation, we chunked the data.
* To chunk the data we first split the note into sentences, word tokenized these sentences and finally subword tokenized these sentences.
* To create the chunk, we took a sentence and took all the adjacent tokens around it until we reached a sequence of 500 sub-word tokens. This was done for every sentence.
* Based on the start and end positions of these chunks, we get the text of the sequence, and the spans associated with the chunked sequence.
* Essentially we are training the de-identification model on sequence chunks from the note as opposed to using the entire note (entire notes would need truncation). However, we can still de-identify the entire note at test time by aggregating the predictions on the chunked sequences back to the note level.
* For more information, refer to the following scripts: [sequence_dataset.py](src/robust_deid/sequence_dataset.py) and [sequence_chunker.py](src/robust_deid/sequence_datasets/sequences/sequence_chunker.py)
* During evaluation however, we only evaluate on the tokens in the current sentence and not on the added on tokens. The added on tokens are present in the sequence and are used as additional context only.
* We don't evaluate on the added on contextual tokens because we care about note level performance as opposed to sequence level performance. By evaluating only on the current sentence in the note we are calculating metrics for each token just once, effectively evaluating at the note level. 
* Similar approach during predict, we only consider predictions on the current sentence, so that we have one single prediction for a given token in the note. Then we can aggregate these predictions back to the note level.
* We've explained chunking during evaluation and predict in the future sections.
* Example:
    - Note: 20 tokens
    - Sentences: 3 sentences
        - Sentence 1: 5 tokens
        - Sentence 2: 7 tokens
        - Sentence 3: 8 tokens
    - Max tokens (Sequence length): 10 tokens

    - Based on these configurations we get:
        - Sequence 1: 5 tokens from sentence 1 and 5 tokens from sentence 2
        - Sequence 2: 7 tokens from sentence 1, 1 tokens from sentence 1 and 2 tokens from sentence 2
        - Sequence 3: 8 tokens from sentence 3 and 2 tokens from sentence 2

    - The datasets now consists of 3 sequences.
    - Training: Train on all tokens in all 3 sequences
        - Sequence 1: Trained on all 10 tokens
        - Sequence 2: Trained on all 10 tokens
        - Sequence 3: Trained on all 10 tokens
    - Evaluation/Predict: Evaluate/Predict only on the current sentence:
        - Sequence 1: Evaluate/Predict only on the 5 tokens from sentence 1
        - Sequence 2: Evaluate/Predict only on the 7 tokens from sentence 2
        - Sequence 3: Evaluate/Predict only on the 8 tokens from sentence 3
        - We've evaluated/predicted on the 20 tokens (evaluated/predicted each token only once)
> *This step is optional and depends on the size of your data/sequences. If the data contains sequences that do not exceed the model max length, you can skip this step.*

### Sentencizer
The medical notes are split into chunks of 500 sub-word tokens, and the model is trained on these chunks. 
Since DeBERTa can handle a maximum sequence length of 512 tokens, we split the notes into chunks (< 512). 
In the simplest case, a chunk is a sentence from the note. 
We took this approach of extracting a sentence and packing it with surrounding tokens for additional context.

- Sentencizer: The dataset was sentencized with the en_core_sci_sm sentencizer from [Scispacy](https://allenai.github.io/scispacy/).
- 500 Length Chunks: Extract a sentence from the note and add tokens (from the sentences adjacent to the extracted sentence) on either side of the extracted sentence until we have a sequence of 500 sub-tokens.
- You can think of this as a sliding window approach where the window (stride) is dynamic, i.e. we move the window from one sentence to the next.
- *This step is used only when chunking the dataset*

### Tokenization

Two-step process. Word tokenization followed by sub-word tokenization.

- Word-level tokenization: Custom spacy tokenizer (additional medically relevant regexes and abbreviations) built on top of the en_core_sci_sm tokenizer from [Scispacy](https://allenai.github.io/scispacy/).
- The custom tokenizer can be found here: [tokenizer-0.0.1](./tokenizer-0.0.1) and the code to build this tokenizer can be found here: [create_tokenizer.py](./create_tokenizer.py) and [custom_tokenizer](./custom_tokenizer).
- Labels are assigned to word level tokens and private information is at the token level.
- Sub-word tokenization: Apply the byte-level Byte Pair Encoding (BPE) algorithm defined by DeBERTa on the split word level tokens.
- We do not train on all subword tokens, we only use the first subword of the word level token to update the model weights.
- Tokenization can be applied on the fly if the user wishes.
- This step is used when chunking the dataset and also when feeding the chunked dataset to the model for training/evaluation/testing.
- The input the model is always in text format (format is shown in the earlier section), so we use this tokenizer to word tokenize and sub-word tokenize the text before feeding it into the model.

### Augmentation

* We built a pipeline to augment any private information, i.e. replace any private information in the data with randomly generated entities.
* This was using the [Faker](https://faker.readthedocs.io/en/stable/) library. We also used the [PHICON](https://github.com/betterzhou/PHICON) repository to generate hospital and company names.
* These libraries were used to generate fake names, locations, dates, id etc (fake PHI). By doing so, we are able to remove replace private information in the notes with generated entities.
* Augmentation lets us release models that have been trained on private data to the public since the private information has been replaced.
* The augmentation pipeline and rules can be found in the scripts present in the following folder: [Augmentations](src/robust_deid/sequence_datasets/text_transformations/augmentations/phi).
* The augmentation rules vary for each type of protected health information (PHI).
* Augmentations can be applied on the fly. An advantage of applying augmentations on the fly is that a note with a set of PHI is only ever seen once, since we replace a given note with different entities in every epoch of the training process. This gives an illusion of the presence of a large collection of notes and thus we can train the models for longer.

</details>

## Trained Models
*This section talks about the models that were trained and how they were trained.*
*It is useful for anyone who wants to know what models were trained, and how they can train, evaluate and test (how to de-identify notes with a trained model) their own models.*

<details>
<summary>Click to expand</summary>

### Overview

* We trained a total of 4 models as part of this project. All 4 models are DeBERTa (see [paper](https://arxiv.org/abs/2006.03654)) based models.
* DeBERTa Encoder-Decoder architecture with a token classification head. The token classification head is a linear classification layer that outputs scores for each named entity/class (protected health information entities).
* **Objective Function:** Cross Entropy with mean reduction (see [API documentation](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html#torch.nn.CrossEntropyLoss)).
* The models are token classification model built to identify tokens that contain private information (named entity recognition).
* A token classification model along with a NER notation (e.g. BIO, BILOU etc.) can be used to identify spans from token labels. Spans are a collection of tokens that represent some protected health information (PHI) entity.
* Each model was trained with a different training dataset.
    1. **Model 1 ([obi/deberta_deid_no_augment_i2b2](https://huggingface.co/obi/deberta_deid_no_augment_i2b2))**: DeBERTa based de-identification model trained with the i2b2 dataset.
    2. **Model 2 ([obi/deberta_deid_i2b2](https://huggingface.co/obi/deberta_deid_i2b2))**: DeBERTa based de-identification model trained with the augmented i2b2 dataset.
    3. **Model 3**: DeBERTa based de-identification model trained with the MGB dataset (contains private data and cannot be released to the public).
    4. **Model 4 ([obi/deberta_deid_i2b2_mgb](https://huggingface.co/obi/deberta_deid_i2b2_mgb))**: DeBERTa based de-identification model trained with the augmented MGB dataset (private data is replaced and can be released to the public).
* The [sequence_tagger.py](src/robust_deid/sequence_tagger.py) script was used to train the models. The following shell script contains all the training calls: [train.sh](./run/model/train.sh)
* While we update our documentation and readme, this script should serve as a good starting point to train, evaluate and test your own models/datasets.
* The config files for each of these models can be found in the [train config_files](./config_files/custom/train) folder. The config files contain information about the learning rate, warmup, batch size etc.

> *More details about the models can be found in the model cards on HuggingFace (click on model links).*

### Model 1
* The model is available on HuggingFace: [obi/deberta_deid_no_augment_i2b2](https://huggingface.co/obi/deberta_deid_no_augment_i2b2)
* Trained with 713 i2b2 notes which are chunked into 29587 sequences.
* The PHI tokens are not augmented.

### Model 2
* The model is available on HuggingFace: [obi/deberta_deid_i2b2](https://huggingface.co/obi/deberta_deid_i2b2)
* Trained with 713 i2b2 notes which are chunked into 29587 sequences. 
* The PHI tokens are augmented. The augmentations are applied on the fly (the sequences are different every epoch).

### Model 3
* The model has not been made available since it has been trained on private data.
* Trained with 713 i2b2 notes and 1150 MGB notes which are chunked into 82917 sequences. 
* The PHI tokens are not augmented. 

### Model 4
* The model is available on HuggingFace: [obi/deberta_deid_i2b2_mgb](https://huggingface.co/obi/deberta_deid_i2b2_mgb)
* Trained with 713 i2b2 notes and 1150 MGB notes which are chunked into 82917 sequences. 
* The PHI tokens are augmented, and the private data has been replaced. The augmentations are applied on the fly (the sequences are different every epoch).

> *If you wish to train your own models, you can do so by following the steps in this notebook: [Train](./Train.ipynb)*

> *If you wish to evaluate a trained model, you can do so by following the steps in this notebook: [Eval](./Eval.ipynb)*

> *If you wish to de-identify notes using a trained model, you can do so by following the steps in this notebook: [Predict](./Predict.ipynb)*

</details>

## Technical Specifications

*This section includes details about compute infrastructure.*

<details>
<summary>Click to expand</summary>

### Compute infrastructure

#### Hardware

* 8 Tesla V100-SXM2-32GB GPUs (1 Node)
    
* 8 GPUs using NVLink

* CPU: Intel

* CPU memory: 512GB per node

* GPU memory: 256GB per node

#### Software

* PyTorch (pytorch-1.11.0 w/ CUDA-11.3.1; see [Github link](https://github.com/pytorch/pytorch))

* NVIDIA Apex ([Github link](https://github.com/NVIDIA/apex))
    
</details>

</details>

---

# Evaluation
*This section describes the evaluation protocols and provides the results of the trained models.*

<details>
<summary>Click to expand</summary>

## Metrics 
*This section describes the different ways performance is calculated and why.*

<details>
<summary>Click to expand</summary>

Includes:

| Metric             | Why chosen                                                         |
|--------------------|--------------------------------------------------------------------|
| [F1](https://en.wikipedia.org/wiki/F-score) | Quantifies the amount of PHI being captured and the amount of entities falsely captured as PHI |
| [Recall](https://en.wikipedia.org/wiki/Precision_and_recall) | Standard objective for computing how much PHI has been identified|
| [Precision](https://en.wikipedia.org/wiki/Precision_and_recall) | Standard objective for computing how much non-PHI has been identified as PHI |

Multiple metrics are computed. F1, precision, recall scores are computed for each entity individually (i.e. we have scores for names, ages etc.). Micro, macro and Binary (PHI v/s Non-PHI) averaged scores are also computed.

</details>

## Datasets
*This section contains information about the test datasets*

<details>
<summary>Click to expand</summary>

* Detailed description of the test data, and the distribution of entities can be found here: [Datasets](data/Datasets.md)

</details>

##  Results
*This section contains the results on the test datasets*

<details>
<summary>Click to expand</summary>

**De-Identification Results:**

*TODO: Forthcoming*

**Downstream Results:**

*TODO: Forthcoming*

</details>

</details>

---

# Uses

*This section addresses questions around how the models/scripts is intended to be used, discusses the foreseeable users of the model (including those affected by it), and describes uses that are considered out of scope.*
*It is useful for anyone who is considering using the models/scripts or who is affected by the project.*

<details>
<summary>Click to expand</summary>
    
## How to use
*This section goes through how to use and deploy this project. It is usefel for anyone who wants to know how to train and evaluate the model, and how to use the model to de-identify documents/notes.*

<details>
<summary>Click to expand</summary>

### Training

* Follow the steps in this notebook to train your own models: [Train](./Train.ipynb)

### Evaluation
* Follow the steps in this notebook to evaluate a trained model: [Eval](./Eval.ipynb)

### Predict

* Follow the steps in this notebook to de-identify notes using a trained model: [Predict](./Predict.ipynb)
* You can also take a look at our HuggingFace space: [Medical Note Deidentification](https://huggingface.co/spaces/obi/Medical-Note-Deidentification) to see how the model is used.

</details>

## Intended Use

*This section addresses how we intend the model to be used and what use cases are considered out-of-scope.*

<details>
<summary>Click to expand</summary>

This project was created in order to de-identify medical notes (i.e. remove protected health information) to facilitate research. De-identification of notes can enable institutes to share notes amongst other institutions while protecting the privacy of their patients. Learning from a larger collection of notes can be more beneficial as compared to learning from a limited set of medical text from a single institution.

### Direct Use

-   De-identification of medical notes. Removing private information (PHI) from medical notes.

### Downstream Use

-   The de-identification pipeline can be the first step in a downstream task (e.g. disease classification) where the de-identification model is used to remove private information from the notes being used in the downstream task.
-   Removing private information from the downstream tasks will allow researchers to publish their models to the public.

### Out-of-scope Uses

* There is no guarantee that the de-identification pipeline will identify all the protected health information.
* If the pipeline is being used in a high stakes setting, additional care needs to be taken to ensure patient data is not being leaked.
* Additional care can be taken, by adding handcrafted rules to identify the PHI or varying classification thresholds to increase recall  
* Intentionally using the model for harm, violating human rights, or other kinds of malicious activities, is a misuse of this model.

### Intended Users

-   General Public

-   Healthcare Institutes

-   Researchers

-   Students

-   Educators

-   Engineers/developers

</details>

</details>

---

# Limitations

*This section addresses some current limitations of the project.*
*While we continue to address and overcome some of these limitations, we are always welcome to suggestions and collaboration.*
*We encourage the community to give us feedback and also address some limitations. Thanks!*

<details>
<summary>Click to expand</summary>

* Model may:

    -   Not identify all the protected health information

    -   Contain stereotypes
  
    -   Contain personal information

    -   Make errors, missing private information or tagging non-private data as PHI
    
* Model has not tested on a truly external dataset (e.g. healthcare provider outside Boston or outside the US) due to lack of availability.

* Integrating the model with additional handcrafted rules to increase recall (prevent the leak of PHI).

* Always room for improvement in terms of speed and memory efficiency. There are a few steps that are redundantly applied on-the-fly instead of being applied just once. We hope to remove this bottleneck.

* Speed up the text transformations (tokenization, label alignment etc.) 
  
* Augmented Models:
  
    * Augmentations may not cover every possible edge case. Improving augmentations may improve performance of the augmented models.
    * Training with augmentations, lets us train the model for longer (since the PHI is always being replaced with new data), but there could be a possibility the model may start to over-fit on non-phi text. Running augmentations (e.g. replacing words with their synonyms) on non-phi text may help resolve this. Refer [PHICON](https://github.com/betterzhou/PHICON).
    * Augmentations currently don't maintain consistency (e.g. a given note can have different patient names for the same patient), while this doesn't seem to affect performance, it would be nice to have augmentations that have some consistency. More so for model predictions, than for training. By consistency, we refer to having the augmentation pipeline generate the same patient name for a given note, dates that are in the right timeline or ages that correspond the dates/patient.
    * While Faker has a good diversity of augmentations, we can always try to improve the diversity of our augmentations.
    

</details>

---