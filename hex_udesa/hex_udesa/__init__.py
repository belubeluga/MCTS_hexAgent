from gymnasium.envs.registration import register

register(
    id="hex_udesa/Hex-v0",
    entry_point="hex_udesa.envs:HexEnv",
)
