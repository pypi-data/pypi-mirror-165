import numpy
from scipy.optimize import curve_fit

# user-import
#import inOutTools

from modelTissueFlow.modules import inOutTools

def boundary_conditions(PARAMETERS,piv):
    boundary_conditions  = {'PERIODIC' : [],'LEFT_RIGHT_fixed' : [0.0,0.0],'LEFT_RIGHT_experimental_input' : [piv[0],piv[-1]]}
    return boundary_conditions

def ODE_solver_with_non_constant_coefficients(s,friction,viscosity,apical_mom_curvGrad,basal_mom_curvGrad,apical_myoGrad,basal_myoGrad,v_grad_correction,BOUNDARY_COND,PARAMETERS):
    ###################
    # equation-domain #
    ###################
    N = len(s)
    ds = numpy.average(s[1:] - s[:-1])
    s = numpy.insert(s,[0,len(s)],[s[0],s[-1]],axis=0)
    ##############
    # parameters #
    ##############
    gamma_Delta = PARAMETERS[0]
    eta_Delta = PARAMETERS[1]
    inv_sqr_L_H = PARAMETERS[2]
    r_a = PARAMETERS[3]
    r_b = PARAMETERS[4]
    a_gamma = PARAMETERS[5]
    a_eta = PARAMETERS[6]
    # rescaling-parameters
    inv_sqr_L_H = inv_sqr_L_H*(a_gamma/a_eta)
    r_a = r_a/a_eta
    r_b = r_b/a_eta
    #########################
    # equation-coefficients #
    #########################
    # viscosity
    A = 1.0 + viscosity*eta_Delta
    A = numpy.insert(A,[0,len(A)],[A[0],A[-1]],axis=0)
    # nothing
    B = numpy.ones_like(s)*0.0
    B = numpy.insert(B,[0,len(B)],[B[0],B[-1]],axis=0)
    # friction
    friction_0 = 1.0 + friction*gamma_Delta
    C = -1.0*friction_0*inv_sqr_L_H
    C = numpy.insert(C,[0,len(C)],[C[0],C[-1]],axis=0)
    # active-tension/curvature
    D = r_a*apical_mom_curvGrad + r_a*apical_myoGrad + r_b*basal_mom_curvGrad + r_b*basal_myoGrad + v_grad_correction  
    D = numpy.insert(D,[0,len(D)],[D[0],D[-1]],axis=0)
    ###################
    # equation-output #
    ###################
    y = None
    # coefficient-matrix 
    coeff_Mat = numpy.zeros((N + 2,N + 2))
    for indx in range(1,N + 1):
        coeff_Mat[indx][indx-1]  = A[indx]/(ds*ds) - B[indx]/(2.0*ds)
        coeff_Mat[indx][indx]  = C[indx] - 2.0*A[indx]/(ds*ds)
        coeff_Mat[indx][indx+1]  = A[indx]/(ds*ds) + B[indx]/(2.0*ds)
    inhomo_Vec = numpy.zeros(N + 2)
    for indx in range(1,N + 1):
        inhomo_Vec[indx] = D[indx]
    #########################
    # non-periodic-boundary #
    #########################
    if BOUNDARY_COND: 
        inhomo_Vec[2] = inhomo_Vec[2] - coeff_Mat[2][1]*BOUNDARY_COND[0]
        inhomo_Vec[N-1] = inhomo_Vec[N-1] - coeff_Mat[N-1][N]*BOUNDARY_COND[1]
        coeff_Mat = numpy.delete(coeff_Mat, [0,1,N,N+1], 0)
        coeff_Mat = numpy.delete(coeff_Mat, [0,1,N,N+1], 1)
        inhomo_Vec = numpy.delete(inhomo_Vec, [0,1,N,N+1], 0)
        # solve-equation
        y = numpy.linalg.solve(numpy.array(coeff_Mat),numpy.array(inhomo_Vec))
        inOutTools.error(not numpy.allclose(numpy.dot(coeff_Mat,y),inhomo_Vec),inOutTools.get_linenumber(),'equationsModule -> no solution of the equation !')
        y = numpy.insert(y,[0,len(y)],[BOUNDARY_COND[0],BOUNDARY_COND[1]],axis=0)# virtual-node-entry
    #####################
    # periodic-boundary #
    #####################
    else:
        coeff_Mat[2][N] = coeff_Mat[2][1]
        coeff_Mat[N][2] = coeff_Mat[N][N+1]*(1 + coeff_Mat[1][2]/coeff_Mat[1][0])
        coeff_Mat[N][N-1] = coeff_Mat[N][N-1] + coeff_Mat[N][N+1]
        coeff_Mat[N][N] = coeff_Mat[N][N] + (coeff_Mat[N][N+1]*coeff_Mat[1][1])/coeff_Mat[1][0]
        inhomo_Vec[N] = inhomo_Vec[N] + (coeff_Mat[N][N+1]*inhomo_Vec[1])/coeff_Mat[1][0]
        coeff_Mat = numpy.delete(coeff_Mat, [0,1,N+1], 0)
        coeff_Mat = numpy.delete(coeff_Mat, [0,1,N+1], 1)
        inhomo_Vec = numpy.delete(inhomo_Vec, [0,1,N+1], 0)
        # solve-equation
        y = numpy.linalg.solve(numpy.array(coeff_Mat),numpy.array(inhomo_Vec))
        inOutTools.error(not numpy.allclose(numpy.dot(coeff_Mat,y),inhomo_Vec),inOutTools.get_linenumber(),'equationsModule -> no solution of the equation !')
        y = numpy.insert(y,0,y[-1],axis=0)
    return y,friction_0    

