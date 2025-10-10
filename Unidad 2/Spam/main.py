from needs.spam_detector import SpamVerifier
from needs.dataset import EXAMPLE_DATASET

if __name__ == "__main__":
    verifier = SpamVerifier(threshold=3.0)
    verifier.evaluate(EXAMPLE_DATASET)
