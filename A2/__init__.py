import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)
register(
    id='A2Env-v0',
    entry_point='A2.env:A2Env',
)
