def GasIndexAlgorithm_init_with_sampling_interval(params, algorithm_type, sampling_interval):
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
    
    def GasIndexAlgorithm_init(params, algorithm_type):
        GasIndexAlgorithm_init_with_sampling_interval(
        params, algorithm_type, GasIndexAlgorithm_DEFAULT_SAMPLING_INTERVAL)

    def GasIndexAlgorithm_reset(params):
        params.mUptime = 0.0
        params.mSraw = 0.0
        params.mGas_Index = 0
        GasIndexAlgorithm__init_instances(params)

def GasIndexAlgorithm__init_instances(params):
    GasIndexAlgorithm__mean_variance_estimator__set_parameters(params)
    GasIndexAlgorithm__mox_model__set_parameters(
    params, GasIndexAlgorithm__mean_variance_estimator__get_std(params),
    GasIndexAlgorithm__mean_variance_estimator__get_mean(params))
    if params.mAlgorithm_Type == GasIndexAlgorithm_ALGORITHM_TYPE_NOX:
        GasIndexAlgorithm__sigmoid_scaled__set_parameters(
        params, GasIndexAlgorithm_SIGMOID_X0_NOX,
        GasIndexAlgorithm_SIGMOID_K_NOX,
        GasIndexAlgorithm_NOX_INDEX_OFFSET_DEFAULT)
    else:
        GasIndexAlgorithm__sigmoid_scaled__set_parameters(
        params, GasIndexAlgorithm_SIGMOID_X0_VOC,
        GasIndexAlgorithm_SIGMOID_K_VOC,
        GasIndexAlgorithm_VOC_INDEX_OFFSET_DEFAULT)
    GasIndexAlgorithm__adaptive_lowpass__set_parameters(params)

    def GasIndexAlgorithm_get_sampling_interval(params, sampling_interval):
        sampling_interval[0] = params.mSamplingInterval

    def GasIndexAlgorithm_get_states(params, state0, state1):
        state0[0] = GasIndexAlgorithm__mean_variance_estimator__get_mean(params)
        state1[0] = GasIndexAlgorithm__mean_variance_estimator__get_std(params)

    def GasIndexAlgorithm_set_states(params, state0, state1):
        GasIndexAlgorithm__mean_variance_estimator__set_states(
        params, state0[0], state1[0], GasIndexAlgorithm_PERSISTENCE_UPTIME_GAMMA)
        GasIndexAlgorithm__mox_model__set_parameters(
        params, GasIndexAlgorithm__mean_variance_estimator__get_std(params),
        GasIndexAlgorithm__mean_variance_estimator__get_mean(params))
        params.mSraw = state0[0]

    def GasIndexAlgorithm_set_tuning_parameters(params, index_offset,
        learning_time_offset_hours,
        learning_time_gain_hours,
        gating_max_duration_minutes,
        std_initial, gain_factor):
        params.mIndex_Offset = float(index_offset)
        params.mTau_Mean_Hours = float(learning_time_offset_hours)
        params.mTau_Variance_Hours = float(learning_time_gain_hours)
        params.mGating_Max_Duration_Minutes = float(gating_max_duration_minutes)
        params.mSraw_Std_Initial = float(std_initial)
        params.mIndex_Gain = float(gain_factor)
        GasIndexAlgorithm__init_instances(params)

    def GasIndexAlgorithm_get_tuning_parameters(params, index_offset,
        learning_time_offset_hours,
        learning_time_gain_hours,
        gating_max_duration_minutes,
        std_initial,
        gain_factor):
        index_offset[0] = int(params.mIndex_Offset)
        learning_time_offset_hours[0] = int(params.mTau_Mean_Hours)
        learning_time_gain_hours[0] = int(params.mTau_Variance_Hours)
        gating_max_duration_minutes[0] = int(params.mGating_Max_Duration_Minutes)
        std_initial[0] = int(params.mSraw_Std_Initial)
        gain_factor[0] = int(params.mIndex_Gain)

    def GasIndexAlgorithm_process(params, sraw, gas_index):
        if params['mUptime'] <= GasIndexAlgorithm_INITIAL_BLACKOUT:
            params['mUptime'] += params['mSamplingInterval']
        else:
            if sraw > 0 and sraw < 65000:
                if sraw < params['mSraw_Minimum'] + 1:
                    sraw = params['mSraw_Minimum'] + 1
                elif sraw > params['mSraw_Minimum'] + 32767:
                    sraw = params['mSraw_Minimum'] + 32767
            params['mSraw'] = float(sraw - params['mSraw_Minimum'])

        if params['mAlgorithm_Type'] == GasIndexAlgorithm_ALGORITHM_TYPE_VOC or \
            GasIndexAlgorithm__mean_variance_estimator__is_initialized(params):
            params['mGas_Index'] = GasIndexAlgorithm__mox_model__process(params, params['mSraw'])
            params['mGas_Index'] = GasIndexAlgorithm__sigmoid_scaled__process(params, params['mGas_Index'])
        else:
            params['mGas_Index'] = params['mIndex_Offset']
        
        params['mGas_Index'] = GasIndexAlgorithm__adaptive_lowpass__process(params, params['mGas_Index'])
        if params['mGas_Index'] < 0.5:
            params['mGas_Index'] = 0.5
        if params['mSraw'] > 0:
            GasIndexAlgorithm__mean_variance_estimator__process(params, params['mSraw'])
            GasIndexAlgorithm__mox_model__set_parameters(params,
                GasIndexAlgorithm__mean_variance_estimator__get_std(params),
                GasIndexAlgorithm__mean_variance_estimator__get_mean(params))

        gas_index[0] = int(params['mGas_Index'] + 0.5)
        return
    
    def GasIndexAlgorithm__mean_variance_estimator__set_parameters(params):
        params['m_Mean_Variance_Estimator___Initialized'] = False
        params['m_Mean_Variance_Estimator___Mean'] = 0.0
        params['m_Mean_Variance_Estimator___Sraw_Offset'] = 0.0
        params['m_Mean_Variance_Estimator___Std'] = params['mSraw_Std_Initial']
        params['m_Mean_Variance_Estimator___Gamma_Mean'] = 
            (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
            GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
            (params['mSamplingInterval'] / 3600) /
            (params['mTau_Mean_Hours'] + (params['mSamplingInterval'] / 3600)))
        params['m_Mean_Variance_Estimator___Gamma_Variance'] = 
            (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
            (params['mSamplingInterval'] / 3600) /
            (params['mTau_Variance_Hours'] + (params['mSamplingInterval'] / 3600)))
        
        if params['mAlgorithm_Type'] == GasIndexAlgorithm_ALGORITHM_TYPE_NOX:
            params['m_Mean_Variance_Estimator___Gamma_Initial_Mean'] = 
                (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
                GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
                params['mSamplingInterval'] /
                (GasIndexAlgorithm_TAU_INITIAL_MEAN_NOX + params['mSamplingInterval']))
        else:
            params['m_Mean_Variance_Estimator___Gamma_Initial_Mean'] = 
                (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__ADDITIONAL_GAMMA_MEAN_SCALING *
                GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
                params['mSamplingInterval'] /
                (GasIndexAlgorithm_TAU_INITIAL_MEAN_VOC + params['mSamplingInterval']))
            
        params['m_Mean_Variance_Estimator___Gamma_Initial_Variance'] = 
            (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__GAMMA_SCALING *
            params['mSamplingInterval'] /
            (GasIndexAlgorithm_TAU_INITIAL_VARIANCE + params['mSamplingInterval']))
        params['m_Mean_Variance_Estimator__Gamma_Mean'] = 0.0
        params['m_Mean_Variance_Estimator__Gamma_Variance'] = 0.0
        params['m_Mean_Variance_Estimator___Uptime_Gamma'] = 0.0
        params['m_Mean_Variance_Estimator___Utime_Gating'] = 0.0
        params['m_Mean_Variance_Estimator___Gating_Duration_Minutes'] = 0.0
        
        def GasIndexAlgorithm__mean_variance_estimator__set_states(
params, mean, std, uptime_gamma):

