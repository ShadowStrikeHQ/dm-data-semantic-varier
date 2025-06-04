import argparse
import logging
import random
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Security best practice: Define a whitelist of allowed faker locales to prevent malicious injection.
ALLOWED_LOCALES = ['en_US', 'en_GB', 'fr_FR', 'de_DE']


def setup_argparse():
    """
    Sets up the argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(
        description="Subtly alters the meaning of data by replacing words or phrases with synonyms or paraphrases.  Preserves the general sense of the information while hindering precise identification."
    )

    parser.add_argument("input_string",
                        help="The input string to be semantically varied.")
    parser.add_argument("-n", "--num_variations", type=int, default=1,
                        help="The number of variations to generate (default: 1).")
    parser.add_argument("-l", "--locale", type=str, default='en_US',
                        help="The Faker locale to use (e.g., en_US, fr_FR).  Must be in the whitelist.")
    parser.add_argument("-s", "--seed", type=int,
                        help="Optional seed for the random number generator, to ensure reproducibility.")
    parser.add_argument("--word_replacement_probability", type=float, default=0.3,
                        help="The probability of replacing each word with a synonym (default: 0.3).")

    return parser


def replace_word_with_synonym(word, fake):
    """
    Replaces a word with a synonym using Faker. This is a very basic
    implementation for demonstration purposes.  A more robust implementation
    would use a proper thesaurus or word embedding model.

    Args:
        word (str): The word to replace.
        fake (Faker): The Faker instance.

    Returns:
        str: A synonym for the word, or the original word if no synonym is found or replacement fails.
    """
    try:
        # Basic synonym replacement using Faker's random elements.  This is illustrative only.
        synonyms = [fake.word(), fake.word(), fake.word()]  # Get a few random words
        if synonyms:
            return random.choice(synonyms)
        else:
            return word  # Return original word if no synonyms are available
    except Exception as e:
        logging.error(f"Error replacing word '{word}': {e}")
        return word


def generate_semantic_variation(input_string, fake, word_replacement_probability):
    """
    Generates a semantically varied version of the input string.

    Args:
        input_string (str): The string to vary.
        fake (Faker): The Faker instance.
        word_replacement_probability (float): Probability of replacing each word

    Returns:
        str: The semantically varied string.
    """
    words = input_string.split()
    varied_words = []
    for word in words:
        if random.random() < word_replacement_probability:
            varied_words.append(replace_word_with_synonym(word, fake))
        else:
            varied_words.append(word)
    return " ".join(varied_words)


def validate_locale(locale):
    """
    Validates the given locale against the allowed locales.
    """
    if locale not in ALLOWED_LOCALES:
        raise ValueError(f"Locale '{locale}' is not allowed.  Allowed locales are: {ALLOWED_LOCALES}")


def main():
    """
    Main function to parse arguments, generate variations, and print results.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        validate_locale(args.locale)
        fake = Faker(args.locale)

        if args.seed is not None:
            random.seed(args.seed)
            fake.seed_instance(args.seed)  # Also seed Faker

        for _ in range(args.num_variations):
            variation = generate_semantic_variation(args.input_string, fake, args.word_replacement_probability)
            print(variation)

    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        sys.exit(1)
    except Exception as e:
        logging.exception("An unexpected error occurred:")
        sys.exit(1)


if __name__ == "__main__":
    main()