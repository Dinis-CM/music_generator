PROBABILITY_PRESETS_TABLE = {
    "Uniform": lambda track: track.set_discrete_uniform_probabilities(),
    "Zero": lambda track: track.set_zero_probabilities(),
    "First Only": lambda track: track.set_first_only_probability(),
    "Last Only": lambda track: track.set_last_only_probability(),
    "Random": lambda track: track.set_random_probabilities(),
}