csharp
Copy code
params.m_Mean_Variance_Estimator___Mean = mean
params.m_Mean_Variance_Estimator___Std = std
params.m_Mean_Variance_Estimator___Uptime_Gamma = uptime_gamma
params.m_Mean_Variance_Estimator___Initialized = True
def GasIndexAlgorithm__mean_variance_estimator__get_std(params):
return params.m_Mean_Variance_Estimator___Std

def GasIndexAlgorithm__mean_variance_estimator__get_mean(params):
return params.m_Mean_Variance_Estimator___Mean + 

params.m_Mean_Variance_Estimator___Sraw_Offset

def GasIndexAlgorithm__mean_variance_estimator__is_initialized(params):
return params.m_Mean_Variance_Estimator___Initialized

def GasIndexAlgorithm__mean_variance_estimator___calculate_gamma(params):
uptime_limit = (GasIndexAlgorithm_MEAN_VARIANCE_ESTIMATOR__FIX16_MAX -
params.mSamplingInterval)
if params.m_Mean_Variance_Estimator___Uptime_Gamma < uptime_limit:
params.m_Mean_Variance_Estimator___Uptime_Gamma += params.mSamplingInterval
if params.m_Mean_Variance_Estimator___Uptime_Gating < uptime_limit:
params.m_Mean_Variance_Estimator___Uptime_Gating += params.mSamplingInterval

