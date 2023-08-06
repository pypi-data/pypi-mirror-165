from ..logging_system import logger
from .trigger import equip

##########################################################################################################################################
from ._base_policy import initialization_policy
from .tabular_mlops import TabularMLOps

class Project(TabularMLOps):
    def __init__(self, local_environment:dict=None):
        if local_environment is None:
            local_environment = dict()
            local_environment['root'] = input('[TabularMLOps:Root]:')
            local_environment['feature_store'] = input('[TabularMLOps:FeatureStore]:')
            local_environment['model_registry'] = input('[TabularMLOps:ModelRegistry]:')
            local_environment['source_repository'] = input('[TabularMLOps:SourceRepository]:')
            local_environment['metadata_store'] = input('[TabularMLOps:MetadataStore]:')
        elif isinstance(local_environment, dict):
            keys = local_environment.keys()
            assert 'root' in keys, 'The local_environment must include the root.'
            assert 'feature_store' in keys, 'The local_environment must include path of the feature_store.'
            assert 'model_registry' in keys, 'The local_environment must include path of the model_registry.'
            assert 'source_repository' in keys, 'The local_environment must include path of the source_repository.'
            assert 'metadata_store' in keys, 'The local_environment must include path of the metadata_store.'
        else:
            local_environment = None

        super(Project, self).__init__(initialization_policy(local_environment))

    def __enter__(self):
        logger['mlops'].info('{:_^100}'.format('TabularMLOps START'))
        return self

    def __exit__(self, exit_type, exit_value, exit_traceback):
        logger['mlops'].info('{:_^100}'.format('TabularMLOps CLOSE'))


##########################################################################################################################################


