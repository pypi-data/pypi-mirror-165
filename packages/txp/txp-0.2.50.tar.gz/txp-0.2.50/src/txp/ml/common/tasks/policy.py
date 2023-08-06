from abc import ABC, abstractmethod
from joblib import dump, load
from dataclasses import dataclass


@dataclass
class PolicyStorage:
    handler: any
    trained: bool
    accuracy: float


class Policy(ABC):

    def __init__(self, policy_file=None):

        if policy_file is not None:
            print(f"Restoring policy from {policy_file}")
            self.clf = load(policy_file)
            self.trained = True
        else:
            self.trained = False
            self.clf = None
        self.accuracy = -1

    @abstractmethod
    def train(self, dataset, target, test_size=0.3):
        pass

    @abstractmethod
    def predict(self, tensor):
        pass

    @abstractmethod
    def name(self):
        pass

    def save(self) -> PolicyStorage:
        return PolicyStorage(self.clf, self.trained, self.accuracy)

    def load(self, policy_storage: PolicyStorage):
        print("Restoring policy")
        self.clf = policy_storage.handler
        self.trained = policy_storage.trained
        self.accuracy = policy_storage.accuracy

    def is_trained(self):
        return self.trained