def curve_fitting_and_prediction(INPUT,fittingDomain,BOUNDARY_COND_SWITCH,input_parameter,tension_flag,curvature_flag,v_grad_correction_flag,distinguish_myo_switch,fix_PARAMETERS,fit_piv_avg): 
    #################
    # specify-input #
    #################
    s_res,s,piv,total_myoGrad,apical_myoGrad,basal_myoGrad,total_mom_curvGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity = INPUT   
    myo_dependent_inputs = [tension_flag*apical_myoGrad,tension_flag*basal_myoGrad,curvature_flag*apical_mom_curvGrad,curvature_flag*basal_mom_curvGrad]     
    # distinguish-apical-basal_myo
    apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = distinguish_apical_basal_myo(distinguish_myo_switch,myo_dependent_inputs)
    # turn-on/off-v-grad-correction
    v_grad_correction = -1.0*v_grad_correction_flag*v_grad_correction # NOTE: flip-in-sign 
    ##################
    # all-parameters #
    ##################
    all_PARAMETER_indices = [item for item,_ in enumerate(input_parameter)]
    numAllParameters = len(all_PARAMETER_indices)
    ##################
    # fix-parameters #
    ##################
    fix_PARAMETER_indices = [key for key,_ in fix_PARAMETERS.items()]
    ###################
    # free-parameters #
    ###################
    free_PARAMETER_indices = numpy.sort(list(set(all_PARAMETER_indices) - set(fix_PARAMETER_indices)))
    if free_PARAMETER_indices.size == 0:
        free_PARAMETER_indices = fix_PARAMETER_indices
    free_input_parameter = [input_parameter[indx] for indx in free_PARAMETER_indices]
    free_PARAMETERS_len = [len(p) for p in free_input_parameter] 
    numFreeParameters =len(free_PARAMETERS_len)
    shift_free_PARAMETERS_len = numpy.cumsum(free_PARAMETERS_len)
    ###############
    # constraints #
    ###############
    const_HF = [numpy.PZERO,numpy.PINF]
    const_HV = [numpy.PZERO,numpy.PINF]
    const_l_H = [numpy.PZERO,numpy.PINF]
    const_r_a = [numpy.PZERO,numpy.PINF] 
    const_r_b = [numpy.PZERO,numpy.PINF]
    const_eta = [numpy.PZERO,numpy.PINF] 
    const_gamma = [numpy.PZERO,numpy.PINF] 
    const_param = [const_HF,const_HV,const_l_H,const_r_a,const_r_b,const_gamma,const_eta] 
    const_matrix = numpy.array([p for sub_parameter in [[const_param[indx]] if len(free_input_parameter[count]) == 1 else [const_param[indx] for _ in range(s.shape[0])] for count,indx in enumerate(free_PARAMETER_indices)] for p in sub_parameter]) 
    #################################
    # parameter-spilitting-function #
    #################################
    def split_PARAMETERS_ARRAY_to_PARAMETERS(time_indx,PARAMETERS_ARRAY):
        PARAMETERS = [0]*numAllParameters
        # construct-free-parameters
        free_PARAMETERS = [PARAMETERS_ARRAY[0] if free_PARAMETERS_len[0]==1 else PARAMETERS_ARRAY[0+time_indx]] 
        for shift_count,item in enumerate(shift_free_PARAMETERS_len[:-1]):
            free_PARAMETERS.append(PARAMETERS_ARRAY[item] if free_PARAMETERS_len[shift_count+1]==1 else PARAMETERS_ARRAY[item+time_indx])   
        # update-with-free-parameters
        for free_PARAMETER_counter,item in enumerate(free_PARAMETER_indices):
            PARAMETERS[item] = free_PARAMETERS[free_PARAMETER_counter] 
        # update-with-fix-parameters
        for fixed_key,item in fix_PARAMETERS.items():
            PARAMETERS[fixed_key] = item[time_indx] if isinstance(item,list) else item
        return PARAMETERS
    ##########################
    # curve-fitting-function #
    ##########################
    def curve_fitting_function(apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity,fit_piv_avg):
        def solve_model_equation(arc_len,*PARAMETERS_ARRAY):
            v_sol = []
            PARAMETERS_ARRAY = list(PARAMETERS_ARRAY)
            for time_indx,(v_exp,t_g_apical,t_g_basal,m_c_g_apical,m_c_g_basal,v_g,f,e) in enumerate(zip(piv,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity)):   
                PARAMETERS = split_PARAMETERS_ARRAY_to_PARAMETERS(time_indx,PARAMETERS_ARRAY)
                BOUNDARY_CONDITIONS = boundary_conditions(PARAMETERS,v_exp) 
                s = arc_len[time_indx]
                # solve-equation
                v,_ = ODE_solver_with_non_constant_coefficients(s,f,e,m_c_g_apical,m_c_g_basal,t_g_apical,t_g_basal,v_g,BOUNDARY_CONDITIONS[BOUNDARY_COND_SWITCH],PARAMETERS)
                # select-data-only-for-fitting-domain
                s_for_fitting = s[fittingDomain]
                v_for_fitting = v[fittingDomain]
                v_sol.append(inOutTools.area_under_curve(s_for_fitting,v_for_fitting,closed=False)/(s_for_fitting[-1]-s_for_fitting[0])) if fit_piv_avg == 'piv_avg' else v_sol.append(v_for_fitting)  
            return numpy.hstack(v_sol)
        return solve_model_equation 
    ###########################
    # individual/collective ? #
    ###########################
    if len(s.shape) == 1: 
        s_res,s,piv,total_myoGrad,apical_myoGrad,basal_myoGrad,total_mom_curvGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity = [numpy.array([item]) for item in [s_res,s,piv,total_myoGrad,apical_myoGrad,basal_myoGrad,total_mom_curvGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity]]
    ###########
    # fitting #
    ###########
    est_PARAMETERS = [p for sub_parameter in free_input_parameter for p in sub_parameter]
    piv_for_fitting = numpy.hstack([inOutTools.area_under_curve(a[fittingDomain],b[fittingDomain],closed=False)/(a[fittingDomain][-1]-a[fittingDomain][0]) for a,b in zip(s,piv)]) if fit_piv_avg == 'piv_avg' else numpy.hstack([p[fittingDomain] for p in piv])
    est_PARAMETERS,_ = curve_fit(curve_fitting_function(apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity,fit_piv_avg),s,piv_for_fitting,p0=est_PARAMETERS,bounds=(const_matrix[:,0],const_matrix[:,1])) 
    ##############
    # prediction #
    ##############
    v_fit = []
    chi_squr =[]
    PARAMETERS_ARRAY = list(est_PARAMETERS)  
    for time_indx,(v_exp,t_g_apical,t_g_basal,m_c_g_apical,m_c_g_basal,v_g,f,e) in enumerate(zip(piv,apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction,friction,viscosity)):   
        PARAMETERS = split_PARAMETERS_ARRAY_to_PARAMETERS(time_indx,PARAMETERS_ARRAY)
        BOUNDARY_CONDITIONS = boundary_conditions(PARAMETERS,v_exp)
        v_sol,_ = ODE_solver_with_non_constant_coefficients(s[time_indx],f,e,m_c_g_apical,m_c_g_basal,t_g_apical,t_g_basal,v_g,BOUNDARY_CONDITIONS[BOUNDARY_COND_SWITCH],PARAMETERS)
        v_fit.append(v_sol[fittingDomain]) 
        chi_squr.append(numpy.sum(numpy.square(numpy.array(v_sol[fittingDomain])-numpy.array(v_exp[fittingDomain]))))
    s_fit = [s[fittingDomain] for s in s_res]
    ##########################
    # restructure-parameters #
    ##########################
    print('updating fit-parameters')
    # free-parameters 
    free_input_parameter = [PARAMETERS_ARRAY[:shift_free_PARAMETERS_len[0]]]
    for free_PARAMETER_count in range(numFreeParameters-1):
        free_input_parameter.append(PARAMETERS_ARRAY[shift_free_PARAMETERS_len[free_PARAMETER_count]:shift_free_PARAMETERS_len[free_PARAMETER_count+1]]) 
    for free_PARAMETER_count,free_PARAMETER_indx in enumerate(free_PARAMETER_indices):
        input_parameter[free_PARAMETER_indx] = free_input_parameter[free_PARAMETER_count]  
    # fix-parameters 
    for fixed_key,item in fix_PARAMETERS.items():
        input_parameter[fixed_key] = item if isinstance(item,list) else [item]
    return input_parameter,v_fit if len(v_fit) > 1 else v_fit[0],chi_squr,s_fit if len(s_fit) > 1 else s_fit[0]