scss
Copy code
GasIndexAlgorithm__mean_variance_estimator___sigmoid__set_parameters(
    params, params.mInit_Duration_Mean, GasIndexAlgorithm_INIT_TRANSITION_MEAN)
sigmoid_gamma_mean = \
    GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
        params, params.m_Mean_Variance_Estimator___Uptime_Gamma)
gamma_mean = (params.m_Mean_Variance_Estimator___Gamma_Mean +
              ((params.m_Mean_Variance_Estimator___Gamma_Initial_Mean - 
                params.m_Mean_Variance_Estimator___Gamma_Mean) *
               sigmoid_gamma_mean))
gating_threshold_mean = \
    (params.mGating_Threshold +
     ((GasIndexAlgorithm_GATING_THRESHOLD_INITIAL - 
       params.mGating_Threshold) *
      GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
          params, params.m_Mean_Variance_Estimator___Uptime_Gating)))
GasIndexAlgorithm__mean_variance_estimator___sigmoid__set_parameters(
    params, gating_threshold_mean, GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION)
sigmoid_gating_mean = \
    GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
        params, params.mGas_Index)
params.m_Mean_Variance_Estimator__Gamma_Mean = (sigmoid_gating_mean * gamma_mean)
GasIndexAlgorithm__mean_variance_estimator___sigmoid__set_parameters(
    params, params.mInit_Duration_Variance, GasIndexAlgorithm_INIT_TRANSITION_VARIANCE)
sigmoid_gamma_variance = \
    GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
        params, params.m_Mean_Variance_Estimator___Uptime_Gamma)
gamma_variance = \
    (params.m_Mean_Variance_Estimator___Gamma_Variance +
     ((params.m_Mean_Variance_Estimator___Gamma_Initial_Variance - 
       params.m_Mean_Variance_Estimator___Gamma_Variance) *
      (sigmoid_gamma_variance - sigmoid_gamma_mean)))
gating_threshold_variance = \
    (params.mGating_Threshold +
     ((GasIndexAlgorithm_GATING_THRESHOLD_INITIAL - 
       params.mGating_Threshold) *
      GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
          params, params.m_Mean_Variance_Estimator___Uptime_Gating)))
GasIndexAlgorithm__mean_variance_estimator___sigmoid__set_parameters(
    params, gating_threshold_variance, GasIndexAlgorithm_GATING_THRESHOLD_TRANSITION)
sigmoid_gating_variance = \
    GasIndexAlgorithm__mean_variance_estimator___sigmoid__process(
        params, params.mGas_Index)
params.m_Mean_Variance_Estimator__Gamma_Variance = (sigmoid_gating_variance * gamma_variance)

params.m_Mean_Variance_Estimator___Gating_Duration_Minutes = \
    (params.m_Mean_Variance_Estimator___Gating_Duration_Minutes +
     ((params.mSamplingInterval / 60.0) * 
      (((1.0 - sigmoid_gating_mean) * 
        (1.0 + GasIndexAlgorithm_GATING_MAX_RATIO)) - 
       GasIndexAlgorithm_GATING_MAX_RATIO)))
if params.m_Mean_Variance_Estimator___Gating_Duration_Minutes < 0.0:
    params.m_Mean_Variance_Estimator___Gating_Duration_Minutes = 0.0
if params.m_Mean_Variance_Estimator___Gating_D
