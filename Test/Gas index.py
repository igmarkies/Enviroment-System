import math

class params:
    mAlgorithm_Type = 0
    mSamplingInterval = 0.0
    mIndex_Offset = 0.0
    mSraw_Minimum = 0
    mGating_Max_Duration_Minutes = 0.0
    mInit_Duration_Mean = 0.0
    mInit_Duration_Variance = 0.0
    mGating_Threshold = 0.0
    mIndex_Gain = 0.0
    mTau_Mean_Hours = 0.0
    mTau_Variance_Hours = 0.0
    mSraw_Std_Initial = 0.0
    mUptime = 0.0
    mSraw = 0.0
    mGas_Index = 0.0
    m_Mean_Variance_Estimator___Initialized = False
    m_Mean_Variance_Estimator___Mean = 0.0
    m_Mean_Variance_Estimator___Sraw_Offset = 0.0
    m_Mean_Variance_Estimator___Std = 0.0
    m_Mean_Variance_Estimator___Gamma_Mean = 0.0
    m_Mean_Variance_Estimator___Gamma_Variance = 0.0
    m_Mean_Variance_Estimator___Gamma_Initial_Mean = 0.0
    m_Mean_Variance_Estimator___Gamma_Initial_Variance = 0.0
    m_Mean_Variance_Estimator__Gamma_Mean = 0.0
    m_Mean_Variance_Estimator__Gamma_Variance = 0.0
    m_Mean_Variance_Estimator___Uptime_Gamma = 0.0
    m_Mean_Variance_Estimator___Uptime_Gating = 0.0
    m_Mean_Variance_Estimator___Gating_Duration_Minutes = 0.0
    m_Mean_Variance_Estimator___Sigmoid__K = 0.0
    m_Mean_Variance_Estimator___Sigmoid__X0 = 0.0
    m_Mox_Model__Sraw_Std = 0.0
    m_Mox_Model__Sraw_Mean = 0.0
    m_Sigmoid_Scaled__K = 0.0
    m_Sigmoid_Scaled__X0 = 0.0
    m_Sigmoid_Scaled__Offset_Default = 0.0
    m_Adaptive_Lowpass__A1 = 0.0
    m_Adaptive_Lowpass__A2 = 0.0
    m_Adaptive_Lowpass___Initialized = False
    m_Adaptive_Lowpass___X1 = 0.0
    m_Adaptive_Lowpass___X2 = 0.0
    m_Adaptive_Lowpass___X3 = 0.0
    