def distinguish_apical_basal_myo(distinguish_myo_switch,myo_dependent_inputs):
    apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = myo_dependent_inputs
    ############
    # ra != rb #
    ############
    if distinguish_myo_switch:
        # apical: myo/mom-curv-grad
        apical_myoGrad = -1.0*apical_myoGrad # NOTE: flip-in-sign
        apical_mom_curvGrad = 1.0*apical_mom_curvGrad
        # basal: myo/mom-curv-grad
        basal_myoGrad = -1.0*basal_myoGrad # NOTE: flip-in-sign
        basal_mom_curvGrad = -1.0*basal_mom_curvGrad # NOTE: flip-in-sign
    ######################
    # r_eff = ra, rb = 0 #
    ######################
    else:
        # apical: myo/mom-curv-grad
        apical_myoGrad = -1.0*apical_myoGrad -1.0*basal_myoGrad 
        apical_mom_curvGrad = 1.0*apical_mom_curvGrad -1.0*basal_mom_curvGrad
        # basal: myo/mom-curv-grad
        basal_myoGrad = numpy.zeros_like(basal_myoGrad) # NOTE: flip-in-sign
        basal_mom_curvGrad = numpy.zeros_like(apical_mom_curvGrad) # NOTE: flip-in-sign
    return apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad

