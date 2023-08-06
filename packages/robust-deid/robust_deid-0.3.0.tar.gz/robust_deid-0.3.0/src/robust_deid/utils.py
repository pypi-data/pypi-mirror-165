import json
import logging
import sys
from pathlib import Path
from typing import NoReturn, Sequence, List

import datasets
import transformers
from faker import Faker
from transformers import (
    TrainingArguments
)

from .deidentification import DeidentificationLevel
from .sequence_datasets.text_transformations.augmentations.noise import CharacterNoiseAugment
from .sequence_datasets.text_transformations.augmentations.phi import AugmentType
from .sequence_datasets.text_transformations.augmentations.phi import (
    PatientAugment,
    StaffAugment,
    AgeAugment,
    PhoneAugment,
    EmailAugment,
    PatorgAugment,
    HospitalAugment,
    IDAugment,
    OtherPHIAugment,
    LocationAugment,
    DateAugment,
    PHIAugmenter,
)


def setup_logging(logger, log_level: int) -> NoReturn:
    """
    Function sets up the log level and format.

    Args:
        logger (): TO-DO
        log_level (int): The numeric value of the log level.

    """
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        level=log_level
    )
    logger.setLevel(log_level)
    datasets.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()


def log_training_args(training_args: TrainingArguments) -> NoReturn:
    """
    Log the training argument values.

    Args:
        training_args (TrainingArguments): The training arguments.

    """
    # Log on each process the small summary:
    logging.warning(
        f"Process rank: {training_args.local_rank}, device: {training_args.device}, n_gpu: {training_args.n_gpu}"
        + f"distributed training: {bool(training_args.local_rank != -1)}, 16-bits training: {training_args.fp16}"
    )
    # Set the verbosity to info of the Transformers logger (on main process only):
    logging.info(f"Training/evaluation parameters {training_args}")


def get_augment_type(augment_type: str):
    """
    Get the augment type enum based on the input string

    Args:
        augment_type (str): The type of augmentation

    Returns:
        (AugmentType): The corresponding augment type enum

    """
    if augment_type == 'random':
        return AugmentType.RANDOM
    elif augment_type == 'mimic':
        return AugmentType.MIMIC
    elif augment_type == 'mimic_probability':
        return AugmentType.MIMIC_PROBABILITY
    else:
        raise ValueError('Invalid augment type')


def get_deidentification_level_type(deidentification_level: str):
    """
    Get the deidentification level enum based on the input string

    Args:
        deidentification_level (str): The type of deidentification level

    Returns:
        (DeidentificationLevel): The corresponding deidentification level enum

    """
    if deidentification_level == 'exact':
        return DeidentificationLevel.EXACT
    elif deidentification_level == 'relaxed':
        return DeidentificationLevel.RELAXED
    else:
        raise ValueError('Invalid augment type')


def get_ner_augmenter(text_tokenizer, notation, augment_type):
    # Setup Faker
    locales = ['en', 'en_AU', 'en_CA', 'en_GB', 'en_IE', 'en_IN', 'en_NZ', 'en_PH', 'en_TH', 'en_US']
    fake = Faker(locales, use_weighting=False)

    organizations_list = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                                 '/augmentations/phi/patorg.txt'
    organizations = [line.strip() for line in open(organizations_list)]
    # Setup the augment objects
    patient_augment = PatientAugment(fake)
    staff_augment = StaffAugment(fake)
    age_augment = AgeAugment(fake)
    phone_augment = PhoneAugment(fake)
    email_augment = EmailAugment(fake)
    patorg_augment = PatorgAugment(fake, organizations)
    id_augment = IDAugment(fake)
    other_phi_augment = OtherPHIAugment(fake)
    location_augment = LocationAugment(fake)
    date_augment = DateAugment(fake)
    hospital_augment = get_hospital_augment(fake, id_augment, location_augment)
    # Create the augmenter
    return PHIAugmenter(
        text_tokenizer=text_tokenizer,
        notation=notation,
        augment_type=get_augment_type(augment_type),
        patient_augment=patient_augment,
        staff_augment=staff_augment,
        age_augment=age_augment,
        phone_augment=phone_augment,
        email_augment=email_augment,
        hospital_augment=hospital_augment,
        patorg_augment=patorg_augment,
        id_augment=id_augment,
        other_phi_augment=other_phi_augment,
        location_augment=location_augment,
        date_augment=date_augment,
    )


def get_hospital_augment(fake, id_augment, location_augment):
    acronyms = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                       '/augmentations/phi/hospital/acronyms.json'
    assisted_living = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                              '/augmentations/phi/hospital/assisted_living.json'
    locations = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                        '/augmentations/phi/hospital/locations.json'
    location_ids = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                           '/augmentations/phi/hospital/location_ids.json'
    ids = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                  '/augmentations/phi/hospital/ids.json'
    pharmacies = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                         '/augmentations/phi/hospital/pharmacies.json'
    hospitals = Path(__file__).parent / 'sequence_datasets/text_transformations' \
                                        '/augmentations/phi/hospital/hospitals_full.json'

    def get_json_object(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    acronyms = get_json_object(acronyms)
    assisted_living = get_json_object(assisted_living)
    locations = get_json_object(locations)
    location_ids = get_json_object(location_ids)
    ids = get_json_object(ids)
    pharmacies = get_json_object(pharmacies)
    hospitals = get_json_object(hospitals)

    return HospitalAugment(
        fake=fake,
        id_augment=id_augment,
        location_augment=location_augment,
        acronyms=acronyms,
        assisted_living=assisted_living,
        locations=locations,
        location_ids=location_ids,
        ids=ids,
        pharmacies=pharmacies,
        hospitals=hospitals,
        randomize=True
    )


def get_character_noise_augmenter(text_tokenizer, noise):
    return CharacterNoiseAugment(text_tokenizer=text_tokenizer, noise=noise)


def unpack_nested_list(nested_list: Sequence[Sequence[str]]) -> List[str]:
    """
    Use this function to unpack a nested list.

    Args:
        nested_list (Sequence[Sequence[str]]): A nested list.

    Returns:
        (List[str]): Flattened list.

    """
    return [inner for nested in nested_list for inner in nested]
