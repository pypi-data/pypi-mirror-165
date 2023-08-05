import numpy
from openpiv import scaling,process,filters,validation

# user-import
from modelTissueFlow.modules import inOutTools

def imageJ_frames_to_frame_pairs(dirPath,frame_Min_Max,numNode,apical_off_set,basal_off_set,posterior_pole_location,epithelium_orientation):  
    frameMin_ref,frameMax_ref = frame_Min_Max
    #######################################
    # consistency-check-for-MARKER-frames #
    #######################################
    marker_frame_indices = list(map(int,[file_header_comp.split('.')[0] for file_header_comp in [file_comp[-1] for file_comp in [each.split('_') for each in [file_comp[-1] for file_comp in [each.split('F_') for each in inOutTools.listdir_nohidden(dirPath + '/MARKERS')]]] if len(file_comp) == 1]]))
    marker_frame_indices.sort()
    if marker_frame_indices:
        mem_frame_indices = list(map(int,[file_header_comp.split('.')[0] for file_header_comp in [file_comp[-1] for file_comp in [each.split('_') for each in [file_comp[-1] for file_comp in [each.split('F_') for each in inOutTools.listdir_nohidden(dirPath + '/MEM')]]] if len(file_comp) == 1]]))
        mem_frame_indices.sort()
        myo_frame_indices = list(map(int,[file_header_comp.split('.')[0] for file_header_comp in [file_comp[-1] for file_comp in [each.split('_') for each in [file_comp[-1] for file_comp in [each.split('F_') for each in inOutTools.listdir_nohidden(dirPath + '/MYO')]]] if len(file_comp) == 1]]))
        myo_frame_indices.sort()
        if marker_frame_indices[-1] > mem_frame_indices[-1] or marker_frame_indices[0] < mem_frame_indices[0]:
            inOutTools.error(True,inOutTools.get_linenumber(),'readOutModule -> MARKER-frame-range exceeds MEM/MYO-frame-range !!!')
        else:
            ##############################################################################################
            # default-selection: only-those-MEM/MYO-frames-having-matching-index-with-the-MARKERS-frames #
            ##############################################################################################
            frameSequence_MEM = [[dirPath+'/MEM' + '/F_'+ '{:03d}'.format(index) + '.tif',dirPath+'/MEM' + '/F_'+ '{:03d}'.format(index+1) + '.tif'] for index in marker_frame_indices]    
            frameSequence_MYO = [[dirPath+'/MYO' + '/F_'+ '{:03d}'.format(index) + '.tif',dirPath+'/MYO' + '/F_'+ '{:03d}'.format(index+1) + '.tif'] for index in marker_frame_indices]  
            frameSequence_MARKERS = [dirPath+'/MARKERS' + '/F_'+ '{:03d}'.format(index) + '.tif' for index in marker_frame_indices] 
            #################################################
            # specific-selection: only-the-requested-frames #
            #################################################
            frameIndexDic = {}
            for indx,item in enumerate(marker_frame_indices):
                frameIndexDic[item] =  indx
            frameMin = frameIndexDic[frameMin_ref] if frameMin_ref in marker_frame_indices else print('frame range:',frameMin_ref,'-',marker_frame_indices[0]-1,' not segmented')
            frameMax = frameIndexDic[frameMax_ref]+1 if frameMax_ref in marker_frame_indices else print('frame range:',marker_frame_indices[-1]+1,'-',frameMax_ref,' not segmented')
            frameSequence_MEM = numpy.array(frameSequence_MEM[frameMin:frameMax]) 
            frameSequence_MYO = numpy.array(frameSequence_MYO[frameMin:frameMax])
            frameSequence_MARKERS = numpy.array(frameSequence_MARKERS[frameMin:frameMax])
            marker_frame_indices = numpy.array(marker_frame_indices[frameMin:frameMax])
            #########################################################################################
            # embryo-reference-frame: construct-via-ellipse-fitting-to-symmetric-phase(first-frame) #
            #########################################################################################
            ref_frame = dirPath+'/MARKERS' + '/F_'+ '{:03d}'.format(marker_frame_indices[0]) + '.tif'
            ref_frame_raw_markers,_,_,frameDimension = extract_different_markers(ref_frame,numNode,apical_off_set,basal_off_set,epithelium_orientation)   
            embryo_centre,embryo_principle_axes,ellipse_markers,_ = inOutTools.coordinate_frame_with_respect_to_polygon(ref_frame_raw_markers)
            frameDim_x,frameDim_y = frameDimension
            axis_scaleFactor = numpy.sum(frameDimension)
            embryo_principle_axes_major,embryo_principle_axes_minor = embryo_principle_axes
            image_frame_markers = numpy.array([[0,0],[frameDim_x,0],[frameDim_x,frameDim_y],[0,frameDim_y]])
            image_frame_line_segments = inOutTools.line_segments_along_polygon(image_frame_markers)
            x_ref_axis = None
            y_ref_axis = None
            embryo_reference_axis = None
            X_1,X_0 = embryo_principle_axes_major
            embryo_reference_axis_dir = inOutTools.normalize(X_1-X_0)
            for sign in [1,-1]:
                P0 = X_0 + sign*axis_scaleFactor*embryo_reference_axis_dir
                P = inOutTools.intersection_point_on_polygon_from_a_point(image_frame_line_segments,X_0,P0)
                X,Y = P-X_0
                embryo_orientation = inOutTools.point_at_which_quandrant(numpy.array([X,-Y])+1e-3)
                if embryo_orientation == posterior_pole_location:
                    embryo_reference_axis = [P,X_0]
                    c_x,c_y = X_0
                    x_ref_axis = numpy.array([[frameDim_x,c_y],[0,c_y]])
                    y_ref_axis = numpy.array([[c_x,frameDim_y],[c_x,0]])   
            if embryo_reference_axis is None: 
                inOutTools.error(True,inOutTools.get_linenumber(),'WARNING: readOutModule -> failed to detect the posterior pole !!!')
            ###########################################
            # embryo-pole-markers: anterior/posterior #
            ###########################################   
            ref_frame_raw_markers,_ = inOutTools.reset_starting_point_of_polygon(ref_frame_raw_markers,embryo_reference_axis)
            ref_frame_raw_markers = numpy.roll(ref_frame_raw_markers,25,axis=0)
            curv = inOutTools.curvature_along_polygon(ref_frame_raw_markers,closed=True)
            curv = -1.0*curv if not inOutTools.Polygon(ref_frame_raw_markers).exterior.is_ccw else curv
            s,s_max = inOutTools.arc_length_along_polygon(ref_frame_raw_markers)
            #curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region_adv(s/s_max,inOutTools.smooth_data(curv),[1.0,0.0],height = 0.0,sorted_peaks=True)
            anterior_ref_marker = ref_frame_raw_markers[0]#curv_peak_indx_second]
            posterior_ref_marker = ref_frame_raw_markers[-1]#curv_peak_indx_first]  
            return(marker_frame_indices,frameSequence_MEM,frameSequence_MYO,frameSequence_MARKERS,embryo_reference_axis,embryo_centre,x_ref_axis,y_ref_axis,anterior_ref_marker,posterior_ref_marker,ref_frame_raw_markers,ellipse_markers,frameDimension)
    else:
        inOutTools.error(True,inOutTools.get_linenumber(),'readOutModule -> no acceptable MARKER-frames (extension: m) exists !!!')
        