def prediction_by_equation(s,INPUT,friction,viscosity,BOUNDARY_COND_SWITCH,PARAMETERS,tension_flag,curvature_flag,v_grad_correction_flag,distinguish_myo_switch): 
    # extract-input 
    apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad,v_grad_correction = INPUT
    myo_dependent_inputs = [tension_flag*apical_myoGrad,tension_flag*basal_myoGrad,curvature_flag*apical_mom_curvGrad,curvature_flag*basal_mom_curvGrad]     
    # distinguish-apical-basal_myo
    apical_myoGrad,basal_myoGrad,apical_mom_curvGrad,basal_mom_curvGrad = distinguish_apical_basal_myo(distinguish_myo_switch,myo_dependent_inputs)    
    # turn-on/off-v-grad-correction    
    v_grad_correction = -1.0*v_grad_correction_flag*v_grad_correction # NOTE: flip-in-sign   
    # boundary-condition
    PARAMETERS = list(PARAMETERS)
    BOUNDARY_CONDITIONS = boundary_conditions(PARAMETERS,[1e-6,1e-6])
    # solution
    v_sol,fric = ODE_solver_with_non_constant_coefficients(s,friction,viscosity,apical_mom_curvGrad,basal_mom_curvGrad,apical_myoGrad,basal_myoGrad,v_grad_correction,BOUNDARY_CONDITIONS[BOUNDARY_COND_SWITCH],PARAMETERS)
    return v_sol,fric 

