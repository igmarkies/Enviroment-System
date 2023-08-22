# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.1
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _sensirion_gas_index_algorithm_wrap
else:
    import _sensirion_gas_index_algorithm_wrap

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


true = _sensirion_gas_index_algorithm_wrap.true
false = _sensirion_gas_index_algorithm_wrap.false
LIBRARY_VERSION_NAME = _sensirion_gas_index_algorithm_wrap.LIBRARY_VERSION_NAME
GasIndexAlgorithm_ALGORITHM_TYPE_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_ALGORITHM_TYPE_VOC
GasIndexAlgorithm_ALGORITHM_TYPE_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_ALGORITHM_TYPE_NOX
GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL
GasIndexAlgorithm_INITIAL_BLACKOUT = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INITIAL_BLACKOUT
GasIndexAlgorithm_INDEX_GAIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INDEX_GAIN
GasIndexAlgorithm_SRAW_STD_INITIAL = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SRAW_STD_INITIAL
GasIndexAlgorithm_SRAW_STD_BONUS_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SRAW_STD_BONUS_VOC
GasIndexAlgorithm_SRAW_STD_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SRAW_STD_NOX
GasIndexAlgorithm_TAU_MEAN_HOURS = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TAU_MEAN_HOURS
GasIndexAlgorithm_TAU_VARIANCE_HOURS = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TAU_VARIANCE_HOURS
GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC
GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX
GasIndexAlgorithm_INIT_DURATION_MEAN_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_DURATION_MEAN_VOC
GasIndexAlgorithm_INIT_DURATION_MEAN_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_DURATION_MEAN_NOX
GasIndexAlgorithm_INIT_TRANSITION_MEAN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_TRANSITION_MEAN
GasIndexAlgorithm_TAU_INITIAL_VARIANCE = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TAU_INITIAL_VARIANCE
GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC
GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX
GasIndexAlgorithm_INIT_TRANSITION_VARIANCE = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_INIT_TRANSITION_VARIANCE
GasIndexAlgorithm_GATING_THRESHOLD_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_THRESHOLD_VOC
GasIndexAlgorithm_GATING_THRESHOLD_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_THRESHOLD_NOX
GasIndexAlgorithm_GATING_THRESHOLD_INITIAL = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_THRESHOLD_INITIAL
GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION
GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES
GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES
GasIndexAlgorithm_GATING_MAX_RATIO = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_GATING_MAX_RATIO
GasIndexAlgorithm_SIGMOID_L = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SIGMOID_L
GasIndexAlgorithm_SIGMOID_K_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SIGMOID_K_VOC
GasIndexAlgorithm_SIGMOID_X0_VOC = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SIGMOID_X0_VOC
GasIndexAlgorithm_SIGMOID_K_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SIGMOID_K_NOX
GasIndexAlgorithm_SIGMOID_X0_NOX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_SIGMOID_X0_NOX
GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT
GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT
GasIndexAlgorithm_LP_TAU_FAST = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_LP_TAU_FAST
GasIndexAlgorithm_LP_TAU_SLOW = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_LP_TAU_SLOW
GasIndexAlgorithm_LP_ALPHA = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_LP_ALPHA
GasIndexAlgorithm_VOC_SRAW_MINIMUM = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_VOC_SRAW_MINIMUM
GasIndexAlgorithm_NOX_SRAW_MINIMUM = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_NOX_SRAW_MINIMUM
GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA
GasIndexAlgorithm_TUNING_INDEX_OFFSET_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_INDEX_OFFSET_MIN
GasIndexAlgorithm_TUNING_INDEX_OFFSET_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_INDEX_OFFSET_MAX
GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MIN
GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MAX
GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MIN
GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MAX
GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MIN
GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MAX
GasIndexAlgorithm_TUNING_STD_INITIAL_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_STD_INITIAL_MIN
GasIndexAlgorithm_TUNING_STD_INITIAL_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_STD_INITIAL_MAX
GasIndexAlgorithm_TUNING_GAIN_FACTOR_MIN = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_GAIN_FACTOR_MIN
GasIndexAlgorithm_TUNING_GAIN_FACTOR_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_TUNING_GAIN_FACTOR_MAX
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING
GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX = _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX
class GasIndexAlgorithmParams(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    mAlgorithm_Type = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mAlgorithm_Type_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mAlgorithm_Type_set)
    mSamplingInterval = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSamplingInterval_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSamplingInterval_set)
    mIndex_Offset = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mIndex_Offset_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mIndex_Offset_set)
    mSraw_Minimum = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_Minimum_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_Minimum_set)
    mGating_Max_Duration_Minutes = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGating_Max_Duration_Minutes_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGating_Max_Duration_Minutes_set)
    mInit_Duration_Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mInit_Duration_Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mInit_Duration_Mean_set)
    mInit_Duration_Variance = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mInit_Duration_Variance_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mInit_Duration_Variance_set)
    mGating_Threshold = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGating_Threshold_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGating_Threshold_set)
    mIndex_Gain = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mIndex_Gain_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mIndex_Gain_set)
    mTau_Mean_Hours = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mTau_Mean_Hours_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mTau_Mean_Hours_set)
    mTau_Variance_Hours = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mTau_Variance_Hours_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mTau_Variance_Hours_set)
    mSraw_Std_Initial = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_Std_Initial_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_Std_Initial_set)
    mUptime = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mUptime_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mUptime_set)
    mSraw = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mSraw_set)
    mGas_Index = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGas_Index_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_mGas_Index_set)
    m_Mean_Variance_Estimator___Initialized = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Initialized_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Initialized_set)
    m_Mean_Variance_Estimator___Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Mean_set)
    m_Mean_Variance_Estimator___Sraw_Offset = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sraw_Offset_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sraw_Offset_set)
    m_Mean_Variance_Estimator___Std = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Std_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Std_set)
    m_Mean_Variance_Estimator___Gamma_Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Mean_set)
    m_Mean_Variance_Estimator___Gamma_Variance = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Variance_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Variance_set)
    m_Mean_Variance_Estimator___Gamma_Initial_Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Initial_Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Initial_Mean_set)
    m_Mean_Variance_Estimator___Gamma_Initial_Variance = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Initial_Variance_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gamma_Initial_Variance_set)
    m_Mean_Variance_Estimator__Gamma_Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator__Gamma_Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator__Gamma_Mean_set)
    m_Mean_Variance_Estimator__Gamma_Variance = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator__Gamma_Variance_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator__Gamma_Variance_set)
    m_Mean_Variance_Estimator___Uptime_Gamma = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Uptime_Gamma_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Uptime_Gamma_set)
    m_Mean_Variance_Estimator___Uptime_Gating = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Uptime_Gating_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Uptime_Gating_set)
    m_Mean_Variance_Estimator___Gating_Duration_Minutes = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gating_Duration_Minutes_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Gating_Duration_Minutes_set)
    m_Mean_Variance_Estimator___Sigmoid__K = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sigmoid__K_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sigmoid__K_set)
    m_Mean_Variance_Estimator___Sigmoid__X0 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sigmoid__X0_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mean_Variance_Estimator___Sigmoid__X0_set)
    m_Mox_Model__Sraw_Std = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mox_Model__Sraw_Std_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mox_Model__Sraw_Std_set)
    m_Mox_Model__Sraw_Mean = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mox_Model__Sraw_Mean_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Mox_Model__Sraw_Mean_set)
    m_Sigmoid_Scaled__K = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__K_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__K_set)
    m_Sigmoid_Scaled__X0 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__X0_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__X0_set)
    m_Sigmoid_Scaled__Offset_Default = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__Offset_Default_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Sigmoid_Scaled__Offset_Default_set)
    m_Adaptive_Lowpass__A1 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass__A1_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass__A1_set)
    m_Adaptive_Lowpass__A2 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass__A2_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass__A2_set)
    m_Adaptive_Lowpass___Initialized = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___Initialized_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___Initialized_set)
    m_Adaptive_Lowpass___X1 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X1_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X1_set)
    m_Adaptive_Lowpass___X2 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X2_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X2_set)
    m_Adaptive_Lowpass___X3 = property(_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X3_get, _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_m_Adaptive_Lowpass___X3_set)

    def __init__(self, algorithm_type: "int32_t", sampling_interval: "float"):
        _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_swiginit(self, _sensirion_gas_index_algorithm_wrap.new_GasIndexAlgorithmParams(algorithm_type, sampling_interval))
    __swig_destroy__ = _sensirion_gas_index_algorithm_wrap.delete_GasIndexAlgorithmParams

    def init(self, algorithm_type: "int32_t", sampling_interval: "float") -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_init(self, algorithm_type, sampling_interval)

    def get_states(self) -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_get_states(self)

    def set_states(self, state0: "float", state1: "float") -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_set_states(self, state0, state1)

    def get_tuning_parameters(self) -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_get_tuning_parameters(self)

    def set_tuning_parameters(self, index_offset: "int32_t", learning_time_offset_hours: "int32_t", learning_time_gain_hours: "int32_t", gating_max_duration_minutes: "int32_t", std_initial: "int32_t", gain_factor: "int32_t") -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_set_tuning_parameters(self, index_offset, learning_time_offset_hours, learning_time_gain_hours, gating_max_duration_minutes, std_initial, gain_factor)

    def get_sampling_interval(self) -> "void":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_get_sampling_interval(self)

    def process(self, sraw: "int32_t") -> "int32_t":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_process(self, sraw)

    def get_version(self) -> "char const *":
        return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_get_version(self)