def extract_intensityColorMap(apical_intensity,basal_intensity,apical_polygon_Mask,basal_polygon_Mask,imageDimension):
    #######################
    # no-myosin-color-map #
    #######################
    intensity_colorMap_null = numpy.zeros(imageDimension[::-1])
    ########################################
    # construct-requested-myosin-color-map #
    ########################################
    intensity_colorMap_seperate_channel_List = [intensity_colorMap_null]
    intensity_colorMap_all_channel = inOutTools.copy_DATA(intensity_colorMap_null)
    for myoSelectFlag,(intensityType,polygonType) in enumerate(zip([apical_intensity,basal_intensity],[apical_polygon_Mask,basal_polygon_Mask])):
        intensity_colorMap_seperate_channel = inOutTools.copy_DATA(intensity_colorMap_null) # x-y-dimensions-are-inverted-for-image-representation
        # construct-the-color-map: fill-with-intensity
        for polygon_counter,(intensity,polygon) in enumerate(zip(intensityType,polygonType)):
            # create-empty(dummy)-colorMap
            empty_colorMap = numpy.zeros_like(intensity_colorMap_seperate_channel)
            # fill-the-dummy-colorMap
            inOutTools.cv2.fillPoly(empty_colorMap,[polygon],255) 
            # get-location-of-intensity-in-the-colorMap
            where_signal = numpy.where(empty_colorMap == 255)
            # fill-the-actual-colorMap
            intensity_colorMap_seperate_channel[where_signal] = intensity
            intensity_colorMap_all_channel[where_signal] = intensity
        intensity_colorMap_seperate_channel_List.append(intensity_colorMap_seperate_channel)
    no_intensity_colorMap_List,apical_intensity_colorMap_List,basal_intensity_colorMap_List = intensity_colorMap_seperate_channel_List
    return(apical_intensity_colorMap_List,basal_intensity_colorMap_List,intensity_colorMap_all_channel)

def extract_different_markers(marker_frame,reMarker_Number,apical_off_set,basal_off_set,epithelium_orientation):
    ####################
    # load-frame-image #
    ####################
    img = inOutTools.readImage(marker_frame,'color') # remove-transparency 
    ref_frame = inOutTools.cv2.cvtColor(img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale
    #############################
    # reference-image-dimension #
    #############################
    y_dim,x_dim = ref_frame.shape[:2]
    imageDimension = [x_dim,y_dim]
    #################################
    # detect-contours: apical/basal #
    #################################
    blured_Frame = inOutTools.cv2.GaussianBlur(ref_frame,(5,5),0.0)
    ret,thresh = inOutTools.cv2.threshold(blured_Frame.copy(),0,255,0)  # second-argument: free-threshold-value, third-argument: max-threshold-value
    contours, hierarchy = inOutTools.cv2.findContours(thresh, inOutTools.cv2.RETR_TREE, inOutTools.cv2.CHAIN_APPROX_SIMPLE)      
    ###############################################
    # conversion: contour-to-apical/basal-markers #
    ###############################################
    apical_markers = None
    basal_markers = None
    if(len(contours) > 0):
        # sort-contours-by-areas
        contourArea = [inOutTools.cv2.contourArea(c) for c in contours]
        contour_indicesr_by_large_area = numpy.argsort(contourArea)
        contour_indicesr_by_large_area = contour_indicesr_by_large_area[::-1]
        # first-two-large-contours-are-used-for-apical/basal-markers  
        apical_basal_contours = [contours[indx] for indx in contour_indicesr_by_large_area[:2]]
        apical_markers,basal_markers = [inOutTools.polygon_from_image_contour(apical_basal_contours[indx].T,reMarker_Number*(indx+1)) for indx in range(len(apical_basal_contours))]
    else:
        inOutTools.error(True,inOutTools.get_linenumber(),'No apical/basal contour detected !')
    #################################
    # ordered-markers: apical/basal #
    #################################   
    apical_markers = numpy.flip(apical_markers, axis = 0) if epithelium_orientation=='D-ccw' else apical_markers
    basal_markers  = numpy.flip(basal_markers, axis = 0) if epithelium_orientation=='D-ccw' else basal_markers
    ##################################################################
    # shifting-apical/basal-markers-from-edges-to-bulk-of-epithelium #
    ##################################################################
    _,normals = inOutTools.tangent_normals_along_polygon(apical_markers,closed=True)
    apical_markers = apical_markers - apical_off_set*normals # inward
    _,normals = inOutTools.tangent_normals_along_polygon(basal_markers,closed=True)
    basal_markers = basal_markers + basal_off_set*normals # outward
    ################################################
    # uniform-distribution-of-markers:apical/basal #
    ################################################
    apical_markers,_ = inOutTools.uniform_distribution_along_polygon(apical_markers,len(apical_markers),closed=True)
    basal_markers,_ = inOutTools.uniform_distribution_along_polygon(basal_markers,len(basal_markers),closed=True)
    #######################################################################
    # effective-embryo: yolk + epithelium (masks-for-removing-background) #
    #######################################################################
    img_masks = [None,None]
    for indx,markers in enumerate([apical_markers,basal_markers]):
        contours = numpy.array([markers],int) 
        img = inOutTools.readImage(marker_frame,'color') # remove-transparency
        ref_img = inOutTools.cv2.cvtColor(img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale 
        imageFieldBlacked = numpy.ones_like(ref_img.copy())*255
        img_masks[indx] = inOutTools.cv2.drawContours(imageFieldBlacked,contours,0,0,inOutTools.cv2.FILLED)
    return(apical_markers,basal_markers,img_masks,imageDimension)

def process_frames_and_markers(mem_frame_pair,myo_frame_pair,marker_frame,img_masks,apply_masks):
    #################################################
    # generate-piv-frame-pairs-from-membrane-frames #
    #################################################
    piv_frame_pair = []
    for mem_frame in mem_frame_pair:
        mem_img = inOutTools.readImage(mem_frame,'color') 
        GRAY_scale_mem = inOutTools.cv2.cvtColor(mem_img.copy(),inOutTools.cv2.COLOR_BGR2GRAY) # convert-to-gray-scale 
        piv_frame_pair.append(GRAY_scale_mem.copy())
    ##################
    # myo-RGB-values #
    ##################
    RGB_scale_myo_pair = []
    for myo_frame in myo_frame_pair:
        myo_img = inOutTools.readImage(myo_frame,'color')
        RGB_scale_myo = inOutTools.cv2.merge(inOutTools.cv2.split(myo_img)) 
        RGB_scale_myo_pair.append(RGB_scale_myo)
    #######################
    # membrane/myo-frames #
    #######################
    mem_img = inOutTools.readImage(mem_frame_pair[0],'color') 
    myo_img = inOutTools.readImage(myo_frame_pair[0],'color') 
    #################
    # masked-frames #
    #################
    mem_masked_img = mem_img.copy()
    myo_masked_img = myo_img.copy()
    if apply_masks:
        background_mask,yolk_mask = img_masks 
        yolk_mask = 255 - yolk_mask
        # mem-mask
        mem_masked_img[background_mask.astype(numpy.bool)] = 255 
        mem_masked_img[yolk_mask.astype(numpy.bool)] = 255
        # myo-mask
        myo_masked_img[background_mask.astype(numpy.bool)] = 255 
        myo_masked_img[yolk_mask.astype(numpy.bool)] = 255
    return(mem_img,myo_img,mem_masked_img,myo_masked_img,RGB_scale_myo_pair,piv_frame_pair)

def create_apical_basal_polygon_masks(mid_markers,apical_markers_raw,basal_markers_raw,layer_widths):
    layer_width_apical,layer_width_basal = layer_widths
    ####################################################
    # create-polygon-edges: determined-by-layer-widths #
    ####################################################
    basal_Mask_refEdge = []
    apical_Mask_refEdge = []
    semi_basal_Mask_refEdge = []
    semi_apical_Mask_refEdge = []
    normDist_outer,normal_dir_outer = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,apical_markers_raw,direction='outer')
    normDist_inner,normal_dir_inner = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,basal_markers_raw,direction='inner')
    for midPoint,norm_out,norm_in,normDist_out,normDist_in in zip(mid_markers,normal_dir_outer,normal_dir_inner,normDist_outer,normDist_inner): 
        norm_step_List_outer = [normDist_out,normDist_out + layer_width_apical[0],normDist_out + layer_width_apical[1]]  
        normalPoints = [midPoint - norm_step*norm_out for norm_step in norm_step_List_outer]   
        norm_step_List_inner = [normDist_in,normDist_in + layer_width_basal[0],normDist_in + layer_width_basal[1]] 
        normalPoints.extend([midPoint + norm_step*norm_in for norm_step in norm_step_List_inner[::-1]])
        # apical/semi-apical
        apical_Mask_refEdge.append(numpy.array([normalPoints[0],normalPoints[1]])) 
        semi_apical_Mask_refEdge.append(numpy.array([normalPoints[1],normalPoints[2]]))
        # basal/semi-basal
        basal_Mask_refEdge.append(numpy.array([normalPoints[-1],normalPoints[-2]])) 
        semi_basal_Mask_refEdge.append(numpy.array([normalPoints[-2],normalPoints[-3]])) 
    ##########################################################
    # construct-polygons: using-the-respective-polygon-edges #
    ##########################################################
    polygon_Mask_List = []
    for maskType in [apical_Mask_refEdge,basal_Mask_refEdge,semi_apical_Mask_refEdge,semi_basal_Mask_refEdge]:
        polygon_vertices = []
        numNode = len(maskType)
        for node_indx in range(numNode):
            e1 = maskType[(node_indx+1)%(numNode)]
            e2 = maskType[(node_indx)%(numNode)]
            polygon = numpy.array(numpy.concatenate((e1,e2[::-1])),numpy.int32)# ordered-polygon
            polygon_vertices.append(polygon)
        polygon_Mask_List.append(polygon_vertices) 
    apical_polygon_Mask,basal_polygon_Mask,_,_ = polygon_Mask_List
    apical_markers = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in apical_polygon_Mask])
    basal_markers = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in basal_polygon_Mask])
    return polygon_Mask_List,apical_markers,basal_markers

