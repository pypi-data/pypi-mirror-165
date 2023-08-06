from .name_augment import NameAugment


class PatientAugment(NameAugment):

    def __init__(self, fake):
        super().__init__(fake)