class GasIndexAlgorithme:
    
    def __init__(self):
        self.GasIndexAlgorithm_ALGORITHM_TYPE_VOC = 0
        self.GasIndexAlgorithm_ALGORITHM_TYPE_NOX = 1
        self.GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL = 1.0
        self.GasIndexAlgorithm_INITIAL_BLACKOUT = 45.0
        self.GasIndexAlgorithm_INDEX_GAIN = 230.0
        self.GasIndexAlgorithm_SRAW_STD_INITIAL = 50.0
        self.GasIndexAlgorithm_SRAW_STD_BONUS_VOC = 220.0
        self.GasIndexAlgorithm_SRAW_STD_NOX = 2000.0
        self.GasIndexAlgorithm_TAU_MEAN_HOURS = 12.0
        self.GasIndexAlgorithm_TAU_VARIANCE_HOURS = 12.0
        self.GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC = 20.0
        self.GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX = 1200.
        self.GasIndexAlgorithm_INIT_DURATION_MEAN_VOC = (3600.0 * 0.75)
        self.GasIndexAlgorithm_INIT_DURATION_MEAN_NOX = (3600.0 * 4.75)
        self.GasIndexAlgorithm_INIT_TRANSITION_MEAN = 0.01
        self.GasIndexAlgorithm_TAU_INITIAL_VARIANCE = 2500.0
        self.GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC = (3600.0 * 1.45)
        self.GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX = (3600.0 * 5.70)
        self.GasIndexAlgorithm_INIT_TRANSITION_VARIANCE = 0.01
        self.GasIndexAlgorithm_GATING_THRESHOLD_VOC = 340.0
        self.GasIndexAlgorithm_GATING_THRESHOLD_NOX = 30.0
        self.GasIndexAlgorithm_GATING_THRESHOLD_INITIAL = 510.0
        self.GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION = 0.09
        self.GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES = (60.0 * 3.0)
        self.GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES = (60.0 * 12.0)
        self.GasIndexAlgorithm_GATING_MAX_RATIO = 0.3
        self.GasIndexAlgorithm_SIGMOID_L = 500.0
        self.GasIndexAlgorithm_SIGMOID_K_VOC = -0.0065
        self.GasIndexAlgorithm_SIGMOID_X0_VOC = 213.0
        self.GasIndexAlgorithm_SIGMOID_K_NOX = -0.0101
        self.GasIndexAlgorithm_SIGMOID_X0_NOX = 614.0
        self.GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT = 100.0
        self.GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT = 1.0
        self.GasIndexAlgorithm_LP_TAU_FAST = 20.0
        self.GasIndexAlgorithm_LP_TAU_SLOW = 500.0
        self.GasIndexAlgorithm_LP_ALPHA = -0.2
        self.GasIndexAlgorithm_VOC_SRAW_MINIMUM = 20000
        self.GasIndexAlgorithm_NOX_SRAW_MINIMUM = 10000
        self.GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA = (3.0 * 3600.0)
        self.GasIndexAlgorithm_TUNING_INDEX_OFFSET_MIN = 1
        self.GasIndexAlgorithm_TUNING_INDEX_OFFSET_MAX = 250
        self.GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MIN = 1
        self.GasIndexAlgorithm_TUNING_LEARNING_TIME_OFFSET_HOURS_MAX = 1000
        self.GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MIN = 1
        self.GasIndexAlgorithm_TUNING_LEARNING_TIME_GAIN_HOURS_MAX = 1000
        self.GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MIN = 0
        self.GasIndexAlgorithm_TUNING_GATING_MAX_DURATION_MINUTES_MAX = 3000
        self.GasIndexAlgorithm_TUNING_STD_INITIAL_MIN = 10
        self.GasIndexAlgorithm_TUNING_STD_INITIAL_MAX = 5000
        self.GasIndexAlgorithm_TUNING_GAIN_FACTOR_MIN = 1
        self.GasIndexAlgorithm_TUNING_GAIN_FACTOR_MAX = 1000
        self.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING = 64.0
        self.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING = 8.0
        self.GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX = 32767.0
        
    def GasIndexAlgorithm_init_with_sampling_interval (self, params, algorithm_type, sampling_time):
        params.mAlgorithm_Type = algorithm_type
        params.mSamplingInterval = sampling_interval
        if (algorithm_type == GasIndexAlgorithm_ALGORITHM_TYPE_NOX):
            params.mIndex_Offset = GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT
            params.mSraw_Minimum = GasIndexAlgorithm_NOX_SRAW_MINIMUM
            params.mGating_Max_Duration_Minutes = GasIndexAlgorithm_GATING_NOX_MAX_DURATION_MINUTES
            params.mInit_Duration_Mean = GasIndexAlgorithm_INIT_DURATION_MEAN_NOX
            params.mInit_Duration_Variance = GasIndexAlgorithm_INIT_DURATION_VARIANCE_NOX
            params.mGating_Threshold = GasIndexAlgorithm_GATING_THRESHOLD_NOX
        else:
            params.mIndex_Offset = GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT
            params.mSraw_Minimum = GasIndexAlgorithm_VOC_SRAW_MINIMUM
            params.mGating_Max_Duration_Minutes = GasIndexAlgorithm_GATING_VOC_MAX_DURATION_MINUTES
            params.mInit_Duration_Mean = GasIndexAlgorithm_INIT_DURATION_MEAN_VOC
            params.mInit_Duration_Variance = GasIndexAlgorithm_INIT_DURATION_VARIANCE_VOC
            params.mGating_Threshold = GasIndexAlgorithm_GATING_THRESHOLD_VOC
        
        params.mIndex_Gain = GasIndexAlgorithm_INDEX_GAIN
        params.mTau_Mean_Hours = GasIndexAlgorithm_TAU_MEAN_HOURS
        params.mTau_Variance_Hours = GasIndexAlgorithm_TAU_VARIANCE_HOURS
        params.mSraw_Std_Initial = GasIndexAlgorithm_SRAW_STD_INITIAL
        GasIndexAlgorithm_reset(params)
        
    def GasIndexAlgorithm_init(self, params, algorithm_type):
        GasIndexAlgorithm_init_with_sampling_interval(params, algorithm_type, self.GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL)
        
    def GasIndexAlgorithm_reset(self, params):
        params.mUptime = 0.0
        params.mSraw = 0.0
        params.mGas_Index = 0
        GasIndexAlgorithm_init_instances(params)
        
    def GasIndexAlgorithm_init_instances(self.params):
        GasIndexAlgorithm_mean_variance_estimator_set_parameters(params)
        
    def process(self):
        if (params.mUptime <= self.gasIndexAlgorithm_INITIAL_BLACKOUT):
            params.mUptime = params.mUptime + params.mSamplingInterval
        else:
            if (((sraw > 0) and (sraw <65000))):
                if ((sraw < (params.mSraw_Minimum + 1))):
                    sraw = (params.mSraw_Minimum + 1)
                elif ((sraw > (params.mSraw_Minimum + 32767))):
                    sraw = (params.mSraw_Minimum + 32767)
                sraw = (float(sraw - params.mSraw_Minimum))
            
        if (params.mAlgorithme_Type == GasIndexAlgorithm_ALGORITHM_TYPE_VOC or GasIndexAlgorithm_mean_variance_estimator_is_initialized(params)):
            params.mGas_Index = GasIndexAlgorithm_mox_model_process(params, sraw)
            params.mGas_Index = GasIndexAlgorithm__sigmoid_scaled__process(params, params.mGas_Index)
        else:
            params.mGas_Index = params.mIndex_Offset

        params.mGas_Index = GasIndexAlgorithm_adaptive_lowpass_process(params, params.mGas_Index)

        if((params.mGas_Index < 0.5)):
            params.mGas_Index = 0.5
        if ((params.sraw > 0.0)):
            GasIndexAlgorithm__mean_variance_estimator__process(params, params.mSraw)
            GasIndexAlgorithm__mox_model__set_parameters(params, GasIndexAlgorithm__mean_variance_estimator__get_std(params), GasIndexAlgorithm__mean_variance_estimator__get_mean(params))
        gas_index = (((params.mGas_Index + 0.5)));
        #return

    
        