def extract_width_and_hegith_of_polygons(polygons):
    poly_edges_List = [[[poly[indx-1],poly[-(indx+2)]] for indx in range(len(poly)//2)] for poly in polygons] 
    poly_mid_markers_List = []
    poly_width_height_List = []
    for polygons in poly_edges_List:
        polygons_basal_edges = numpy.array([edges[0] for edges in polygons])
        polygons_apical_edges = numpy.array([edges[1] for edges in polygons])
        polygons_mid_edges = 0.5*(polygons_apical_edges+polygons_basal_edges)
        _,poly_width = inOutTools.arc_length_along_polygon(polygons_mid_edges)
        poly_height,_ = inOutTools.distance_between_pair_of_polygons(polygons_apical_edges,polygons_basal_edges)      
        poly_width_height_List.append([poly_width,poly_height])
        poly_mid_markers_List.append(polygons_mid_edges)
    poly_mid_markers_List = numpy.array(poly_mid_markers_List)
    poly_width_height_List = numpy.reshape(poly_width_height_List,(-1,2))
    return poly_width_height_List,poly_mid_markers_List

def refine_polygon_masks_at_target_posterior_region(mid_markers,polygon_Mask,apical_basal_markers_ref,layer_widths): 
    mask_refined_List = []
    polygon_centres_List = []
    semi_mask_refined_List = []
    layer_width_apical,layer_width_basal = layer_widths
    apical_Mask,basal_Mask,semi_apical_Mask,semi_basal_Mask = polygon_Mask
    for indx,(mask_semiMask_Type,ld) in enumerate(zip([[inOutTools.copy_DATA(apical_Mask),inOutTools.copy_DATA(semi_apical_Mask)],[inOutTools.copy_DATA(basal_Mask),inOutTools.copy_DATA(semi_basal_Mask)]],[layer_width_apical,layer_width_basal])):
        ##############################################################################
        # refine-polygon-masks-having-width > 10-times-the-width-of-smallest-polygon #
        ##############################################################################
        maskType,semi_maskType = mask_semiMask_Type
        mask_Width_Height,_ = extract_width_and_hegith_of_polygons(maskType)
        division_polygon_num = numpy.array(mask_Width_Height[:,0]/(10*min(mask_Width_Height[:,0])),int)
        polygon_centres = numpy.array([numpy.array(inOutTools.Polygon(polygon).centroid.coords).flatten() for polygon in maskType])
        for refine_indx,refine_polygon_iteration in enumerate(division_polygon_num):#range(len(maskType)):#polygon_Mask_refine_indices:
            ###############################################################
            # increase-polygon-node-number-by-inserting-an-edge: mid-edge #
            ###############################################################
            c1 = numpy.array(inOutTools.nearest_point_on_contour_from_external_point(apical_basal_markers_ref[indx],polygon_centres[refine_indx]))
            normal_dir = inOutTools.normalize(c1-mid_markers[refine_indx])
            c1 = numpy.array(c1)
            c2 = numpy.array(c1 + ld[0]*normal_dir,int)
            c3 = numpy.array(c1 + ld[1]*normal_dir,int)
            maskType[refine_indx] = numpy.insert(maskType[refine_indx],[0,2],[c1,c2],axis=0)
            semi_maskType[refine_indx] = numpy.insert(semi_maskType[refine_indx],[0,2],[c2,c3],axis=0)
            # refined-polygon-centre: mid-point-of-the-two-newly-inserted-markers-on-the-polygon-mask
            polygon_centres[refine_indx] = 0.5*(c1 + c2)   
            #########################################################################################
            # increase-polygon-node-number-by-inserting-a-pair-of-edges: left/rigth-to-the-mid-edge #
            #########################################################################################
            for N_max in range(refine_polygon_iteration):
                markers_Mask_add_List = []
                markers_semi_Mask_add_List = []
                for refine_indx_next in range(2**(N_max+1)):
                    # mid-point-of-outer-edge    
                    p1 = numpy.array(0.5*numpy.array(maskType[refine_indx][refine_indx_next-1]+maskType[refine_indx][refine_indx_next]),int) 
                    # mid-point-of-intermediate-edge
                    p2 = numpy.array(0.5*numpy.array(maskType[refine_indx][-(refine_indx_next+2)]+maskType[refine_indx][-(refine_indx_next+3)]),int) 
                    distance = numpy.linalg.norm(p2-p1)
                    # mid-point-of-inner-edge
                    p3 = numpy.array(0.5*numpy.array(semi_maskType[refine_indx][-(refine_indx_next+2)]+semi_maskType[refine_indx][-(refine_indx_next+3)]),int) 
                    semi_distance = numpy.linalg.norm(p3-p2)
                    # translate-mask/semi-mask-to-fit-with-the-raw-apical/basal-contour 
                    p1 = numpy.array(inOutTools.nearest_point_on_contour_from_external_point(apical_basal_markers_ref[indx],p1),int)
                    p2 = numpy.array(p1+distance*inOutTools.normalize(p2-p1),int)
                    p3 = numpy.array(p2+semi_distance*inOutTools.normalize(p3-p2),int)
                    # polygon-masks
                    markers_Mask_add_List.append(p1)
                    markers_Mask_add_List.append(p2)
                    # semi-polygon-masks
                    markers_semi_Mask_add_List.append(p2) 
                    markers_semi_Mask_add_List.append(p3)
                # insert-newly-created-markers-into-the-corresponding-polygon-masks/semi-polygon-masks
                insert_indx_list = []
                for insert_indx in range(2**(N_max+1)):
                    insert_indx_list.extend([insert_indx,2**(N_max+2)-insert_indx])
                maskType[refine_indx] = numpy.insert(maskType[refine_indx],insert_indx_list,markers_Mask_add_List,axis=0)
                semi_maskType[refine_indx] = numpy.insert(semi_maskType[refine_indx],insert_indx_list,markers_semi_Mask_add_List,axis=0)
        mask_refined_List.append(maskType)
        semi_mask_refined_List.append(semi_maskType)
        polygon_centres_List.append(polygon_centres) 
    ###############################################
    # extract-refines-polygon-masks: apical/basal #
    ###############################################
    apical_polygon_Mask,basal_polygon_Mask = mask_refined_List
    semi_apical_mask_List,semi_basal_mask_List = semi_mask_refined_List 
    apical_markers,basal_markers = polygon_centres_List
    return [apical_polygon_Mask,basal_polygon_Mask,semi_apical_mask_List,semi_basal_mask_List],apical_markers,basal_markers

def apical_basal_markers_and_masks_with_respect_to_midline(mid_markers,apical_markers_raw,basal_markers_raw,apical_markers,basal_markers,imageDimension,layer_widths):
    ############################################################################
    # transtale-markers-to-respective-raw-reference-marker-lines: apical/basal #
    ############################################################################
    apical_markers = [inOutTools.nearest_point_on_contour_from_external_point(apical_markers_raw,marker) for marker in apical_markers]
    basal_markers = [inOutTools.nearest_point_on_contour_from_external_point(basal_markers_raw,marker) for marker in basal_markers]
    layer_offSet_List = []
    for layer in [numpy.roll(mid_markers,1,axis=0),numpy.roll(apical_markers,1,axis=0),numpy.roll(basal_markers,1,axis=0)]:
        numNode = len(layer)
        layer_offSet = [0.5*(numpy.array(layer[(node_indx+1)%(numNode)]) + numpy.array(layer[(node_indx)%(numNode)])) for node_indx in range(numNode)]
        layer_offSet_List.append(numpy.array(layer_offSet))
    mid_markers_offSet,_,_ = layer_offSet_List
    ######################
    # set-myo-mask-width #
    ######################
    layer_width_apical,layer_width_basal = layer_widths
    sub_layer_width_apical,sub_layer_width_basal = [ele/2.0 for ele in layer_widths]
    layer_width_apical = [-layer_width_apical,-(layer_width_apical+sub_layer_width_apical)] # apical,semi-apical
    layer_width_basal = [-layer_width_basal,-(layer_width_basal+sub_layer_width_basal)] # basal-semi-basal
    layer_widths = [layer_width_apical,layer_width_basal]
    ##########################################
    # create-masks-and-markers: apical/basal #
    ##########################################
    polygon_Mask,apical_markers,basal_markers = create_apical_basal_polygon_masks(mid_markers_offSet,apical_markers_raw,basal_markers_raw,layer_widths)
    ##########################################
    # refine-masks-and-markers: apical/basal #
    ##########################################
    polygon_Mask,apical_markers,basal_markers = refine_polygon_masks_at_target_posterior_region(mid_markers,polygon_Mask,[apical_markers_raw,basal_markers_raw],layer_widths)
    ##################################
    # check-ordeing-of-polygon-masks #
    ##################################
    intersecting_edges = []
    for indx0,(a0,b0) in enumerate(zip(apical_markers,basal_markers)):
        for indx1,(a1,b1) in enumerate(zip(apical_markers[indx0+1:],basal_markers[indx0+1:])):
            flag,v,_ = inOutTools.intersection_of_two_LineSegments(a0,b0,a1,b1)
            if flag:
                intersecting_edges.append([indx0,indx1+indx0+1])
    inOutTools.error(intersecting_edges,inOutTools.get_linenumber(),'inOutTools -> masks are not sequentially orderd !!!')
    ##########################################
    # extract-masks-and-markers: apical/basal #
    ##########################################
    apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask = polygon_Mask
    apical_polygon_Mask = numpy.array(apical_polygon_Mask)
    basal_polygon_Mask = numpy.array(basal_polygon_Mask)
    semi_apical_polygon_Mask = numpy.array(semi_apical_polygon_Mask)
    semi_basal_polygon_Mask = numpy.array(semi_basal_polygon_Mask)
    return(apical_markers,basal_markers,apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask) 

def calculate_PIV(frame_0,frame_1,ws,ol,fr,area,sig_to_noise,piv_cutOff):
    ##############################################
    # extract-piv-accross-a-pair-of-movie-frames #
    ##############################################
    u, v, sig2noise = process.extended_search_area_piv(frame_0.astype(numpy.int32), 
                                                       frame_1.astype(numpy.int32), 
                                                       window_size = ws, 
                                                       overlap = ol, 
                                                       dt = fr, 
                                                       search_area_size = area, 
                                                       sig2noise_method = sig_to_noise
                                                       )
    x, y = process.get_coordinates(image_size = frame_0.shape, window_size = ws, overlap = ol)
    sig2noise[sig2noise == numpy.inf] = 1e6
    threshold_after_PIV = 1.0*numpy.min(sig2noise[numpy.nonzero(sig2noise)])
    piv_x_limit = (numpy.min(u),numpy.max(u))
    piv_y_limit = (numpy.min(v),numpy.max(v))
    u, v, piv_mask = validation.global_val(u, v, piv_x_limit, piv_y_limit)
    u, v, piv_mask = validation.sig2noise_val(u, v, sig2noise, threshold = threshold_after_PIV)
    u, v = filters.replace_outliers(u, v, method = 'localmean', max_iter = 10, kernel_size = 3)
    x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = 1.0)
    ################################
    # discard-piv-above-set-cutoff #
    ################################
    piv_mat_x,piv_mat_y = x.shape
    if piv_cutOff > 0.0: # remove-noisy-piv-cut-off-based
        uv_Dirs = [list(a) for a in zip(list(u.flatten()),list(v.flatten()))] 
        uv_norms = [numpy.linalg.norm(pvec) for pvec in uv_Dirs]
        uv_cutOff = numpy.mean(uv_norms) + piv_cutOff*numpy.std(uv_norms)
        for i in range(piv_mat_x):
            for j in range(piv_mat_y):
                if numpy.linalg.norm([u[i][j],v[i][j]]) > uv_cutOff: 
                    u[i][j] = 0.0
                    v[i][j] = 0.0 
    return(x,y,u,v,piv_mask)

def split_PIV_in_components(x,y,u,v,markers_set,window_size_interpol_piv): 
    #################################################
    # interpolate-piv-at-different-types-of-markers #
    #################################################
    piv_interpoleted_List,_ = interpolate_PIV_around_markers(markers_set,window_size_interpol_piv,x,y,u,v)
    ########################################################
    # extract-piv-components-at-different-types-of-markers #
    ########################################################
    piv_List = []
    piv_normal_mag_List = []
    piv_tangent_mag_List = []
    for markers,piv_interpoleted in zip(markers_set,piv_interpoleted_List):
        # tangent/normal-at-markers
        tangents,normals = inOutTools.tangent_normals_along_polygon(markers,closed=True)
        normals_outward = -1.0*normals # outward-normal
        # extract-tangent/normal-component-of-PIV 
        piv = []
        piv_normal_mag = []
        piv_tangent_mag = []
        for piv_interp,t_dir,n_dir in zip(piv_interpoleted,tangents,normals_outward): 
            piv_vector = numpy.array(piv_interp)
            # piv
            piv.append(piv_vector)
            # piv-tangent-component (NOTE:signed-magnitude)
            piv_tangent_mag.append(numpy.dot(t_dir,piv_vector))
            # piv-normal-component (NOTE:signed-magnitude)
            piv_normal_mag.append(numpy.dot(n_dir,piv_vector))
        piv_tangent_mag_List.append(piv_tangent_mag)
        piv_normal_mag_List.append(piv_normal_mag) 
        piv_List.append(piv)
    ######################################################
    # piv: averaged-over-over-different-types-of-markers #
    ######################################################
    piv_tangent_mag_avg = numpy.mean(numpy.array(piv_tangent_mag_List).T,axis=1)
    piv_normal_mag_avg = numpy.mean(numpy.array(piv_normal_mag_List).T,axis=1) 
    return(piv_tangent_mag_avg,piv_normal_mag_avg,piv_List)

def interpolate_PIV_around_markers(markers_set,window_size,piv_x_pos,piv_y_pos,piv_x_dir,piv_y_dir):
    #############################################################################
    # adjusting-piv-reference: flip-y-axis-to-comply-with-image-reference-frame #
    #############################################################################
    x = piv_x_pos
    u = piv_x_dir
    y = piv_y_pos[::-1]
    v = piv_y_dir*-1.0
    #####################################################################
    # count: types-of-markers/number-of-nodes-for-each-types-of-markers #
    #####################################################################
    markers_set = numpy.array(markers_set)
    num_marker_types,marker_length,_ =  markers_set.shape
    #################################################
    # search-piv-vetors-around-each-type-of-markers #
    #################################################
    xdim,ydim = x.shape
    indices_of_searched_vectors_set = [[[] for _ in range(marker_length)] for _ in range(num_marker_types)]
    for i in range(xdim):
        for j in range(ydim):
            # select-a-vector
            P = numpy.array([x[i][j],y[i][j]])
            # define-interpolation-window
            w_BL = P-window_size
            w_TR = P+window_size
            # loop-through-each-type-of-markers
            for m_type_indx in range(num_marker_types):
                for m_indx,m_type in enumerate(markers_set[m_type_indx]):  
                    # search-window: square
                    if ((m_type[0] > w_BL[0] and m_type[0] < w_TR[0]) and (m_type[1] > w_BL[1] and m_type[1] < w_TR[1])):
                        indices_of_searched_vectors_set[m_type_indx][m_indx].append([i,j])
    #####################################################################
    # interpolation-of-neighbouring-piv-vectors-on-each-type-of-markers #
    #####################################################################
    polygonCollections_List_all = []
    interpolated_uv_at_points_List_all = []
    # loop-through-each-type-of-markers
    for searched_vector_type,marker_type in zip(indices_of_searched_vectors_set,markers_set):
        polygonCollections_List = []
        interpolated_uv_at_points_List = []
        # loop-through-each-node-of-the-markers
        for sv_type,m_type in zip(searched_vector_type,marker_type):
            # interpolate-piv-vectors 
            vectors_dir = numpy.array([[u[i][j]for i,j in sv_type],[v[i][j]for i,j in sv_type]])
            vectors_pos = numpy.array(([x[i][j]for i,j in sv_type],[y[i][j]for i,j in sv_type])).T 
            interpolated_uv_at_points = inOutTools.interpolate_vectors_around_point(vectors_dir,vectors_pos,m_type)
            # orient-polygons-containing-neighbouring-piv-vectors
            polygonVertices = [[x[i][j],y[i][j]] for i,j in sv_type]
            polygonCollections = inOutTools.orient_polygon(polygonVertices,orientation_reference_indx=0,clockwise=True)                
            polygonCollections_List.append(polygonCollections)    
            interpolated_uv_at_points_List.append(interpolated_uv_at_points)
        # store-piv-vectors-and-polygons-for-each-type-of-markers
        polygonCollections_List_all.append(polygonCollections_List)
        interpolated_uv_at_points_List_all.append(interpolated_uv_at_points_List)
    return(interpolated_uv_at_points_List_all,polygonCollections_List_all)

def extract_MYOSIN_intensity(intensity_set,apply_MyoMask,apical_polygon_Mask,basal_polygon_Mask):     
    ###############
    # function: 1 #
    ###############
    def average_MYOSIN_intensity_per_pixel_within_polygon_mask(true,mask):
        # average-of-true-intensity 
        true_avg_apical = sum(true[0])/len(true[0])
        true_avg_basal = sum(true[1])/len(true[1])
        # average-of-mask-intensity 
        mask_avg_apical = sum(mask[0])/len(mask[0])
        mask_avg_basal = sum(mask[1])/len(mask[1])
        return([true_avg_apical,true_avg_basal],[mask_avg_apical,mask_avg_basal])
    ###########################
    # apical/basal-mask-width #
    ###########################
    apical_polygon_Mask_width_height,apical_poly_mid_markers_List = extract_width_and_hegith_of_polygons(apical_polygon_Mask)
    basal_polygon_Mask_width_height,basal_poly_mid_markers_List = extract_width_and_hegith_of_polygons(basal_polygon_Mask)
    apical_layer_width = apical_polygon_Mask_width_height[:,0]
    basal_layer_width = basal_polygon_Mask_width_height[:,0]
    #############################################################################################
    # integrated-intensity-at-different-types-masks/sub-mask: apical/sub-apical,basal/sub-basal #
    #############################################################################################
    apical_basal_integrated_intensity_raw = numpy.array(intensity_set[0]).T
    apical_basal_mask_integrated_intensity_raw = numpy.array(intensity_set[1]).T
    ###################################
    # seperate-apical/basal-intensity #
    ###################################
    apical_basal_intensity_per_length = []
    for indx,(true,mask) in enumerate(zip(apical_basal_integrated_intensity_raw,apical_basal_mask_integrated_intensity_raw)):
        true_avg,mask_avg = average_MYOSIN_intensity_per_pixel_within_polygon_mask(true,mask)
        ######################################################
        # masked-intensity: actual-intensity - sub-intensity #
        ######################################################
        true_apical = numpy.array(true[0])
        true_basal = numpy.array(true[1])
        if apply_MyoMask: 
            true_apical = numpy.array(true_apical - mask_avg[0])
            true_basal = numpy.array(true_basal - mask_avg[1])
            true_apical[true_apical < 0] = 0 # replace-negative-apical-intensity-by-zero 
            true_basal[true_basal < 0] = 0 # replace-negative-basal-intensity-by-zero
        ######################
        # per-length-average #
        ######################
        apical_basal_intensity_per_length.append([sum(true_apical)/apical_layer_width[indx],sum(true_basal)/basal_layer_width[indx]]) 
    ############################
    # list-to-array-conversion #
    ############################
    apical_basal_intensity_per_length = numpy.array(apical_basal_intensity_per_length) 
    apical_intensity_per_length,basal_intensity_per_length = [apical_basal_intensity_per_length[:,0],apical_basal_intensity_per_length[:,1]]
    return(apical_intensity_per_length,basal_intensity_per_length)

def extract_MYOSIN_intensity_and_colorMap(apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask,frameDimension,RGB_scale_myo_pair,myoMask,apical_polygon_Mask_width_height,basal_polygon_Mask_width_height):
    frameDimension = frameDimension[::-1] # NOTE: x-y-dimensions-are-inverted
    ######################################################
    # raw-myosin-intensity: averaged-over-pair-of-frames #
    ######################################################
    RGB_scale_myo,RGB_scale_myo_next = RGB_scale_myo_pair
    raw_myo_intensity = 0.5*(RGB_scale_myo+RGB_scale_myo_next)
    #########################################
    # compute-myosin-intensity-and-colorMap #
    #########################################
    intensity_values_List = []
    for indx,PolygonLayer in enumerate([[apical_polygon_Mask,basal_polygon_Mask],[semi_apical_polygon_Mask,semi_basal_polygon_Mask]]):
        ##################################################################
        # take-a-pair-of-polygon-mask-or-semi-polygon-mask: apical,basal #
        ##################################################################
        intensity_values_per_layer = []
        intensity_colorMap = numpy.zeros(frameDimension)
        for PolygonType in PolygonLayer:
            #######################################################
            # extract-intensity(primarily)-also-fill-for-colorMap #
            #######################################################
            intensity_values = []
            for polygon in PolygonType:
                # create-empty(dummy)-colorMap
                mask = numpy.zeros(frameDimension)
                # fill-the-dummy-colorMap
                inOutTools.cv2.fillPoly(mask,[polygon],255) 
                # get-location-of-intensity-in-the-colorMap
                where = numpy.where(mask == 255)
                R_G_B_indv_pixels = raw_myo_intensity[where[0], where[1]]
                RGB_indv_pixels = [sum(myo) for myo in R_G_B_indv_pixels]   
                # fill-the-actual-intensity-colorMap
                intensity_colorMap[where] = RGB_indv_pixels
                ###################################
                # store-the-intensity-per-polygon #
                ###################################
                intensity_values.append(RGB_indv_pixels)
            ###########################################
            # store-the-intensity-per-individual-layer #
            ############################################
            intensity_values_per_layer.append(intensity_values)
        ######################################
        # store-the-intensity-per-layer-type #
        ######################################
        intensity_values_List.append(intensity_values_per_layer)
    ##############################################
    # myosin-intensity: per-length-and-per-pixel #
    ##############################################
    apical_intensity_per_length,basal_intensity_per_length = extract_MYOSIN_intensity(intensity_values_List,myoMask,apical_polygon_Mask_width_height,basal_polygon_Mask_width_height)      
    ################################
    # true/mask-intensity-colorMap #
    ################################
    return(apical_intensity_per_length,basal_intensity_per_length)

def extract_activeMoment_ingredients(apical_intensity,basal_intensity,mid_markers,apical_markers,basal_markers):
    ######################################################################
    # active-moment-ingredients: apical-myosion,basal-myosin,cell-height #
    ######################################################################
    e_h_List = []
    basal_myo_List = []
    apical_myo_List = []
    apical_basal_point_pairs = numpy.array([[a,b] for a,b in zip(apical_markers,basal_markers)])
    for marker_pair,mid_mark,apical_myo,basla_myo in zip(apical_basal_point_pairs,mid_markers,apical_intensity,basal_intensity):
        ########################
        # myosin: apical/basal #
        ########################
        apical_myo_List.append(apical_myo)
        basal_myo_List.append(basla_myo)
        ###############
        # cell-height #
        ###############
        e_h_List.append(2.0*numpy.average([numpy.linalg.norm(marks-mid_mark) for marks in marker_pair]))
    return(numpy.array(e_h_List),numpy.array(apical_myo_List),numpy.array(basal_myo_List))

def time_allignmnet(EMBRYO,piv_transition_cutOff_val,window_SIZE):
    ####################################################################################
    # window-averaging: piv/apical-myo (over-arc-length,at-each-individual-time-point) #
    ####################################################################################
    piv_tan_List,apical_myo_List = numpy.array([inOutTools.sliding_window_average_data(item,window_SIZE) for item in [EMBRYO.piv_tan_sign_mag_List,EMBRYO.apical_myo_List]]) 
    #####################################
    # spatial-averaging: piv/apical-myo #
    #####################################
    vitelline_space_List = []
    pos_piv_tan_sp_avg_List = []
    full_piv_tan_sp_avg_List = []
    pos_apical_myo_sp_avg_List = []
    full_apical_myo_sp_avg_List = []  
    for time_indx,(mid_markers,apical_markers,piv_tan,apical_myo,pos_mid_markers,pos_piv_tan,pos_apical_myo) in enumerate(zip(EMBRYO.mid_markers_List,EMBRYO.apical_markers_List,piv_tan_List,apical_myo_List,inOutTools.truncate_Data_Range(EMBRYO.mid_markers_List,EMBRYO.posterior_domain),inOutTools.truncate_Data_Range(EMBRYO.piv_tan_sign_mag_List,EMBRYO.posterior_domain),inOutTools.truncate_Data_Range(EMBRYO.apical_myo_List,EMBRYO.posterior_domain))):
        ###################
        # full-epithelium #
        ###################
        s,s_max = inOutTools.arc_length_along_polygon(mid_markers)
        # spatially-averaged-piv 
        area_under_piv_tan = inOutTools.area_under_curve(s/s_max,numpy.array(inOutTools.sliding_window_average_data(piv_tan,window_SIZE)),closed=False)
        full_piv_tan_sp_avg_List.append(area_under_piv_tan) 
        # total-apical-myo
        area_under_apical_myo = sum(apical_myo)
        full_apical_myo_sp_avg_List.append(area_under_apical_myo)
        ########################
        # posterior-epithelium #
        ########################
        pos_s,pos_s_max = inOutTools.arc_length_along_polygon(pos_mid_markers)
        # spatially-averaged-piv
        area_under_piv_tan = inOutTools.area_under_curve(pos_s/pos_s_max,numpy.array(inOutTools.sliding_window_average_data(pos_piv_tan,window_SIZE)),closed=False)
        pos_piv_tan_sp_avg_List.append(area_under_piv_tan) 
        # total-apical-myo
        area_under_apical_myo = sum(pos_apical_myo)
        pos_apical_myo_sp_avg_List.append(area_under_apical_myo)
        ###################
        # vitelline-space #
        ###################
        vitelline_space_List.append(1.0-inOutTools.Polygon(apical_markers).area/inOutTools.Polygon(EMBRYO.animal_markers_ref).area)
    ##############################################################
    # window-averaging: piv-avg/apical-myo (over-all-time-point) #
    ##############################################################
    vitelline_space_List = numpy.array(inOutTools.sliding_window_average_data(vitelline_space_List,window_SIZE))
    # posterior-epithelium: piv-avg/apical-myo 
    pos_piv_tan_sp_avg_List = numpy.array(inOutTools.sliding_window_average_data(pos_piv_tan_sp_avg_List,window_SIZE))
    pos_apical_myo_sp_avg_List = numpy.array(inOutTools.sliding_window_average_data(pos_apical_myo_sp_avg_List,window_SIZE))
    # full-epithelium: piv-avg/apical-myo
    full_piv_tan_sp_avg_List = numpy.array(inOutTools.sliding_window_average_data(full_piv_tan_sp_avg_List,window_SIZE))
    full_apical_myo_sp_avg_List = numpy.array(inOutTools.sliding_window_average_data(full_apical_myo_sp_avg_List,window_SIZE))
    #################################
    # apply-cut-off-to-piv-avg-data #
    #################################
    coeff = None
    piv_fitting_range = None
    sym_asym_transition_frame = None
    if piv_transition_cutOff_val > 0.0:
        cutOff_indices, = numpy.where(full_piv_tan_sp_avg_List > piv_transition_cutOff_val)
        piv_cutOff_index = 0
        if cutOff_indices.size > 0:
            piv_cutOff_index = cutOff_indices[0] 
        # piv-avg-above-cut-off
        piv_valid_for_fitting_range = len(EMBRYO.frameIndex_List)-piv_cutOff_index 
        ###########################
        # sym-to-asym-frame-index #
        ###########################
        if piv_valid_for_fitting_range > 5:
            piv_fitting_range = piv_cutOff_index + 5
            # line-fitting
            frame_indx_patch = EMBRYO.frameIndex_List[piv_cutOff_index:piv_fitting_range]
            piv_tan_sp_avg_patch = full_piv_tan_sp_avg_List[piv_cutOff_index:piv_fitting_range]
            coeff = numpy.polyfit(frame_indx_patch,piv_tan_sp_avg_patch,1) 
            # sym-to-asym-transition-frame-indx
            sym_asym_transition_frame = int(round(-1.0*coeff[1]/coeff[0]))
            frameIndexDic = {item:indx for indx,item in enumerate(EMBRYO.frameIndex_List)}
            sym_asym_transition_frame_reverseMap = frameIndexDic[sym_asym_transition_frame]
            if full_piv_tan_sp_avg_List[sym_asym_transition_frame_reverseMap] < 0:
                full_piv_tan_sp_avg_List_negative_indices, = numpy.where(full_piv_tan_sp_avg_List[sym_asym_transition_frame_reverseMap:]< 0)
                sym_asym_transition_frame = EMBRYO.frameIndex_List[sym_asym_transition_frame_reverseMap+max(full_piv_tan_sp_avg_List_negative_indices)+1]  
            sym_asym_transition_frame = int(sym_asym_transition_frame)
        else:
            print('Allignmnet failed !!!, number of frames after transition is <', 5)
            inOutTools.terminate()
    else:
        print('no allignmnet requested !!!')
        sym_asym_transition_frame = EMBRYO.frameIndex_List[0]
    return [[piv_transition_cutOff_val,piv_fitting_range,coeff],sym_asym_transition_frame,full_piv_tan_sp_avg_List,full_apical_myo_sp_avg_List,pos_piv_tan_sp_avg_List,pos_apical_myo_sp_avg_List,vitelline_space_List]

def orient_animal(animal,crop_margin): 
    ellipse_markers,apical_myo_Mask_List,basal_myo_Mask_List,mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,myo_frame_List  = [animal.ellipse_markers,animal.apical_myo_Mask_List,animal.basal_myo_Mask_List,animal.mid_markers_List,animal.bulk_markers_List,animal.bulk_piv_List,animal.apical_markers_List,animal.apical_markers_raw_List,animal.basal_markers_List,animal.basal_markers_raw_List,animal.myo_frame_List]
    # split-piv-to-end-points
    bulk_piv_dir_List  = [numpy.reshape(bulk_piv,(-1,2)) for bulk_piv in bulk_piv_List]
    bulk_markers_List = [numpy.reshape(bulk_markers,(-1,2)) for bulk_markers in bulk_markers_List]
    bulk_piv_List  = [numpy.add(bulk_piv_dir,bulk_markers) for bulk_piv_dir,bulk_markers in zip(bulk_piv_dir_List,bulk_markers_List)]
    # ref-image/rotation-angle
    img_ref = inOutTools.copy_DATA(myo_frame_List[0])
    rotation_angle_List = [inOutTools.angle_between(numpy.array(mid_markers[0]-numpy.mean(ellipse_markers,axis=0)),numpy.array([-1,0])) for mid_markers in  mid_markers_List]
    # rotate-image
    ellipse_markers = numpy.array(inOutTools.rotatePointsOnImage(myo_frame_List[0],ellipse_markers,rotation_angle=rotation_angle_List[0]))
    #apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List = [numpy.array([inOutTools.rotateImage(myoColorMap,rotation_angle=rotation_angle) for myoColorMap,rotation_angle in zip(myoColorMaps,rotation_angle_List)]) for myoColorMaps in [apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List]]  
    apical_myo_Mask_List,basal_myo_Mask_List = [[numpy.array([numpy.array(inOutTools.rotatePointsOnImage(myo_frame,mask,rotation_angle=rotation_angle),int) for mask in myo_Mask]) for myo_Mask,myo_frame,rotation_angle in zip(myo_maskType_List,myo_frame_List,rotation_angle_List)] for myo_maskType_List in [apical_myo_Mask_List,basal_myo_Mask_List]]
    mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List = [numpy.array([inOutTools.rotatePointsOnImage(myo_frame,markers,rotation_angle=rotation_angle) for myo_frame,markers,rotation_angle in zip(myo_frame_List,markers_List,rotation_angle_List)]) for markers_List in [mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List]]
    myo_frame_List = numpy.array([inOutTools.rotateImage(myo_frame,rotation_angle=rotation_angle) for myo_frame,rotation_angle in zip(myo_frame_List,rotation_angle_List)])
    # flip-image
    img_ref = inOutTools.copy_DATA(myo_frame_List[0])
    mid_markers_ref = inOutTools.copy_DATA(mid_markers_List[0])
    flipMode = 'H' if not inOutTools.Polygon(mid_markers_ref).exterior.is_ccw else None
    ellipse_markers = numpy.array(inOutTools.flipPointsOnImage(img_ref,ellipse_markers,flipMode=flipMode))
    #apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List = [numpy.array([inOutTools.flipImage(myoColorMap,flipMode=flipMode) for myoColorMap in myoColorMaps]) for myoColorMaps in [apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List]]  
    apical_myo_Mask_List,basal_myo_Mask_List = [[numpy.array([numpy.array(inOutTools.flipPointsOnImage(img_ref,mask,flipMode=flipMode),int) for mask in myo_Mask]) for myo_Mask,myo_frame in zip(myo_maskType_List,myo_frame_List)] for myo_maskType_List in [apical_myo_Mask_List,basal_myo_Mask_List]]
    mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List = [numpy.array([inOutTools.flipPointsOnImage(img_ref,markers,flipMode=flipMode) for myo_frame,markers in zip(myo_frame_List,markers_List)]) for markers_List in [mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List]]
    myo_frame_List = numpy.array([inOutTools.flipImage(myo_frame,flipMode=flipMode) for myo_frame in myo_frame_List])
    # crop-image
    img_ref = inOutTools.copy_DATA(myo_frame_List[0])
    height,width,_ = img_ref.shape
    mid_markers_ref = inOutTools.copy_DATA(mid_markers_List[0])
    P_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[0]),int)
    D_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[25]),int)
    A_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[50]),int)
    V_markers_ref = numpy.array(inOutTools.copy_DATA(mid_markers_ref[75]),int)
    crop_xL,crop_xR = [P_markers_ref[0]-crop_margin,-(width-A_markers_ref[0]-crop_margin)]
    crop_yT,crop_yB = [D_markers_ref[1]-crop_margin,-(height-V_markers_ref[1]-crop_margin)]
    ellipse_markers = numpy.array(ellipse_markers) - numpy.array([crop_xL,crop_yT])
    #apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List = [numpy.array([myoColorMap[crop_yT:crop_yB,crop_xL:crop_xR] for myoColorMap in myoColorMaps]) for myoColorMaps in [apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List]] 
    apical_myo_Mask_List,basal_myo_Mask_List = [[numpy.array([numpy.array(mask)-numpy.array([crop_xL,crop_yT]) for mask in myo_Mask]) for myo_Mask,myo_frame in zip(myo_maskType_List,myo_frame_List)] for myo_maskType_List in [apical_myo_Mask_List,basal_myo_Mask_List]] 
    mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List  = [numpy.array([numpy.array(markers) - numpy.array([crop_xL,crop_yT]) for markers in markers_List]) for markers_List in [mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List]]
    myo_frame_List = numpy.array([myo_frame[crop_yT:crop_yB,crop_xL:crop_xR] for myo_frame in myo_frame_List])
    # construct-piv-from-end-points
    bulk_piv_List  = [numpy.subtract(bulk_piv_dir,bulk_markers) for bulk_piv_dir,bulk_markers in zip(bulk_piv_List,bulk_markers_List)]
    animal.ellipse_markers,animal.apical_myo_Mask_List,animal.basal_myo_Mask_List,animal.mid_markers_List,animal.bulk_markers_List,animal.bulk_piv_List,animal.apical_markers_List,animal.apical_markers_raw_List,animal.basal_markers_List,animal.basal_markers_raw_List,animal.myo_frame_List = [ellipse_markers,apical_myo_Mask_List,basal_myo_Mask_List,mid_markers_List,bulk_markers_List,bulk_piv_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,myo_frame_List]
    # update-frame-dimension
    y_dim,x_dim = myo_frame_List[0].shape[:2]
    animal.frameDimension = [x_dim,y_dim]
    animal.finalize()
    return animal