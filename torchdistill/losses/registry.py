from ..common import misc_util

LOSS_DICT = misc_util.get_classes_as_dict('torch.nn.modules.loss')
HIGH_LEVEL_LOSS_DICT = dict()
LOSS_WRAPPER_DICT = dict()
MIDDLE_LEVEL_LOSS_DICT = dict()
FUNC2EXTRACT_MODEL_OUTPUT_DICT = dict()


def register_high_level_loss(arg=None, **kwargs):
    def _register_high_level_loss(cls_or_func):
        key = kwargs.get('key')
        if key is None:
            key = cls_or_func.__name__

        HIGH_LEVEL_LOSS_DICT[key] = cls_or_func
        return cls_or_func

    if callable(arg):
        return _register_high_level_loss(arg)
    return _register_high_level_loss


def register_loss_wrapper(arg=None, **kwargs):
    def _register_loss_wrapper(cls_or_func):
        key = kwargs.get('key')
        if key is None:
            key = cls_or_func.__name__

        LOSS_WRAPPER_DICT[key] = cls_or_func
        return cls_or_func

    if callable(arg):
        return _register_loss_wrapper(arg)
    return _register_loss_wrapper


def register_mid_level_loss(arg=None, **kwargs):
    def _register_mid_level_loss(cls_or_func):
        key = kwargs.get('key')
        if key is None:
            key = cls_or_func.__name__

        MIDDLE_LEVEL_LOSS_DICT[key] = cls_or_func
        return cls_or_func

    if callable(arg):
        return _register_mid_level_loss(arg)
    return _register_mid_level_loss


def register_func2extract_model_output(arg=None, **kwargs):
    def _register_func2extract_model_output(func):
        key = kwargs.get('key')
        if key is None:
            key = func.__name__

        FUNC2EXTRACT_MODEL_OUTPUT_DICT[key] = func
        return func

    if callable(arg):
        return _register_func2extract_model_output(arg)
    return _register_func2extract_model_output


def get_loss(key, **kwargs):
    if key in LOSS_DICT:
        return LOSS_DICT[key](**kwargs)
    raise ValueError('No loss `{}` registered'.format(key))


def get_high_level_loss(criterion_config):
    criterion_key = criterion_config['key']
    args = criterion_config.get('args', None)
    kwargs = criterion_config.get('kwargs', None)
    if args is None:
        args = list()
    if kwargs is None:
        kwargs = dict()
    if criterion_key in HIGH_LEVEL_LOSS_DICT:
        return HIGH_LEVEL_LOSS_DICT[criterion_key](*args, **kwargs)
    raise ValueError('No high-level loss `{}` registered'.format(criterion_key))


def get_loss_wrapper(mid_level_loss, criterion_wrapper_config):
    wrapper_key = criterion_wrapper_config['key']
    args = criterion_wrapper_config.get('args', None)
    kwargs = criterion_wrapper_config.get('kwargs', None)
    if args is None:
        args = list()
    if kwargs is None:
        kwargs = dict()
    if wrapper_key in LOSS_WRAPPER_DICT:
        return LOSS_WRAPPER_DICT[wrapper_key](mid_level_loss, *args, **kwargs)
    raise ValueError('No loss wrapper `{}` registered'.format(wrapper_key))


def get_mid_level_loss(mid_level_criterion_config, criterion_wrapper_config=None):
    loss_key = mid_level_criterion_config['key']
    mid_level_loss = MIDDLE_LEVEL_LOSS_DICT[loss_key](**mid_level_criterion_config['kwargs']) \
        if loss_key in MIDDLE_LEVEL_LOSS_DICT else get_loss(loss_key, **mid_level_criterion_config['kwargs'])
    if criterion_wrapper_config is None or len(criterion_wrapper_config) == 0:
        return mid_level_loss
    return get_loss_wrapper(mid_level_loss, criterion_wrapper_config)


def get_func2extract_model_output(key):
    if key is None:
        key = 'extract_model_loss_dict'
    if key in FUNC2EXTRACT_MODEL_OUTPUT_DICT:
        return FUNC2EXTRACT_MODEL_OUTPUT_DICT[key]
    raise ValueError('No function to extract original output `{}` registered'.format(key))
