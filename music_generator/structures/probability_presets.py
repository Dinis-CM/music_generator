PROBABILITY_PRESETS_TABLE = {
    "Uniform": lambda track: track.set_discrete_uniform_probabilities(),
    "First Only": lambda track: track.set_first_only_probability(),
    "Last Only": lambda track: track.set_last_only_probability(),
    "Binomial, p=0.1": lambda track: track.set_binomial_probabilities(0.1),
    "Binomial, p=0.2": lambda track: track.set_binomial_probabilities(0.2),
    "Binomial, p=0.3": lambda track: track.set_binomial_probabilities(0.3),
    "Binomial, p=0.4": lambda track: track.set_binomial_probabilities(0.4),
    "Binomial, p=0.5": lambda track: track.set_binomial_probabilities(0.5),
    "Binomial, p=0.6": lambda track: track.set_binomial_probabilities(0.6),
    "Binomial, p=0.7": lambda track: track.set_binomial_probabilities(0.7),
    "Binomial, p=0.8": lambda track: track.set_binomial_probabilities(0.8),
    "Binomial, p=0.9": lambda track: track.set_binomial_probabilities(0.9)
}