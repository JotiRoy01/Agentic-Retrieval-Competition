import sys
sys.path.insert(0, 'src')

from agentic.entity.config_entity import ConfigEntity

config = ConfigEntity.load_config()
print("Data directories:", config.data_dir)