def time_dynamics_of_markers(markers,ds,indx):
    s,s_max = inOutTools.arc_length_along_polygon(markers)
    # update-the-position-of-the-myo-centre
    s_next = s[indx]+ds*s_max
    # marker-at-the-updated-position-of-the-myo-centre
    markers_closed = inOutTools.numpy.insert(markers,len(markers),markers[0],axis=0)
    markers_interpolator,_,s_closed = inOutTools.interpolate_Points_and_Measurables_OnCurve(markers_closed,[],normalized=False)
    s_next = s_next - s_closed[-1] if s_next > s_closed[-1] else s_next
    markers_point_to_interpolate = markers_interpolator(s_next)
    # register-the-time-evolved-marker-as-new-entry: increases-total-number-of-marker-by-one
    markers = inOutTools.numpy.insert(markers,0,markers_point_to_interpolate,axis=0)
    markers = inOutTools.orient_polygon(markers,orientation_reference_indx=0,clockwise=True)   
    # uniformy-distribute-the-markers: reduce-total-number-of-makers-by-one (defaut -configuration)
    markers,_ = inOutTools.uniform_distribution_along_polygon(markers,len(markers),closed=True)
    return markers
   
def set_myo_curvature_off_set(mid_markers,initial_myo_to_curv_offSet,ellipse_axes_length):
    ellipse_semi_a,ellipse_semi_b = ellipse_axes_length
    intersection_scale_factor = ellipse_semi_a + ellipse_semi_b
    mid_markers_centre = inOutTools.numpy.array(inOutTools.Polygon(mid_markers).centroid.coords).flatten()
    mid_coordinate_orientation = inOutTools.normalize([-1.0*ellipse_semi_a,mid_markers_centre[0]]-mid_markers_centre)
    mid_origin_intersetion_axis = inOutTools.numpy.array([mid_markers_centre+2*(intersection_scale_factor)*mid_coordinate_orientation,mid_markers_centre])
    # reference-coordinate-origin 
    mid_markers,_ = inOutTools.uniform_distribution_along_polygon(mid_markers,len(mid_markers)+1,closed=True)
    mid_markers,mid_marker_parameters = inOutTools.reset_starting_point_of_polygon(mid_markers,mid_origin_intersetion_axis)
    mid_markers,_ = inOutTools.uniform_distribution_along_polygon(mid_markers,len(mid_markers),closed=True)
    # initial-myo-centre-to-curvature-peak-offSet 
    mid_markers_interpolator,_,_ = inOutTools.interpolate_Points_and_Measurables_OnCurve(mid_markers,[],normalized=True)
    initial_myo_position = mid_markers_interpolator(initial_myo_to_curv_offSet+1e-6) 
    initial_myo_orientation = inOutTools.normalize(initial_myo_position-mid_markers_centre)
    myo_centre_intersetion_axis = inOutTools.numpy.array([mid_markers_centre+2*(intersection_scale_factor)*initial_myo_orientation,mid_markers_centre])
    mid_markers,_ = inOutTools.reset_starting_point_of_polygon(mid_markers,myo_centre_intersetion_axis)  
    mid_markers,_ = inOutTools.uniform_distribution_along_polygon(mid_markers,len(mid_markers),closed=True)
    return [mid_markers,mid_coordinate_orientation,intersection_scale_factor]