# Register GasIndexAlgorithmParams in _sensirion_gas_index_algorithm_wrap:
_sensirion_gas_index_algorithm_wrap.GasIndexAlgorithmParams_swigregister(GasIndexAlgorithmParams)


def GasIndexAlgorithm_init(params: "GasIndexAlgorithmParams", algorithm_type: "int32_t") -> "void":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_init(params, algorithm_type)

def GasIndexAlgorithm_init_with_sampling_interval(params: "GasIndexAlgorithmParams", algorithm_type: "int32_t", sampling_interval: "float") -> "void":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_init_with_sampling_interval(params, algorithm_type, sampling_interval)

def GasIndexAlgorithm_reset(params: "GasIndexAlgorithmParams") -> "void":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_reset(params)

def GasIndexAlgorithm_get_states(params: "GasIndexAlgorithmParams") -> "float *, float *":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_get_states(params)

def GasIndexAlgorithm_set_states(params: "GasIndexAlgorithmParams", state0: "float", state1: "float") -> "void":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_set_states(params, state0, state1)

def GasIndexAlgorithm_set_tuning_parameters(params: "GasIndexAlgorithmParams", index_offset: "int32_t", learning_time_offset_hours: "int32_t", learning_time_gain_hours: "int32_t", gating_max_duration_minutes: "int32_t", std_initial: "int32_t", gain_factor: "int32_t") -> "void":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_set_tuning_parameters(params, index_offset, learning_time_offset_hours, learning_time_gain_hours, gating_max_duration_minutes, std_initial, gain_factor)

def GasIndexAlgorithm_get_tuning_parameters(params: "GasIndexAlgorithmParams") -> "int32_t *, int32_t *, int32_t *, int32_t *, int32_t *, int32_t *":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_get_tuning_parameters(params)

def GasIndexAlgorithm_get_sampling_interval(params: "GasIndexAlgorithmParams") -> "float *":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_get_sampling_interval(params)

def GasIndexAlgorithm_process(params: "GasIndexAlgorithmParams", sraw: "int32_t") -> "int32_t *":
    return _sensirion_gas_index_algorithm_wrap.GasIndexAlgorithm_process(params, sraw)

