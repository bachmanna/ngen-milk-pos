from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

rate_cache = cache.get_cache('rate.cache', type='memory', expire=3600)
settings_cache = cache.get_cache('settings.cache', type='memory', expire=3600)