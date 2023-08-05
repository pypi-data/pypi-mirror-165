#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 20:29:28 2022

@author: bandan
"""
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable

from modelTissueFlow.modules import inOutTools
from modelTissueFlow.modules import fittingModule
from modelTissueFlow.modules import analysisModule
from modelTissueFlow.modules import equationModule

# color-list
colorsList = inOutTools.colors 
colorMaps = inOutTools.colorMaps

class Fitting1D:
    
    # initialize-animal 
    def __init__(self,curv_flag,hetFric_flag,parameters_FIXED):
        self.curv_flag = curv_flag
        self.hetFric_flag = hetFric_flag
        self.parameters_FIXED = parameters_FIXED
        
        return
    
    # update-animal 
    def update(self,s_fit,v_fit,fit_PARAMETERS):
        self.s_fit = s_fit
        self.v_fit = v_fit
        self.fit_PARAMETERS = fit_PARAMETERS
        
        return
        
class Model1D:
    
    # initialize-animal 
    def __init__(self,myoDomain,myoIntensity,ellipse_aspect_ratio,initial_myo_to_curv_offSet,ellipse_semi_a,reMarker_Number,cell_width,HETEROGENEOUS_friction_domain,physical_PARAMETERS,time_parameters):
        self.cell_width = cell_width
        self.time_step,time_max = time_parameters
        self.physical_PARAMETERS = physical_PARAMETERS
        self.time_range = numpy.arange(0,int(time_max)-1)
        self.curv_flag = 0 if physical_PARAMETERS[0] > 0 else 1
        self.hetFric_flag = 0 if physical_PARAMETERS[0] == 0 else 1
        self.HETEROGENEOUS_friction_domain = HETEROGENEOUS_friction_domain
        self.mid_markers_ini = inOutTools.ellipse(ellipse_semi_a=ellipse_semi_a,ellipse_semi_b=ellipse_semi_a/ellipse_aspect_ratio-1e-3,numNode=2*reMarker_Number)
        self.intersection_scale_factor,self.ref_coordinate_orientation = inOutTools.set_ellipse_origin_on_semi_minor_axis(ellipse_semi_a,ellipse_semi_a/ellipse_aspect_ratio-1e-3,self.mid_markers_ini)
        self.mid_markers_ref = inOutTools.shift_origin_of_polygon_contour(self.mid_markers_ini,initial_myo_to_curv_offSet,self.intersection_scale_factor,self.ref_coordinate_orientation)
        self.model_curv_List = []
        self.model_markers_List = []
        self.model_apical_myo_List = []
        self.model_heteroGenFriction_List = []
        self.model_v_inhomoFriction_PBC_List = []
        self.model_v_sp_avg_inhomoFriction_PBC = []
        self.model_apical_myo_patch_indices_List = []
        self.model_v_sp_avg_homoFriction_PBC_theo = []
     
        return
    
    # update-animal 
    def update(self,curv,apical_myo,updated_markers,heteroGenFriction,v_inhomoFriction_PBC,v_sp_avg_inhomoFriction_PBC,apical_myo_patch_indices,v_sp_avg_homoFriction_PBC_theo):
        self.model_curv_List.append(curv)
        self.model_apical_myo_List.append(apical_myo)
        self.model_markers_List.append(updated_markers)
        self.model_heteroGenFriction_List.append(heteroGenFriction)
        self.model_v_inhomoFriction_PBC_List.append(v_inhomoFriction_PBC)
        self.model_apical_myo_patch_indices_List.append(apical_myo_patch_indices)
        self.model_v_sp_avg_inhomoFriction_PBC.append(v_sp_avg_inhomoFriction_PBC)
        self.model_v_sp_avg_homoFriction_PBC_theo.append(v_sp_avg_homoFriction_PBC_theo)
        
        return
        
class Animal1D:
    
    # initialize-animal 
    def __init__(self,ID,dirPath,posterior_domain,initial_frame,frame_Min_Max,reMarker_Number,apical_off_set,basal_off_set,posterior_pole_location,epithelium_orientation):
        self.ID = ID
        self.initial_frame = initial_frame
        self.posterior_domain = posterior_domain
        self.marker_frame_indices,self.frameSequence_MEM_PAIRS,self.frameSequence_MYO,self.frameSequence_MARKERS,self.animal_reference_axis,self.ellipse_fit_centre,self.x_ref_axis,self.y_ref_axis,self.anterior_ref_marker,self.posterior_ref_marker,self.animal_markers_ref,self.ellipse_markers,self.frameDimension = analysisModule.imageJ_frames_to_frame_pairs(dirPath,frame_Min_Max,reMarker_Number,apical_off_set,basal_off_set,posterior_pole_location,epithelium_orientation)                                                                                                                                                      
        self.e_h_List = []
        self.curv_List = []
        self.s_mic_List = []
        self.bulk_piv_List = []
        self.mem_frame_List = []
        self.myo_frame_List = []
        self.basal_myo_List = []
        self.frameIndex_List = []
        self.apical_myo_List = []
        self.piv_normal_List = []
        self.mid_markers_List = []
        self.bulk_markers_List = []
        self.basal_markers_List = []
        self.apical_markers_List = []
        self.basal_myo_Mask_List = []
        self.apical_myo_Mask_List = []
        self.mem_frame_masked_List = []
        self.myo_frame_masked_List = []
        self.piv_tan_sign_mag_List = []
        self.basal_markers_raw_List = []
        self.apical_markers_raw_List = []
        self.basal_myo_pixel_distributed_List = []
        self.apical_myo_pixel_distributed_List = []
        
        return
    
    # update-animal 
    def update(self,e_h,curv,s_mic,mem_frame,mem_frame_masked,myo_frame,myo_frame_masked,basal_myo,frameIndex,apical_myo,piv_normal,piv_tangent,bulk_piv,mid_markers,bulk_markers,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,basal_polygon_Mask,apical_polygon_Mask,apical_myo_pixel_distributed,basal_myo_pixel_distributed):
        self.e_h_List.append(e_h)
        self.curv_List.append(curv)
        self.s_mic_List.append(s_mic)
        self.bulk_piv_List.append(bulk_piv)
        self.mem_frame_List.append(mem_frame)
        self.myo_frame_List.append(myo_frame)
        self.basal_myo_List.append(basal_myo)
        self.frameIndex_List.append(frameIndex)
        self.apical_myo_List.append(apical_myo)
        self.piv_normal_List.append(piv_normal)
        self.mid_markers_List.append(mid_markers)
        self.bulk_markers_List.append(bulk_markers)
        self.basal_markers_List.append(basal_markers)
        self.piv_tan_sign_mag_List.append(piv_tangent)
        self.apical_markers_List.append(apical_markers)
        self.mem_frame_masked_List.append(mem_frame_masked)
        self.myo_frame_masked_List.append(myo_frame_masked)
        self.basal_myo_Mask_List.append(basal_polygon_Mask)
        self.apical_myo_Mask_List.append(apical_polygon_Mask)
        self.basal_markers_raw_List.append(basal_markers_raw)
        self.apical_markers_raw_List.append(apical_markers_raw)
        self.basal_myo_pixel_distributed_List.append(basal_myo_pixel_distributed)
        self.apical_myo_pixel_distributed_List.append(apical_myo_pixel_distributed)
        
        return
        
    # temporally-alligned-information-of-animal 
    def include_allignment_information(self,transition_detection_information,transition_frame_indx,full_piv_avg,full_apical_myo_avg,pos_piv_avg,pos_apical_myo_avg,vitelline_space):
        self.vitelline_space = vitelline_space
        self.pos_piv_avg = pos_piv_avg
        self.full_piv_avg = full_piv_avg
        self.pos_apical_myo_avg = pos_apical_myo_avg
        self.full_apical_myo_avg = full_apical_myo_avg
        self.transition_frame_indx = transition_frame_indx
        self.transition_detection_information = transition_detection_information 
        
        return
    
    # finalization
    def finalize(self):
        self.piv_tan_dir_List = [numpy.reshape([t_dir*vec for t_dir,vec in zip(tangents_normals[0],piv_tan)],(-1,2)) for tangents_normals,piv_tan in zip([inOutTools.tangent_normals_along_polygon(item,closed=False) for item in self.mid_markers_List],self.piv_tan_sign_mag_List)]
        self.pvec_tan_mag_List = [numpy.sqrt(piv_tan_dir[:,0]**2+piv_tan_dir[:,1]**2) for piv_tan_dir in self.piv_tan_dir_List]
        self.bulk_piv_dir_List = [numpy.reshape(bulk_piv,(-1,2)) for bulk_piv in self.bulk_piv_List]
        self.bulk_pvec_mag_List = [numpy.array([numpy.linalg.norm(v) for v in bulk_piv]) for bulk_piv in self.bulk_piv_dir_List]
        
        return
    
    # visualization
    def view_frames(self,path,parameters,figFormat='png'):
        # delete-existing-images
        inOutTools.delete_files_with_specific_extension(path +'/'+ self.ID,'.' + figFormat)
        frameIndex_List,mid_markers_List,bulk_markers_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,myo_frame_List,piv_tan_sign_mag_List,piv_tan_dir_List,pvec_tan_mag_List,bulk_piv_dir_List,bulk_pvec_mag_List,apical_myo_Mask_List,basal_myo_Mask_List,apical_myo_pixel_distributed_List,basal_myo_pixel_distributed_List = [self.frameIndex_List,self.mid_markers_List,self.bulk_markers_List,self.apical_markers_List,self.apical_markers_raw_List,self.basal_markers_List,self.basal_markers_raw_List,self.myo_frame_List,self.piv_tan_sign_mag_List,self.piv_tan_dir_List,self.pvec_tan_mag_List,self.bulk_piv_dir_List,self.bulk_pvec_mag_List,self.apical_myo_Mask_List,self.basal_myo_Mask_List,self.apical_myo_pixel_distributed_List,self.basal_myo_pixel_distributed_List]
        # epithelium: full/posterior ? 
        truncate_data = [mid_markers_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,piv_tan_sign_mag_List,piv_tan_dir_List,pvec_tan_mag_List,apical_myo_Mask_List,basal_myo_Mask_List,apical_myo_pixel_distributed_List,basal_myo_pixel_distributed_List]
        mid_markers_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,piv_tan_sign_mag_List,piv_tan_dir_List,pvec_tan_mag_List,apical_myo_Mask_List,basal_myo_Mask_List,apical_myo_pixel_distributed_List,basal_myo_pixel_distributed_List = [inOutTools.truncate_Data_Range(item,self.posterior_domain) if parameters['view_posterior_domain'] else item for item in truncate_data] 
        # extract-myo-color-map 
        intensity_apical_basal_all_colorMap_List = numpy.swapaxes(numpy.array([analysisModule.extract_intensityColorMap(apical_intensity,basal_intensity,apical_polygon_Mask,basal_polygon_Mask,self.frameDimension) for apical_intensity,basal_intensity,apical_polygon_Mask,basal_polygon_Mask in zip(apical_myo_pixel_distributed_List,basal_myo_pixel_distributed_List,apical_myo_Mask_List,basal_myo_Mask_List)]),0,1) 
        apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List = intensity_apical_basal_all_colorMap_List
        # min-max-limit-of-data
        apical_myo_lim,basal_myo_lim,all_myo_intensity_map_myo_lim,piv_mag_lim = inOutTools.get_min_max_of_Data([apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List,pvec_tan_mag_List])
        ####################
        # loop-over-frames #
        ####################
        ellipse_center = numpy.mean(self.ellipse_markers,axis=0)
        for frame_counter,(frame_indx,mid_markers,bulk_markers,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,myo_frame,piv_tan_sig,piv_tan_dir,pvec_tan_mag,bulk_piv_dir,bulk_piv_mag,apical_myo_colorMap,basal_myo_colorMap,all_myo_colorMap,apical_myo_Mask,basal_myo_Mask) in enumerate(zip(frameIndex_List,mid_markers_List,bulk_markers_List,apical_markers_List,apical_markers_raw_List,basal_markers_List,basal_markers_raw_List,myo_frame_List,piv_tan_sign_mag_List,piv_tan_dir_List,pvec_tan_mag_List,bulk_piv_dir_List,bulk_pvec_mag_List,apical_myo_colorMap_List,basal_myo_colorMap_List,all_myo_colorMap_List,apical_myo_Mask_List,basal_myo_Mask_List)):     
            myo_frame = inOutTools.adjustBrightnessImage(numpy.copy(myo_frame),brightNessParam=int(parameters['brightNess']))       
           ####################
            # reference-frames #
            ####################
            if parameters['view_reference_frames']:
                FIG_split, (AB_ax,Edge_ax) = plt.subplots(2, 1, figsize = (5,4))
                # map-markers/ellipse-on-frame 
                for axis in [AB_ax,Edge_ax]:
                    axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                ellipse_ref_line = inOutTools.open_to_closed_polygon(self.ellipse_markers)
                AB_ax.plot(ellipse_ref_line[:,0],ellipse_ref_line[:,1], c = 'b', lw = 0.5) 
                # map-lateral-edge-position-on-frame 
                apical_line = inOutTools.open_to_closed_polygon(apical_markers_raw)
                basal_line = inOutTools.open_to_closed_polygon(basal_markers_raw)
                Edge_ax.plot(apical_line[:,0],apical_line[:,1], c = 'r', ls = '--', lw = 0.5)
                Edge_ax.plot(basal_line[:,0],basal_line[:,1], c = 'b', ls = '--', lw = 0.5)
                for marker_type_counter,(m,a,b) in enumerate(zip(mid_markers[:],apical_markers[:],basal_markers[:])):
                    Edge_ax.scatter(a[0],a[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                    Edge_ax.scatter(m[0],m[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                    Edge_ax.scatter(b[0],b[1], c = colorsList[marker_type_counter], marker = 'o', s = 0.1)
                    Edge_ax.add_line(Line2D([a[0],m[0]],[a[1],m[1]], c = colorsList[marker_type_counter], lw = 0.5))
                    Edge_ax.add_line(Line2D([m[0],b[0]],[m[1],b[1]], c = colorsList[marker_type_counter], lw = 0.5))
                # reference-origin/orientation
                mid_markers_orientation_patch = mid_markers[0:5]
                for axis_counter,axis in enumerate([AB_ax,Edge_ax]):    
                    axis.plot([mid_markers[0][0],ellipse_center[0]],[mid_markers[0][1],ellipse_center[1]], c = 'r', ls = '-', lw = 0.5) 
                    axis.plot(mid_markers_orientation_patch[:,0],mid_markers_orientation_patch[:,1], c = 'c', ls = '--', lw = 0.5) 
                AB_ax.axis('off')
                Edge_ax.axis('off') 
                figName = path +'/'+ self.ID + '/Fig_readOut_' + str(frame_indx) + '.' + figFormat
                inOutTools.deleteFile(figName)
                FIG_split.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_split)       
            #########################
            # myo-masks/mid-markers #
            #########################
            if parameters['view_myo_masks']:   
                FIG_midline,mask_ax = plt.subplots(1,1,figsize = (8,4))
                mask_ax.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else mask_ax.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                # myo-masks: apical/basal 
                for maskType in [apical_myo_Mask,basal_myo_Mask]:
                    mask_ax.add_collection(PatchCollection([Polygon(polygon,True) for polygon in maskType] , facecolors = 'w', edgecolors = 'k',linewidths= 0.5)) 
                # mid-markers-and-lateral-edges 
                for indx,(a,m,b) in enumerate(zip(apical_markers,mid_markers,basal_markers)):
                    # mid-markers 
                    m_x,m_y = m
                    mask_ax.scatter(m_x,m_y, c = 'g', marker = 'o',s = 2.0, zorder = 2)
                    # lateral-edges 
                    a_x,a_y = a
                    b_x,b_y = b
                    mask_ax.add_line(Line2D([a_x,m_x,b_x],[a_y,m_y,b_y], c = 'w', lw = 0.5,zorder=1))
                mask_ax.axis('off')
                figName = path +'/'+ self.ID + '/FIG_midline_ref_' + str(frame_indx) + '.' +  figFormat
                inOutTools.deleteFile(figName)
                FIG_midline.savefig(figName,format = figFormat, figsize=(10, 3),dpi=500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_midline)       
            #############################
            # piv/myo-map-oriented-color #
            ##############################
            if parameters['view_piv_oriented_color']:
                FIG_piv_tan_myo,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4)) 
                # piv-tangent-map 
                img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                piv_color = ['y' if piv <= 0 else 'r' for piv in piv_tan_sig]
                if not numpy.all((pvec_tan_mag == 0)): 
                    img_piv_tan_myo_axis.quiver(mid_markers[:,0],mid_markers[:,1], piv_tan_dir[:,0], piv_tan_dir[:,1],color = piv_color,angles ='xy',scale = parameters['piv_scale_factor'], width = 0.003,zorder=2) # cmap : inOutTools.transparent_cmap(plt.get_cmap('rainbow'))
                img_piv_tan_myo_axis.axis('off')
                # save-figure 
                figName = path +'/'+ self.ID + '/FIG_piv_oriented_' + str(frame_indx) + '.' + figFormat
                inOutTools.deleteFile(figName)
                FIG_piv_tan_myo.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_piv_tan_myo)       
            ################
            # bulk-piv-map #
            ################
            if parameters['view_bulk_piv']:
                FIG_piv_tan_myo,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4))
                # piv-tangent-map 
                img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                divider = make_axes_locatable(img_piv_tan_myo_axis)
                if not numpy.all((bulk_piv_mag == 0)): 
                    cax_piv_tan = divider.append_axes("left", size="5%", pad=0.05)
                    img = img_piv_tan_myo_axis.quiver(bulk_markers[:,0],bulk_markers[:,1],bulk_piv_dir[:,0],bulk_piv_dir[:,1],bulk_piv_mag,angles ='xy',cmap = 'nipy_spectral',scale = 6.0*parameters['piv_scale_factor'], width = 0.003,zorder=2) # cmap : inOutTools.transparent_cmap(plt.get_cmap('rainbow'))
                   # img.set_clim(bulk_piv_mag_lim[0],bulk_piv_mag_lim[-1])  
                    FIG_piv_tan_myo.colorbar(img, ax = img_piv_tan_myo_axis, cax = cax_piv_tan)
                    cax_piv_tan.yaxis.set_ticks_position("left")
                #cax_piv_tan.tick_params(labelsize=20) 
                img_piv_tan_myo_axis.tick_params(axis='both', which='major', labelsize=18)
                img_piv_tan_myo_axis.axis('off')
                # save-figure 
                figName = path +'/'+ self.ID + '/FIG_bulk_piv_' + str(frame_indx) + '.' + figFormat
                inOutTools.deleteFile(figName)
                FIG_piv_tan_myo.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_piv_tan_myo)      
            ########################
            # piv/myo-map-together #
            ########################
            if parameters['view_piv_myo_together']:
                FIG_piv_tan_myo,img_piv_tan_myo_axis = plt.subplots(1,1,figsize = (8,4))
                # piv-tangent-map 
                img_piv_tan_myo_axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else img_piv_tan_myo_axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                divider = make_axes_locatable(img_piv_tan_myo_axis)
                if not numpy.all((pvec_tan_mag == 0)): 
                    cax_piv_tan = divider.append_axes("left", size="5%", pad=0.05)
                    img = img_piv_tan_myo_axis.quiver(mid_markers[:,0],mid_markers[:,1], piv_tan_dir[:,0], piv_tan_dir[:,1],piv_tan_sig,angles ='xy',cmap = 'nipy_spectral',scale = parameters['piv_scale_factor'], width = 0.003,zorder=2) # cmap : inOutTools.transparent_cmap(plt.get_cmap('rainbow'))
                    img.set_clim(piv_mag_lim[0],piv_mag_lim[-1])  
                    FIG_piv_tan_myo.colorbar(img, ax = img_piv_tan_myo_axis, cax = cax_piv_tan)
                    cax_piv_tan.yaxis.set_ticks_position("left")
                # apical/basal-myosin-map 
                if not numpy.all((all_myo_colorMap == 0)):
                    cax_myo = divider.append_axes("right", size="5%", pad=0.05)
                    img = img_piv_tan_myo_axis.imshow(all_myo_colorMap,cmap = inOutTools.transparent_cmap(plt.get_cmap(colorMaps[162])),interpolation = 'none',origin = 'upper',zorder=2)
                    img.set_clim(all_myo_intensity_map_myo_lim[0],all_myo_intensity_map_myo_lim[-1]) 
                    FIG_piv_tan_myo.colorbar(img, ax = img_piv_tan_myo_axis, cax = cax_myo)
                    cax_myo.yaxis.set_ticks_position("right")
                #cax_piv_tan.tick_params(labelsize=20) 
                img_piv_tan_myo_axis.tick_params(axis='both', which='major', labelsize=18)
                img_piv_tan_myo_axis.axis('off')
                # save-figure 
                figName = path +'/'+ self.ID + '/FIG_piv_myo_tog_' + str(frame_indx) + '.' + figFormat
                inOutTools.deleteFile(figName)
                FIG_piv_tan_myo.savefig(figName,figsize=(10, 3), format = figFormat, dpi = 500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_piv_tan_myo)    
            ###############################
            # piv/myo-map-seperate-panels #
            ###############################
            if parameters['view_piv_myo_separately']:
                FIG_piv_myo,(imgPIVtan_ax,img_apical_myo_ax,img_basal_myo_ax) = plt.subplots(3,1,figsize = (8,12))
                # piv-tangent-map 
                imgPIVtan_ax.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else imgPIVtan_ax.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                divider_tan = make_axes_locatable(imgPIVtan_ax)
                if not numpy.all((pvec_tan_mag == 0)): 
                    cax_piv_tan = divider_tan.append_axes("right", size="5%", pad=0.05)
                    img = imgPIVtan_ax.quiver(mid_markers[:,0], mid_markers[:,1], piv_tan_dir[:,0], piv_tan_dir[:,1],pvec_tan_mag,angles ='xy',cmap = inOutTools.transparent_cmap(plt.get_cmap('rainbow')),scale = parameters['piv_scale_factor'], width = 0.003,zorder=2)
                    img.set_clim(piv_mag_lim[0],piv_mag_lim[-1]) 
                    FIG_piv_myo.colorbar(img, ax = imgPIVtan_ax, cax = cax_piv_tan)
                    cax_piv_tan.yaxis.set_ticks_position("right")
                imgPIVtan_ax.axis('off')
                # apical/basal-myosin-map 
                for axis_counter,(axis,axis_lim,intensity_colorMap) in enumerate(zip([img_apical_myo_ax,img_basal_myo_ax],[apical_myo_lim,basal_myo_lim],[apical_myo_colorMap,basal_myo_colorMap])):
                    axis.imshow(myo_frame[:,:,0], interpolation = 'nearest', cmap = 'gray_r', origin = 'upper') if parameters['invert_RGB'] else axis.imshow(myo_frame, interpolation = 'nearest', cmap = 'gray', origin = 'upper')
                    divider = make_axes_locatable(axis)
                    if not numpy.all((intensity_colorMap == 0)):
                        cax_myo = divider.append_axes("right", size="5%", pad=0.05)
                        img = axis.imshow(intensity_colorMap,cmap = inOutTools.transparent_cmap(plt.get_cmap(colorMaps[162])),interpolation = 'none',origin = 'upper',zorder=2)
                        img.set_clim(axis_lim[0],axis_lim[-1]) 
                        FIG_piv_myo.colorbar(img, ax = axis, cax = cax_myo)
                        cax_myo.yaxis.set_ticks_position("right")
                img_apical_myo_ax.axis('off')
                img_basal_myo_ax.axis('off')
                # reference-mark-tracking 
                if parameters['view_reference_mark_tracking']: 
                    for axis_counter,axis in enumerate([imgPIVtan_ax,img_apical_myo_ax,img_basal_myo_ax]):
                        for ref_mark_counter,(ref_indx,x_dis,y_dis,ref_col) in enumerate(zip([0,len(mid_markers)//4,len(mid_markers)//2,3*len(mid_markers)//4],[-50,0,50,0],[0,-50,0,50],['r','m','b','orange'])):
                            axis.scatter(mid_markers[:,0][ref_indx],mid_markers[:,1][ref_indx], marker = 'o', s = 50.0,facecolors = ref_col,edgecolors = 'k',zorder = 5) 
                            x = [mid_markers[:,0][ref_indx],ellipse_center[0]]
                            y = [mid_markers[:,1][ref_indx],ellipse_center[1]]
                            axis.plot(x,y, c = ref_col, ls = '--', lw = 1.0)
                # save-figure 
                figName = path +'/'+ self.ID + '/FIG_piv_myo_sep_' + str(frame_indx) + '.' + figFormat
                inOutTools.deleteFile(figName)
                FIG_piv_myo.savefig(figName,format = figFormat, figsize=(10, 3),dpi=500, bbox_inches='tight', pad_inches=0.01)
                plt.close(FIG_piv_myo)
        
        ########################
        # transition detection #
        ########################
        piv_transition_cutOff_val,piv_fitting_range,piv_transition_steepness_coeff = self.transition_detection_information
        if piv_transition_cutOff_val > 0.0:
            FIG_piv_tan_sp_avg,piv_tangent_sp_avg_ax = plt.subplots(1,1,figsize = (2.6,1.3))
            # raw-piv-avg-data
            piv_tangent_sp_avg_ax.scatter(self.frameIndex_List,self.full_piv_avg, c = 'k', marker = 'o', s = 5,zorder=1,label = self.ID)
            # transition-references
            piv_tangent_sp_avg_ax.axvline(self.transition_frame_indx, c = 'm', ls = '-', lw = 1.0)
            fit_line = numpy.poly1d(piv_transition_steepness_coeff)
            frameIndex_List_regression = numpy.linspace(self.transition_frame_indx,self.frameIndex_List[-1],10) 
            piv_tangent_sp_avg_ax.plot(frameIndex_List_regression,fit_line(frameIndex_List_regression) , ls  = '--', c = 'm', lw = 1.0,zorder=2)
            # cut-off-references
            piv_tangent_sp_avg_ax.axhspan(0.0,piv_transition_cutOff_val, alpha=0.5, facecolor='r',edgecolor='none') 
            piv_tangent_sp_avg_ax.axhspan(piv_transition_cutOff_val,self.full_piv_avg[piv_fitting_range-1], alpha=0.5, facecolor='g',edgecolor='none')
            piv_tangent_sp_avg_ax.axhspan(self.full_piv_avg[piv_fitting_range-1],max(self.full_piv_avg),alpha=0.5, facecolor='r',edgecolor='none') 
            # highlight-transition-region
            piv_tangent_sp_avg_ax.axhline(0.0 ,  ls  = '--', c = 'k', lw = 1.0,zorder=3)
            piv_tangent_sp_avg_ax.set_ylim([-piv_transition_cutOff_val,max(self.full_piv_avg)+piv_transition_cutOff_val])
            piv_tangent_sp_avg_ax.tick_params(axis='both', which='major', labelsize=5)
            piv_tangent_sp_avg_ax.margins(x=0)
            piv_tangent_sp_avg_ax.legend(loc=2, prop={'size': 3})
            # save-figure
            figName = path +'/'+ self.ID  + '/FIG_transition_cutoff=' + str(piv_transition_cutOff_val) + '.' + figFormat
            inOutTools.deleteFile(figName)
            FIG_piv_tan_sp_avg.savefig(figName,format = figFormat, figsize=(10, 3), dpi = 500, bbox_inches='tight', pad_inches=0.01)
            plt.close(FIG_piv_tan_sp_avg)  
            
        return
    
class System1D:
    
    # initialize-system 
    def __init__(self,ID,path,animals,indv_emb_piv_not_alligned,indv_emb_piv_alligned,full_apical_myo_not_alligned,full_apical_myo_alligned,pos_piv_not_alligned,pos_piv_alligned,pos_apical_myo_not_alligned,pos_apical_myo_alligned,vitelline_space_not_alligned,vitelline_space_alligned,transition_indiv_frame_reference,transition_merge_frame_reference,spatial_shift_by_node_index,normalized_epithelium,time_between_frames,pix_mic,sec_min):
        self.ID = ID
        self.path = path
        self.sec_min = sec_min
        self.pix_mic = pix_mic
        self.ANIMALS = animals
        self.pos_piv_alligned = pos_piv_alligned
        self.time_between_frames = time_between_frames
        self.pos_piv_not_alligned = pos_piv_not_alligned
        self.normalized_epithelium = normalized_epithelium
        self.indv_emb_piv_alligned = indv_emb_piv_alligned
        self.pos_apical_myo_alligned = pos_apical_myo_alligned
        self.vitelline_space_alligned = vitelline_space_alligned
        self.full_apical_myo_alligned = full_apical_myo_alligned
        self.indv_emb_piv_not_alligned = indv_emb_piv_not_alligned
        self.spatial_shift_by_node_index = spatial_shift_by_node_index
        self.pos_apical_myo_not_alligned = pos_apical_myo_not_alligned
        self.full_apical_myo_not_alligned = full_apical_myo_not_alligned
        self.vitelline_space_not_alligned = vitelline_space_not_alligned
        self.transition_indiv_frame_reference = transition_indiv_frame_reference
        self.transition_merge_frame_reference = transition_merge_frame_reference
        self.pos_avg_emb_piv_alligned = [numpy.ma.mean(self.pos_piv_alligned,axis=0),numpy.ma.std(self.pos_piv_alligned,axis=0)]
        self.full_avg_emb_piv_alligned  = [numpy.ma.mean(self.indv_emb_piv_alligned,axis=0),numpy.ma.std(self.indv_emb_piv_alligned,axis=0)]
        self.full_avg_emb_piv_not_alligned = [numpy.ma.mean(indv_emb_piv_not_alligned,axis=0),numpy.ma.std(indv_emb_piv_not_alligned,axis=0)]
        self.time_List = []
        self.s_time_series = []
        self.s_std_time_series = []
        self.eh_time_series = []
        self.eh_std_time_series = []
        self.mom_time_series = []
        self.mom_std_time_series = []
        self.curv_time_series = []
        self.curv_std_time_series = []
        self.s_ref_time_series = []
        self.s_ref_std_time_series = []
        self.myo_frames_List = []
        self.eh_curv_time_series = []
        self.eh_curv_std_time_series = []
        self.mid_markers_List = []
        self.piv_tan_time_series = []
        self.piv_tan_std_time_series = []
        self.piv_norm_time_series = []
        self.piv_norm_std_time_series = []
        self.total_myo_time_series = []
        self.total_myo_std_time_series = []
        self.basal_myo_time_series = []
        self.basal_myo_std_time_series = []
        self.apical_myo_time_series = []
        self.apical_myo_std_time_series = []
        self.piv_tanGrad_time_series = []
        self.piv_tanGrad_std_time_series = []
        self.mom_curvGrad_time_series = []
        self.mom_curvGrad_std_time_series = []
        self.curv_momGrad_time_series = []
        self.curv_momGrad_std_time_series = []
        self.basal_myoGrad_time_series = []
        self.basal_myoGrad_std_time_series = []
        self.total_myoGrad_time_series = []
        self.total_myoGrad_std_time_series = []
        self.apical_myoGrad_time_series = []
        self.apical_myoGrad_std_time_series = []
        self.basal_mom_curvGrad_time_series = []
        self.basal_mom_curvGrad_std_time_series = []
        self.curv_basal_myoGrad_time_series = []
        self.curv_basal_myoGrad_std_time_series = []
        self.apical_mom_curvGrad_time_series = []
        self.apical_mom_curvGrad_std_time_series = []
        self.curv_apical_myoGrad_time_series = []
        self.curv_apical_myoGrad_std_time_series = []
        self.piv_tanGrad_correction_time_series = []
        self.piv_tanGrad_correction_std_time_series = []
        self.piv_correction_factor_Grad_time_series = []
        self.piv_correction_factor_Grad_std_time_series = []
        
        return
    
    # update-system 
    def update(self,time,s_avg,s_std,eh_avg,eh_std,eh_curv_avg,eh_curv_std,mom_avg,mom_std,curv_avg,curv_std,s_ref_avg,s_ref_std,piv_tan_avg,piv_tan_std,piv_tanGrad_avg,piv_tanGrad_std,piv_tanGrad_correction_avg,piv_tanGrad_correction_std,piv_norm_avg,piv_norm_std,total_myo_avg,total_myo_std,basal_myo_avg,basal_myo_std,apical_myo_avg,apical_myo_std,mom_curvGrad_avg,mom_curvGrad_std,curv_momGrad_avg,curv_momGrad_std,basal_myoGrad_avg,basal_myoGrad_std,total_myoGrad_avg,total_myoGrad_std,apical_myoGrad_avg,apical_myoGrad_std,basal_mom_curvGrad_avg,basal_mom_curvGrad_std,curv_basal_myoGrad_avg,curv_basal_myoGrad_std,apical_mom_curvGrad_avg,apical_mom_curvGrad_std,curv_apical_myoGrad_avg,curv_apical_myoGrad_std,piv_correction_factor_Grad_avg,piv_correction_factor_Grad_std,myo_frames,mid_markers):
        self.time_List.append(time)
        self.s_time_series.append(s_avg)
        self.s_std_time_series.append(s_std)
        self.eh_time_series.append(eh_avg)
        self.eh_std_time_series.append(eh_std)
        self.mom_time_series.append(mom_avg)
        self.mom_std_time_series.append(mom_std)
        self.curv_time_series.append(curv_avg)
        self.curv_std_time_series.append(curv_std)
        self.s_ref_time_series.append(s_ref_avg)
        self.s_ref_std_time_series.append(s_ref_std)
        self.myo_frames_List.append(myo_frames)
        self.eh_curv_time_series.append(eh_curv_avg)
        self.eh_curv_std_time_series.append(eh_curv_std)
        self.mid_markers_List.append(mid_markers)
        self.piv_tan_time_series.append(piv_tan_avg)
        self.piv_tan_std_time_series.append(piv_tan_std)
        self.piv_norm_time_series.append(piv_norm_avg)
        self.piv_norm_std_time_series.append(piv_norm_std)
        self.total_myo_time_series.append(total_myo_avg)
        self.total_myo_std_time_series.append(total_myo_std)
        self.basal_myo_time_series.append(basal_myo_avg)
        self.basal_myo_std_time_series.append(basal_myo_std)
        self.apical_myo_time_series.append(apical_myo_avg)
        self.apical_myo_std_time_series.append(apical_myo_std)
        self.piv_tanGrad_time_series.append(piv_tanGrad_avg)
        self.piv_tanGrad_std_time_series.append(piv_tanGrad_std)
        self.mom_curvGrad_time_series.append(mom_curvGrad_avg)
        self.mom_curvGrad_std_time_series.append(mom_curvGrad_std)
        self.curv_momGrad_time_series.append(curv_momGrad_avg)
        self.curv_momGrad_std_time_series.append(curv_momGrad_std)
        self.basal_myoGrad_time_series.append(basal_myoGrad_avg)
        self.basal_myoGrad_std_time_series.append(basal_myoGrad_std)
        self.total_myoGrad_time_series.append(total_myoGrad_avg)
        self.total_myoGrad_std_time_series.append(total_myoGrad_std)
        self.apical_myoGrad_time_series.append(apical_myoGrad_avg)
        self.apical_myoGrad_std_time_series.append(apical_myoGrad_std)
        self.basal_mom_curvGrad_time_series.append(basal_mom_curvGrad_avg)
        self.basal_mom_curvGrad_std_time_series.append(basal_mom_curvGrad_std)
        self.curv_basal_myoGrad_time_series.append(curv_basal_myoGrad_avg)
        self.curv_basal_myoGrad_std_time_series.append(curv_basal_myoGrad_std)
        self.apical_mom_curvGrad_time_series.append(apical_mom_curvGrad_avg)
        self.apical_mom_curvGrad_std_time_series.append(apical_mom_curvGrad_std)
        self.curv_apical_myoGrad_time_series.append(curv_apical_myoGrad_avg)
        self.curv_apical_myoGrad_std_time_series.append(curv_apical_myoGrad_std)
        self.piv_tanGrad_correction_time_series.append(piv_tanGrad_correction_avg)
        self.piv_tanGrad_correction_std_time_series.append(piv_tanGrad_correction_std)
        self.piv_correction_factor_Grad_time_series.append(piv_correction_factor_Grad_avg)
        self.piv_correction_factor_Grad_std_time_series.append(piv_correction_factor_Grad_std)
        
        return
    
    # visualization
    def view_piv(self,path,figFormat):
        path = path + '/plot_avg'
        # delete-existing-images
        inOutTools.delete_files_with_specific_extension(path,'.' + figFormat)
        ################
        # temporal-piv #
        ################
        FIG_piv_phase_sep, FIG_piv_phase_sep_axes = plt.subplots(2,4,figsize = (10,3))
        piv_raw_ax,piv_all_ax,piv_sym_ax,piv_asym_ax = FIG_piv_phase_sep_axes[0]
        piv_raw_avg_ax,piv_alligned_avg_ax,piv_sym_avg_ax,piv_asym_avg_ax = FIG_piv_phase_sep_axes[1] 
        transition_time = self.transition_merge_frame_reference*self.time_between_frames
        #*****************************#
        # PIV-individual-over-animals #
        #*****************************#
        animalTypes = numpy.array([animal.ID for animal in self.ANIMALS])
        for emb_counter,(piv_all_raw,piv_all_alligned) in enumerate(zip(self.indv_emb_piv_not_alligned,self.indv_emb_piv_alligned)):
            # piv-not-alligned
            time_raw = [indx*self.time_between_frames for indx in range(len(piv_all_raw))]
            piv_raw_ax.plot(time_raw,piv_all_raw,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            piv_raw_ax.axvline(self.transition_indiv_frame_reference[emb_counter]*self.time_between_frames,c=colorsList[emb_counter],alpha = 0.3,ls='--',lw = 1.0)
            # piv-alligned 
            time_all = [indx*self.time_between_frames-transition_time for indx in range(len(piv_all_alligned))]
            piv_all_ax.plot(time_all,piv_all_alligned,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            # piv-sym
            piv_sym = piv_all_alligned[:self.transition_merge_frame_reference+1]
            time_sym = [indx*self.time_between_frames-transition_time for indx in range(len(piv_sym))]
            piv_sym_ax.plot(time_sym,piv_sym,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
            # piv-asym
            piv_asym = piv_all_alligned[self.transition_merge_frame_reference:]
            time_asym = [indx*self.time_between_frames for indx in range(len(piv_asym))]
            piv_asym_ax.plot(time_asym,piv_asym,c=colorsList[emb_counter],ls = '-', lw = 0.5, marker = 'o',ms = 2.0,label=animalTypes[emb_counter])
        # sym-asym-transition-reference 
        piv_all_ax.axvline(0.0,c='k',alpha = 0.3,ls='--',lw = 1.0)
        for axis_counter,axis in enumerate([piv_raw_ax,piv_all_ax,piv_sym_ax,piv_asym_ax]): 
            axis.margins(x=0)
            axis.legend(loc=2, prop={'size': 2})
            axis.axhline(0.0,ls='--',c='k',lw=1.0,zorder=3)
            axis.tick_params(axis='both', which='major', labelsize=5)
        #**************************#
        # PIV-average-over-animals #
        #**************************#
        for emb_counter,(piv_all_raw,piv_all_alligned) in enumerate(zip([self.full_avg_emb_piv_not_alligned],[self.full_avg_emb_piv_alligned])): 
            # piv-not-alligned
            piv_avg, piv_std = piv_all_raw
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_raw_avg_ax.plot(time_avg,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_raw_avg_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-alligned
            piv_avg, piv_std = piv_all_alligned
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_alligned_avg_ax.plot(time_avg-transition_time,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_alligned_avg_ax.fill_between(time_avg-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-sym
            piv_avg, piv_std = [item[:self.transition_merge_frame_reference+1] for item in piv_all_alligned]
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_sym_avg_ax.plot(time_avg-transition_time,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_sym_avg_ax.fill_between(time_avg-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
            # piv-asym
            piv_avg, piv_std = [item[self.transition_merge_frame_reference:] for item in piv_all_alligned]
            time_avg = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)]) 
            piv_asym_avg_ax.plot(time_avg,piv_avg,c = 'k', ls  = '-', marker = 'o', ms = 2.0, lw = 0.5,zorder=1,label='animal average') 
            piv_asym_avg_ax.fill_between(time_avg,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
        piv_alligned_avg_ax.axvline(0.0,c='k',alpha = 0.3,ls='--',lw = 1.0)    
        for axis_counter,axis in enumerate([piv_raw_avg_ax,piv_alligned_avg_ax,piv_sym_avg_ax,piv_asym_avg_ax]): 
             axis.margins(x=0)
             axis.legend(loc=2, prop={'size': 2})
             axis.axhline(0.0,ls='--',c='k',lw=1.0,zorder=3)
             axis.tick_params(axis='both', which='major', labelsize=5)   
        FIG_piv_phase_sep.savefig(path +'/FIG_steps_of_allign.' + figFormat, format = figFormat, figsize=(10, 3), dpi = 500,bbox_inches ='tight',pad_inches = 0)
        plt.close(FIG_piv_phase_sep)
        
        ##############################
        # piv-avg: full-vs-posterior #
        ##############################
        FIG_piv_full_pos,full_pos_ax = plt.subplots(1,1,figsize = (2.6,1.7))
        # full
        piv_avg,piv_std  = self.pos_avg_emb_piv_alligned
        pos_time = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)])
        full_pos_ax.plot(pos_time-transition_time,piv_avg,c = 'r', ls  = '-', lw = 1,zorder=1,label='posterior-epithelium')  
        full_pos_ax.fill_between(pos_time-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='r',alpha= 0.3)
        # posterior
        piv_avg,piv_std  = self.full_avg_emb_piv_alligned
        full_time = numpy.ma.array([item*self.time_between_frames for item in range(piv_avg.size)])
        full_pos_ax.plot(full_time-transition_time,piv_avg,c = 'k', ls  = '-', lw = 1,zorder=1,label='full-epithelium') 
        full_pos_ax.fill_between(full_time-transition_time,piv_avg-piv_std,piv_avg+piv_std,facecolor='k',alpha= 0.3)
        # axis-atributes
        full_pos_ax.margins(x=0)
        full_pos_ax.legend(loc=2, prop={'size': 3})
        full_pos_ax.axhline(0.0, ls='--', c='k', lw=0.5, zorder=3)
        full_pos_ax.tick_params(axis='both', which='major', labelsize=3)
        FIG_piv_full_pos.savefig(path +'/FIG_piv_full_vs_pos' + '.' + figFormat,format = figFormat, figsize=(10, 3), dpi = 500,bbox_inches ='tight',pad_inches = 0.01)
        plt.close(FIG_piv_full_pos)
        
        ###############
        # spatial-piv #
        ###############
        time_List,s_avg_List,eh_avg_List,eh_std_List,eh_curv_avg_List,eh_curv_std_List,piv_tan_avg_List,piv_tan_std_List,piv_tanGrad_avg_List,piv_tanGrad_std_List,piv_tanGrad_correction_avg_List,piv_tanGrad_correction_std_List,curv_avg_List,curv_std_List,apical_myo_avg_List,apical_myo_std_List,basal_myo_avg_List,basal_myo_std_List,curv_momGrad_avg_List,curv_momGrad_std_List = [numpy.array(item)[numpy.array([item*2 for item in self.time_List],int)] for item in [self.time_List,self.s_time_series,self.eh_time_series,self.eh_std_time_series,self.eh_curv_time_series,self.eh_curv_std_time_series,self.piv_tan_time_series,self.piv_tan_std_time_series,self.piv_tanGrad_time_series,self.piv_tanGrad_std_time_series,self.piv_tanGrad_correction_time_series,self.piv_tanGrad_correction_std_time_series,self.curv_time_series,self.curv_std_time_series,self.apical_myo_time_series,self.apical_myo_std_time_series,self.basal_myo_time_series,self.basal_myo_std_time_series,self.curv_momGrad_time_series,self.curv_momGrad_std_time_series]]
        curv_lim,v_lim,basal_myo_lim,apical_myo_lim = [[numpy.amin(curv_avg_List-curv_std_List),numpy.amax(curv_avg_List+curv_std_List)],[numpy.amin(piv_tan_avg_List-piv_tan_std_List),numpy.amax(piv_tan_avg_List+piv_tan_std_List)],[numpy.amin(basal_myo_avg_List-basal_myo_std_List),numpy.amax(basal_myo_avg_List+basal_myo_std_List)],[numpy.amin(apical_myo_avg_List-apical_myo_std_List),numpy.amax(apical_myo_avg_List+apical_myo_std_List)]]
        for time_indx,(t,s,eh_avg,eh_std,eh_curv_avg,eh_curv_std,piv_avg,piv_std,piv_Grad_avg,piv_Grad_std,piv_Grad_correction_avg,piv_Grad_correction_std,curv_avg,curv_std,apical_myo_avg,apical_myo_std,basal_myo_avg,basal_myo_std,curv_momGrad_avg,curv_momGrad_std) in enumerate(zip(time_List,s_avg_List,eh_avg_List,eh_std_List,eh_curv_avg_List,eh_curv_std_List,piv_tan_avg_List,piv_tan_std_List,piv_tanGrad_avg_List,piv_tanGrad_std_List,piv_tanGrad_correction_avg_List,piv_tanGrad_correction_std_List,curv_avg_List,curv_std_List,apical_myo_avg_List,apical_myo_std_List,basal_myo_avg_List,basal_myo_std_List,curv_momGrad_avg_List,curv_momGrad_std_List)):
            FIG, axes = plt.subplots(2, 2, figsize=(6,3))
            v_ax,basal_myo_ax = axes[0]
            apical_myo_ax,curv_ax = axes[1]
            s_ref = s-s[self.spatial_shift_by_node_index]
            for axis_counter,(axis,axis_lim,meas_avg,meas_std) in enumerate(zip([v_ax,curv_ax,apical_myo_ax,basal_myo_ax],[v_lim,curv_lim,apical_myo_lim,basal_myo_lim],[piv_avg,curv_avg,apical_myo_avg,basal_myo_avg],[piv_std,curv_std,apical_myo_std,basal_myo_std])):
                axis.plot(s_ref,meas_avg, c='k',lw=1.0, ls='-')
                axis.fill_between(s_ref,meas_avg-meas_std,meas_avg+meas_std, facecolor='k', alpha=0.3)
                axis.margins(x=0)
                axis.axhline(0.0, ls='--', c='k', lw=0.5, zorder=3)
                axis.axvline(0.0, ls='--', c='k', lw=0.5, zorder=3)
                axis.tick_params(axis='both', which='major', labelsize=3)
                axis.set_ylim(axis_lim)
            FIG.savefig(path + '/Measurables_' + str(t - self.time_List[self.transition_merge_frame_reference]) + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.05)
            plt.close(FIG)
            
        return

class tissueFlow1D:
    
    #####################
    # initialize-tissue #
    #####################
    def __init__(self,parameters,path,frameIndex_Maps={},transition_cutOff_val=0.0):
        self.inOut_path = path
        self.parameters = parameters
        self.frameIndex_Maps = frameIndex_Maps
        self.transition_cutOff_val = transition_cutOff_val
        # float-parameters
        self.sec_min = self.parameters['sec_min']
        self.pix_mic = self.parameters['pix_mic']
        self.time_between_frames = self.parameters['time_between_frames']
        # integer-parameters
        self.crop_margin = int(self.parameters['crop_margin'])
        self.window_avg_SIZE = int(self.parameters['window_avg_SIZE']) 
        self.spatial_shift_by_node_index = int(self.parameters['spatial_shift_by_node_index'])
        # bool-parameters
        self.temporal_allignment = self.parameters['temporal_allignment']
        self.normalized_epithelium = self.parameters['normalized_epithelium']
        self.normalize_myosin_intensity = self.parameters['normalize_myosin_intensity']
        self.spatial_allignment_anterior_posterior = self.parameters['spatial_allignment_anterior_posterior']
        
        return
    
    #############
    # modelling #
    #############
    def run_MODEL(self,model_parameters,figFormat):
        path = self.inOut_path +'/model'
        inOutTools.delete_files_with_specific_extension(path,'.' + figFormat)
        # parameters
        ra = model_parameters['ra']
        rb = model_parameters['rb']
        gamma_del = model_parameters['gamma_del']
        myoDomains_List = [int(ele) for ele in model_parameters['myoDomains_List']] if isinstance(model_parameters['myoDomains_List'],list) else [int(model_parameters['myoDomains_List'])]
        myoIntensity_List,ellipse_aspect_ratio_List,initial_myo_to_curv_offSet_List = [[float(ele) for ele in item] if isinstance(item,list) else [item] for item in [model_parameters['myoIntensity_List'],model_parameters['ellipse_aspect_ratio_List'],model_parameters['initial_myo_to_curv_offSet_List']]]
        #*************#
        # start-model #
        #*************#
        plot_instances = 0
        FIG_sim,Simulation_ax = plt.subplots(1, 1, figsize = (1.8,1.3))
        FIG_theo,Theoretical_ax = plt.subplots(1, 1, figsize = (1.8,1.3))
        FIG_v_predict_param_dep, v_predict_param_dep_ax = plt.subplots(1, 1, figsize=(2.6,1.3))
        for AR in ellipse_aspect_ratio_List:
            for IC_offSet in initial_myo_to_curv_offSet_List:
                for mD in myoDomains_List: 
                    for mI in myoIntensity_List:
                        MODEL = Model1D(mD,mI,AR,IC_offSet,ellipse_semi_a=500,reMarker_Number=100,cell_width=60,HETEROGENEOUS_friction_domain=3,physical_PARAMETERS=[gamma_del,0.0,1.0,ra,rb,1.0,1.0],time_parameters=model_parameters['time_parameters']) 
                        # default-origin-at-the-anterior-end-of-myo-patch 
                        half_length_myosin_patch = 2*mD*(len(MODEL.mid_markers_ini)+1) # myo-patch-length
                        origin_shift_index =  half_length_myosin_patch//200 # normalize-by-number-of-epithelial-cells ~ 200 cells 
                        markers = numpy.roll(MODEL.mid_markers_ref,-origin_shift_index, axis=0) 
                        # myo-centre-displacement/starting-frame 
                        ds_next = 0.0  
                        markers_start_ref = numpy.copy(markers) 
                        #*************#
                        # time-series #
                        #*************#
                        for time_indx in MODEL.time_range:
                            numNode = len(markers)
                            max_node_indx = numNode - 1
                            numNode_myo_domain = 2*mD-2
                            # position-of-the-myosin-patch-centre 
                            markers_centre_ref = inOutTools.numpy.array(inOutTools.Polygon(MODEL.mid_markers_ref).centroid.coords).flatten()
                            ref_intersetion_axis = numpy.array([markers_centre_ref + 2*(MODEL.intersection_scale_factor)*MODEL.ref_coordinate_orientation,markers_centre_ref])
                            _,myo_shift_detection_parameters = inOutTools.reset_starting_point_of_polygon(inOutTools.copy_DATA(markers),1.0*ref_intersetion_axis)
                            myo_marker_L,myo_indx_L = myo_shift_detection_parameters 
                            m_R_apical = max_node_indx - 1
                            m_L_apical = m_R_apical - 2*numNode_myo_domain
                            m_patch_apical = numpy.arange(m_L_apical,m_R_apical+1)
                            s_pix,_ = inOutTools.arc_length_along_polygon(markers)
                            m_patch_apical_centre_indx = int(numpy.average(m_patch_apical))
                            # equation-inputs: pix-to-mic 
                            curv = inOutTools.smooth_data(inOutTools.curvature_along_polygon(markers,closed=True))
                            lengths,inv_length,areas = inOutTools.unit_conversion_Length_inverseLength_Area([s_pix,MODEL.cell_width],[curv],[],self.pix_mic)
                            s,e_h = lengths
                            curv, = inv_length
                            # equation-inputs: effective 
                            s_norm = s/s[-1] 
                            apical_myo = numpy.zeros_like(s_pix)
                            apical_myo[m_patch_apical] = mI 
                            basal_myo = numpy.zeros_like(s_pix)
                            apical_mom = 0.5*e_h*apical_myo
                            basal_mom = 0.5*e_h*basal_myo
                            apical_myo_grad = inOutTools.gradients_of_data(s_norm,apical_myo,uniform_sampling=True,closed=True) 
                            basal_myo_grad = inOutTools.gradients_of_data(s_norm,basal_myo,uniform_sampling=True,closed=True)
                            curv_grad = inOutTools.gradients_of_data(s_norm,curv,uniform_sampling=True,closed=True)
                            v_grad_correction = numpy.zeros_like(s_norm)
                            heteroGenFriction = inOutTools.rectangular_function(s,[0,MODEL.HETEROGENEOUS_friction_domain]) 
                            apical_mom_curv_grad = apical_mom*curv_grad
                            basal_mom_curv_grad = basal_mom*curv_grad
                            INPUT = [apical_myo_grad,basal_myo_grad,apical_mom_curv_grad,basal_mom_curv_grad,v_grad_correction]
                            # simulation 
                            v_inhomoFriction_PBC,friction = equationModule.prediction_by_equation(s_norm,INPUT,MODEL.hetFric_flag*heteroGenFriction,inOutTools.numpy.zeros_like(heteroGenFriction),'PERIODIC',MODEL.physical_PARAMETERS,tension_flag=1.0,curvature_flag=MODEL.curv_flag,v_grad_correction_flag=0.0,distinguish_myo_switch=True) 
                            v_sp_avg_inhomoFriction_PBC = inOutTools.area_under_curve(s_norm,v_inhomoFriction_PBC,closed=False)/s_norm[-1]
                            apical_myo_patch_indices = numpy.where(apical_myo)[0]
                            apical_myo_patch_indices = numpy.insert(apical_myo_patch_indices,[0,len(apical_myo_patch_indices)],[apical_myo_patch_indices[0]-1,apical_myo_patch_indices[-1]+1],axis=0)
                            # theoretical 
                            F_R,F_L = [0,MODEL.HETEROGENEOUS_friction_domain]
                            F_R = F_R - 2 if F_R > 0 else F_R
                            heterogeneous_friction_contribution = inOutTools.area_under_curve(s_norm[F_R:F_L+2],(friction[F_R:F_L+2]-1)*v_inhomoFriction_PBC[F_R:F_L+2],closed=False)
                            curvature_contribution = -1.0*MODEL.curv_flag*(1/MODEL.physical_PARAMETERS[2])*(MODEL.physical_PARAMETERS[3]*inOutTools.area_under_curve(s_norm,apical_mom*curv_grad,closed=True) - MODEL.physical_PARAMETERS[4]*inOutTools.area_under_curve(s_norm,basal_mom*curv_grad,closed=True))
                            v_sp_avg_homoFriction_PBC_theo = curvature_contribution - heterogeneous_friction_contribution
                            # update-time-series-data
                            MODEL.update(curv,apical_myo,markers,heteroGenFriction,v_inhomoFriction_PBC,v_sp_avg_inhomoFriction_PBC,apical_myo_patch_indices,v_sp_avg_homoFriction_PBC_theo)
                            # update-mid-markers: time-evolution 
                            ds = v_inhomoFriction_PBC[m_patch_apical_centre_indx]*MODEL.time_step # micron
                            ds_normalized = ds/s[-1] # no-unit
                            ds_next += ds_normalized
                            markers_next = markers_start_ref #
                            markers =  inOutTools.shift_position_of_a_point_along_polygon(markers_next,ds_next,m_patch_apical_centre_indx)
                            markers = numpy.roll(markers,-origin_shift_index, axis=0)   
                        #***************#
                        # parameter-key #
                        #***************#
                        model_markers = MODEL.model_markers_List[-1] 
                        s,_ = inOutTools.arc_length_along_polygon(model_markers)
                        if len(ellipse_aspect_ratio_List) >1:
                            key = 'AR = ' + str(AR)
                        elif len(myoIntensity_List) > 1: 
                            key = 'I = ' + str(round(mI,2))
                        elif len(myoDomains_List) > 1: 
                            key = 'ML = ' + str(round(2*mD*numpy.average(s[1:]-s[:-1])*self.pix_mic,2)) 
                        elif len(initial_myo_to_curv_offSet_List) > 1:
                            key = 'OFF-SET = ' + str(IC_offSet) 
                        else:
                            key = ' ' 
                        #***************#
                        # configuration #
                        #***************#
                        apical_myo_patch_indices = MODEL.model_apical_myo_patch_indices_List[-1]
                        apical_myo_patch_coordinates = model_markers[apical_myo_patch_indices]
                        if plot_instances == 1:
                            FIG_v_predict_config, v_predict_config_ax = plt.subplots(1, 1, figsize=(2.6,1.3))
                            # ellipse-contour
                            markers_line = numpy.insert(model_markers,0,model_markers[-1],axis=0)
                            v_predict_config_ax.plot(markers_line[:,0],markers_line[:,1],c='k',ls = '-',lw = 1.0,alpha = 1.0,zorder=2)  
                            # posterior-pole-reference
                            s,_ = inOutTools.arc_length_along_polygon(model_markers)
                            curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s[-1],MODEL.model_curv_List[-1],[1.0,0.0],height=0.0,sorted_peaks=False)
                            posterior_pole = model_markers[curv_peak_indx_second]  
                            ellipse_centre = numpy.average(model_markers,axis = 0) 
                            v_predict_config_ax.plot([ellipse_centre[0],posterior_pole[0]],[ellipse_centre[1],posterior_pole[1]],ls='--', c='k', lw=1.0, zorder=3) 
                            # myosin-patch-reference
                            myo_centre_index = apical_myo_patch_indices[len(apical_myo_patch_indices)//2]
                            myo_centre = model_markers[myo_centre_index]
                            v_predict_config_ax.plot(apical_myo_patch_coordinates[:,0],apical_myo_patch_coordinates[:,1],c='g',ls = '-',lw = 2.0,zorder=10) 
                            v_predict_config_ax.plot([ellipse_centre[0],myo_centre[0]],[ellipse_centre[1],myo_centre[1]],ls='--', c='g', lw=1.0, zorder=3) 
                            # friction 
                            if gamma_del:
                                hetFriction = MODEL.model_heteroGenFriction_List[-1]
                                if numpy.count_nonzero(hetFriction):
                                    friction_patch_indices = numpy.where(hetFriction)[0]
                                    friction_patch_coordinates = model_markers[friction_patch_indices]
                                    v_predict_config_ax.plot(friction_patch_coordinates[:,0],friction_patch_coordinates[:,1],c='m',ls = '-',lw = 2.0,alpha = 1.0,zorder=3)        
                            v_predict_config_ax.tick_params(axis='both', which='major', labelsize=3) 
                            # save-fig: config
                            FIG_v_predict_config.savefig(path + '/FIG_config' + '.' + figFormat, format = figFormat, dpi=500, bbox_inches='tight', pad_inches=0.02)
                            plt.close(FIG_v_predict_config)
                        #***#
                        # v #
                        #***#
                        last_time_indx = len(MODEL.model_markers_List)-1 
                        # redefined-arc-length-reference: at-posterior-curvature-peak
                        s,s_max  = inOutTools.arc_length_along_polygon(MODEL.model_markers_List[last_time_indx])  
                        curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s_max,MODEL.model_curv_List[last_time_indx],[0.5,0.0],height=0.0,sorted_peaks=False)
                        numNode = len(MODEL.model_markers_List[last_time_indx])
                        shift_indx = numNode -curv_peak_indx_second - int(0.31*numNode)  # -origin-shift-by, ds = 0.31
                        m,v,f,myo,curv = [numpy.roll(item,shift_indx,axis=0) for item in [MODEL.model_markers_List[last_time_indx],MODEL.model_v_inhomoFriction_PBC_List[last_time_indx],MODEL.model_heteroGenFriction_List[last_time_indx],MODEL.model_apical_myo_List[last_time_indx],MODEL.model_curv_List[last_time_indx]]]
                        s,s_max = inOutTools.arc_length_along_polygon(m)
                        curv_peak_indx_first,curv_peak_indx_second = inOutTools.detection_of_peak_pairs_in_defined_region(s/s_max,curv,[0.5,0.0],height=0.0,sorted_peaks=False)
                        s = s/s_max
                        s = s - s[curv_peak_indx_second]
                        # v 
                        v_predict_param_dep_ax.plot(s, v, c =colorsList[plot_instances], lw = 1.0, ls = '-',label = key)
                        curv_ax = v_predict_param_dep_ax.twinx()
                        curv_ax.plot(s, curv, c =colorsList[plot_instances], lw = 1.0, ls = '-',label = key)
                        # myosin
                        range_myo = list(numpy.where(myo > 0)[0])
                        if range_myo:
                            myo_ax = v_predict_param_dep_ax.twinx()
                            range_myo_start,range_myo_end = [range_myo[0],range_myo[-1]]
                            myo_ax.axvspan(s[range_myo_start],s[range_myo_end+1],color='g',alpha = 0.5,linewidth=0.0,zorder=2)
                            myo_ax.axis('off') 
                        # friction
                        if gamma_del:
                            range_fric = list(numpy.where(f > 0)[0])
                            if range_fric:
                                fric_ax = v_predict_param_dep_ax.twinx()
                                range_fric_start,range_fric_end = [range_fric[0],range_fric[-1]]
                                fric_ax.axvspan(s[range_fric_start-1],s[range_fric_end],color='m',alpha = 0.5,linewidth=0.0,zorder=2)
                                fric_ax.axis('off') 
                        v_predict_param_dep_ax.axvline(s[curv_peak_indx_second], c =colorsList[plot_instances], lw = 1.0, ls = '-')
                        v_predict_param_dep_ax.margins(x=0) 
                        #*******#
                        # v-avg #
                        #*******#
                        for color_indx,(v_sp_avg,v_sp_avg_ax,line_style) in enumerate(zip([MODEL.model_v_sp_avg_inhomoFriction_PBC,MODEL.model_v_sp_avg_homoFriction_PBC_theo],[Simulation_ax,Theoretical_ax],['-','--'])):
                            v_sp_avg_ax.plot(MODEL.time_range*MODEL.time_step,v_sp_avg,c=colorsList[plot_instances],markerfacecolor=colorsList[plot_instances], markeredgecolor=colorsList[plot_instances], ls = line_style, zorder=2,label = key)   
                        # increase-plot-number 
                        plot_instances += 1
        # save-figure: v-avg 
        for axis in [Simulation_ax,Theoretical_ax,v_predict_param_dep_ax]:
            axis.margins(x=0) 
            axis.legend(loc=0, prop={'size': 2.0})
            axis.axhline(0.0, ls='--', c='k', lw=1.0, zorder=3)
            axis.tick_params(axis='both', which='major', labelsize=8)
        # v-avg-theo
        FIG_theo.savefig(path + '/FIG_v_avg_theo' + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_theo)
        # v-avg-sim
        FIG_sim.savefig(path + '/FIG_v_avg_sim' + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_sim)
        # save-figure: v 
        FIG_v_predict_param_dep.savefig(path + '/FIG_v_sim'  + '.' + figFormat, format = figFormat, dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(FIG_v_predict_param_dep)
        
        return
    
    ###########
    # fitting #
    ###########
    def run_FITTING(self,GENOTYPE,fitting_parameters,hypothesis,changingParameter,parameters_FIXED,BOUNDARY_COND_SWITCH,spatial_fitting_domain,fit_piv_Type,figFormat):
        tmin,tmax = [int(ele) for ele in fitting_parameters['time_range']]
        simultaneous_fitting = fitting_parameters['simultaneous_fitting'] 
        friction_domainSize,friction_domainLocation = [int(ele) for ele in fitting_parameters['friction_domainSize_domainLocation']]
        viscosity_domainSize,viscosity_domainLocation = [int(ele) for ele in fitting_parameters['viscosity_domainSize_domainLocation']]
        p_guess = [[item] for item in [float(fitting_parameters['gamma_del']),float(fitting_parameters['eta_del']),float(fitting_parameters['lh']),float(fitting_parameters['ra']),float(fitting_parameters['rb']),float(fitting_parameters['gamma_factor']),float(fitting_parameters['eta_factor'])]]
        #********************#
        # process-input-data #
        #********************#
        # time-range-for-fitting
        time_range = numpy.arange(tmin,tmax+1)
        full_avg_emb_piv_alligned_avg,full_avg_emb_piv_alligned_std,time_List,s_ref_time_series,s_time_series,apical_myo_time_series,apical_myo_std_time_series,basal_myo_time_series,basal_myo_std_time_series,piv_norm_time_series,piv_norm_std_time_series,piv_tan_time_series,piv_tan_std_time_series,piv_correction_factor_Grad_time_series,piv_correction_factor_Grad_std_time_series,total_myoGrad_time_series,apical_myoGrad_time_series,basal_myoGrad_time_series,apical_mom_curvGrad_time_series,curv_apical_myoGrad_time_series,basal_mom_curvGrad_time_series,curv_basal_myoGrad_time_series,mom_curvGrad_time_series,curv_momGrad_time_series,mid_markers_List,myo_frames_List = [numpy.array(item)[time_range+GENOTYPE.transition_merge_frame_reference] for item in [GENOTYPE.full_avg_emb_piv_alligned[0],GENOTYPE.full_avg_emb_piv_alligned[1],GENOTYPE.time_List,GENOTYPE.s_ref_time_series,GENOTYPE.s_time_series,GENOTYPE.apical_myo_time_series,GENOTYPE.apical_myo_std_time_series,GENOTYPE.basal_myo_time_series,GENOTYPE.basal_myo_std_time_series,GENOTYPE.piv_norm_time_series,GENOTYPE.piv_norm_std_time_series,GENOTYPE.piv_tan_time_series,GENOTYPE.piv_tan_std_time_series,GENOTYPE.piv_correction_factor_Grad_time_series,GENOTYPE.piv_correction_factor_Grad_std_time_series,GENOTYPE.total_myoGrad_time_series,GENOTYPE.apical_myoGrad_time_series,GENOTYPE.basal_myoGrad_time_series,GENOTYPE.apical_mom_curvGrad_time_series,GENOTYPE.curv_apical_myoGrad_time_series,GENOTYPE.basal_mom_curvGrad_time_series,GENOTYPE.curv_basal_myoGrad_time_series,GENOTYPE.mom_curvGrad_time_series,GENOTYPE.curv_momGrad_time_series,GENOTYPE.mid_markers_List,GENOTYPE.myo_frames_List] ]
        # heterogeneous-friction
        time_series_friction_star_ref = inOutTools.numpy.array([friction_domainLocation  for time_frame in time_range])
        heteroGenFriction = numpy.array([inOutTools.rectangular_function(s, numpy.array([friction_center-friction_domainSize//2,friction_center+friction_domainSize//2])) for s, friction_center in zip(s_time_series,time_series_friction_star_ref)])
        # heterogeneous-viscosity
        time_series_viscosity_center_ref = inOutTools.numpy.array([viscosity_domainLocation  for time_frame in time_range])
        heteroGenViscosity = numpy.array([inOutTools.rectangular_function(s, numpy.array([viscosity_center-viscosity_domainSize//2,viscosity_center+viscosity_domainSize//2])) for s, viscosity_center in zip(s_time_series,time_series_viscosity_center_ref)])
        # hypothesis-initialization
        hetVisco_flag = 0 if viscosity_domainSize == 0 else 1
        hetFric_flag = 0 if (hypothesis == 'tension' or hypothesis == 'curvature') else 1
        curv_flag =  0 if (hypothesis == 'tension' or hypothesis == 'friction') else 1
        # input-data-for-fitting 
        eff_heteroGenFriction = hetFric_flag*heteroGenFriction 
        eff_heteroGenViscosity = hetVisco_flag*heteroGenViscosity
        time_ref = GENOTYPE.time_List[GENOTYPE.transition_merge_frame_reference]
        s_res_List = numpy.array([s-s[GENOTYPE.spatial_shift_by_node_index] for s in s_time_series])
        v_grad_correction_List = numpy.array([s[-1]*pcf for s, pcf in zip(s_ref_time_series, piv_correction_factor_Grad_time_series)]) if GENOTYPE.normalized_epithelium else piv_correction_factor_Grad_time_series
        model_INPUT_avg = [s_res_List,s_time_series,piv_tan_time_series, total_myoGrad_time_series, apical_myoGrad_time_series, basal_myoGrad_time_series,mom_curvGrad_time_series,-1.0 *curv_apical_myoGrad_time_series,-1.0 *curv_basal_myoGrad_time_series,v_grad_correction_List] 
        model_INPUT_avg_updated = numpy.array(model_INPUT_avg + [eff_heteroGenFriction] + [eff_heteroGenViscosity])
        #*********#
        # fitting #
        #*********#
        s_fit = None
        v_fit = None
        fit_PARAMETERS = None
        # guessed-parameters
        parameter_INDEXING = {'gamma_del': 0,'eta_del': 1,'lh': 2,'ra': 3,'rb': 4,'gamma_factor': 5,'eta_factor': 6}
        time_dependent_parameter_indx = int(parameter_INDEXING[changingParameter]) if changingParameter is not None else None
        PARAMETER_guess = [param*s_time_series.shape[0] if item_indx == time_dependent_parameter_indx else param for item_indx,param in enumerate(p_guess)] if time_dependent_parameter_indx is not None else p_guess.copy()
        # fixed-parameters
        parameters_FIXED = {parameter_INDEXING[k]: v for k, v in parameters_FIXED.items()}
        parameters_FIXED = {**parameters_FIXED,**{parameter_INDEXING['gamma_factor']:1.0,parameter_INDEXING['eta_factor']:1.0}} if changingParameter is None else{**parameters_FIXED,**{parameter_INDEXING['gamma_factor']:1.0,parameter_INDEXING['eta_factor']:1.0}} if changingParameter == 'eta_del' else{**parameters_FIXED,**{parameter_INDEXING['gamma_factor']:1.0,parameter_INDEXING['eta_factor']:1.0}} if changingParameter == 'lh' else {**parameters_FIXED,**{parameter_INDEXING['gamma_factor']:1.0,parameter_INDEXING['eta_factor']:1.0}} if changingParameter == 'rb' else {**parameters_FIXED,**{parameter_INDEXING['gamma_factor']:1.0}} if changingParameter == 'eta_factor' else {**parameters_FIXED,**{parameter_INDEXING['eta_factor']:1.0}} if changingParameter == 'gamma_factor' else parameters_FIXED
        parameters_FIXED = parameters_FIXED if hetFric_flag else {**parameters_FIXED,**{parameter_INDEXING['gamma_del']:0.0}}
        parameters_FIXED = parameters_FIXED if hetVisco_flag else {**parameters_FIXED,**{parameter_INDEXING['eta_del']:0.0}}  
        FIT = Fitting1D(curv_flag,hetFric_flag,parameters_FIXED)
        # fitting-switches
        piv_fittingDomain_List = numpy.arange(spatial_fitting_domain[0],spatial_fitting_domain[-1]) if spatial_fitting_domain else numpy.arange(0, s_ref_time_series.shape[-1])
        # simultaneous-fitting
        if simultaneous_fitting:
            print('simultinious fitting')
            fit_PARAMETERS,v_fit,chiSQ,s_fit = fittingModule.curve_fitting_and_prediction(model_INPUT_avg_updated,piv_fittingDomain_List,BOUNDARY_COND_SWITCH,PARAMETER_guess,tension_flag=1.0,curvature_flag=curv_flag,v_grad_correction_flag=0,distinguish_myo_switch=True,fix_PARAMETERS=parameters_FIXED,fit_piv_avg=fit_piv_Type) 
        # individual-fitting
        else:
            print('individual fitting')
            fit_PARAMETERS_v_fit_chiSQ_s_fit_List = numpy.array([fittingModule.curve_fitting_and_prediction(model_INPUT,piv_fittingDomain_List,BOUNDARY_COND_SWITCH,p_guess.copy(),tension_flag=1.0,curvature_flag=curv_flag,v_grad_correction_flag=0,distinguish_myo_switch=True,fix_PARAMETERS=parameters_FIXED,fit_piv_avg=fit_piv_Type) for model_INPUT in numpy.swapaxes(model_INPUT_avg_updated,0,1)])
            fit_PARAMETERS_indv,v_fit,chiSQ,s_fit = [fit_PARAMETERS_v_fit_chiSQ_s_fit_List[:,indx] for indx in range(fit_PARAMETERS_v_fit_chiSQ_s_fit_List.shape[1])]
            fit_PARAMETERS = fit_PARAMETERS_indv[0]
            if time_dependent_parameter_indx is not None: 
                fit_PARAMETERS[time_dependent_parameter_indx] = [list(numpy.concatenate(param).flat)[time_dependent_parameter_indx] for param in fit_PARAMETERS_indv]
        # update-FIT
        FIT.update(s_fit,v_fit,fit_PARAMETERS)
        #**********#
        # plotting #
        #**********#
        path = './movies/' + GENOTYPE.ID + '/fitting'
        inOutTools.delete_files_with_specific_extension(path,'.' + figFormat)
        # v-fit-piv 
        Fig_v_avg,v_predict_avg_ax = plt.subplots(1, 1, figsize=(2.6, 1.3)) 
        for time_counter,(s,v,s_ref,piv_tan_avg,piv_tan_std,hf,hv) in enumerate(zip(FIT.s_fit,FIT.v_fit,s_res_List,piv_tan_time_series,piv_tan_std_time_series,eff_heteroGenFriction,eff_heteroGenViscosity)): #s_res_List,piv_tan_time_series,piv_tan_std_time_series
            FIG_v,v_predict_ax = plt.subplots(1, 1, figsize=(2.6, 1.3))
            v_predict_ax.plot(s, v, c='b', ls='-',label = 'fittingl') # 'orange'
            v_predict_ax.plot(s_ref, piv_tan_avg, c='k', ls='-',label = 'experimental') # 'orange'
            v_predict_ax.fill_between(s_ref, piv_tan_avg-piv_tan_std,piv_tan_avg+piv_tan_std, facecolor='k', alpha=0.2)
            # friction
            range_fric = list(numpy.where(hf > 0)[0])
            if range_fric:
                range_fric_start,range_fric_end = [range_fric[0],range_fric[-1]] 
                fric_ax = v_predict_ax.twinx()
                fric_ax.axvspan(s[range_fric_start],s[range_fric_end],color='m',alpha = 0.3,linewidth=0.0,zorder=2)
                fric_ax.margins(x=0)
                fric_ax.axis('off')
            # viscosity
            range_visco = list(numpy.where(hv > 0)[0]) 
            if range_visco:
                range_visco_start,range_visco_end = [range_visco[0],range_visco[-1]]
                visco_ax = v_predict_ax.twinx()
                visco_ax.axvspan(s[range_visco_start],s[range_visco_end],color='b',alpha = 0.3,linewidth=0.0,zorder=2)
                visco_ax.margins(x=0)
                visco_ax.axis('off')
            # axis-atributes    
            v_predict_ax.margins(x=0)
            v_predict_ax.axhline(0.0, ls='--', c='k', lw=0.5, zorder=3)
            v_predict_ax.axvline(0.0, ls='--', c='k', lw=0.5, zorder=3)
            v_predict_ax.tick_params(axis='both', which='major', labelsize=3)
            v_predict_ax.legend(loc=1, prop={'size': 2})
            FIG_v.savefig(path + '/FIG_v_' + str(time_counter) + '.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
            plt.close(FIG_v)
         # v-fit-piv-avg
        v_avg_predict = inOutTools.sliding_window_average_data([inOutTools.area_under_curve(s,v,closed=False)/s[-1] for s,v in zip(FIT.s_fit,FIT.v_fit)],window_SIZE=1) 
        v_predict_avg_ax.plot(time_List-time_ref,full_avg_emb_piv_alligned_avg,c = 'k', ls  = '-', lw = 1.0,zorder=1,label='experimental')
        v_predict_avg_ax.fill_between(time_List-time_ref,full_avg_emb_piv_alligned_avg-full_avg_emb_piv_alligned_std,full_avg_emb_piv_alligned_avg+full_avg_emb_piv_alligned_std,facecolor='k',alpha= 0.3)
        v_predict_avg_ax.plot(time_List-time_ref, inOutTools.sliding_window_average_data(v_avg_predict,window_SIZE=1), c='b', ls='-', lw=1.0, zorder=1)#,label= 'Length_high_eta = ' +  f'{e*0.01:.2f}' + str(hypothesis_param[hypothesis_counter])) 
        v_predict_avg_ax.margins(x=0)
        v_predict_avg_ax.axhline(0.0, ls='--', c='k', lw=0.5, zorder=3)
        v_predict_avg_ax.axvline(0.0, ls='--', c='k', lw=0.5, zorder=3)
        v_predict_avg_ax.tick_params(axis='both', which='major', labelsize=3)
        v_predict_avg_ax.legend(loc=1, prop={'size': 2})
        Fig_v_avg.savefig(path + '/FIG_v_avg.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
        plt.close(Fig_v_avg) 
        # time-dependent-parameter
        parameter_key = list(parameter_INDEXING.keys())
        if time_dependent_parameter_indx is not None:
            FIG,axis = plt.subplots(1, 1, figsize=(2.6, 1.3))
            axis.scatter(time_List-time_ref,fit_PARAMETERS[time_dependent_parameter_indx], marker='o', s=10.0,facecolors='g', edgecolors='k', zorder=1, ls='-', lw=0.5, label = parameter_key[time_dependent_parameter_indx])
            axis.margins(x=0)
            axis.axhline(0.0, ls='--', c='k', lw=0.5, zorder=3)
            axis.axvline(0.0, ls='--', c='k', lw=0.5, zorder=3)
            axis.tick_params(axis='both', which='major', labelsize=3)
            axis.legend(loc='best', prop={'size': 2})
            FIG.savefig(path + '/FIG_timeDepParam.' + figFormat, format = figFormat, figsize=(10, 3), dpi=500, bbox_inches='tight', pad_inches=0.02)
            plt.close(FIG)  
            
        return
    
    ##################
    # analyze-animal #
    ##################
    def analysis_ANIMAL(self,sys_ID,animal_ID):
        animal_reference,raw_frames = self.frameIndex_Maps[sys_ID][animal_ID]
        posterior_pole_location,epithelium_orientation = animal_reference
        initial_frame,segmented_frames = raw_frames
        # integer-parameters
        overlap = int(self.parameters['overlap'])
        reMarker_Number = int(self.parameters['reMarker_Number'])
        search_area_size = int(self.parameters['search_area_size'])
        layer_widths = [int(ele) for ele in self.parameters['layer_widths']]
        posterior_domain = numpy.array(self.parameters['posterior_domain'],int)
        piv_interpol_window_size = int(self.parameters['piv_interpol_window_size'])
        bulk_piv_refMarker_Number = int(self.parameters['bulk_piv_refMarker_Number'])
        # float-parameters
        piv_cutOff = self.parameters['piv_cutOff']
        piv_interpol_depth = self.parameters['piv_interpol_depth']
        basal_marker_position_off_set = self.parameters['basal_marker_position_off_set']
        apical_marker_position_off_set = self.parameters['apical_marker_position_off_set']
        # bool-parameters
        myoMask = self.parameters['myoMask']
        bulk_PIV = self.parameters['bulk_PIV']
        midline_PIV = self.parameters['midline_PIV']
        background_subtraction = self.parameters['background_subtraction']
        equal_midline_to_apical_basal_distance = self.parameters['equal_midline_to_apical_basal_distance']
        #*******************#
        # initialize-animal #
        #*******************#
        ANIMAL = Animal1D(animal_ID,self.inOut_path + '/movies' + '/' + sys_ID +'/'+animal_ID,posterior_domain,initial_frame,segmented_frames,reMarker_Number,apical_marker_position_off_set,basal_marker_position_off_set,posterior_pole_location,epithelium_orientation)
        for frame_counter,frame_indx in enumerate(ANIMAL.marker_frame_indices):
            # markers:apical/basal/midline 
            apical_markers_raw,basal_markers_raw,img_masks,frameDimension = analysisModule.extract_different_markers(ANIMAL.frameSequence_MARKERS[frame_counter],reMarker_Number,apical_marker_position_off_set,basal_marker_position_off_set,epithelium_orientation)
            apical_markers_ref,_ = inOutTools.reset_starting_point_of_polygon(apical_markers_raw,ANIMAL.animal_reference_axis)
            # extract-RGB-values/PIV-referencing-of-image-frames 
            mem_frame,myo_frame,mem_frame_masked,myo_frame_masked,RGB_scale_myo_pair,piv_frame_pair = analysisModule.process_frames_and_markers(ANIMAL.frameSequence_MEM_PAIRS[frame_counter],ANIMAL.frameSequence_MYO[frame_counter],ANIMAL.frameSequence_MARKERS[frame_counter],img_masks,background_subtraction)
            # spatial-orientation-of-animal 
            s,mid_markers,apical_markers,basal_markers = inOutTools.midline_polygon_from_a_pair_of_ploygons(apical_markers_raw,basal_markers_raw,start_point_intersetion_axis=ANIMAL.animal_reference_axis,equal_apical_basal_distance=equal_midline_to_apical_basal_distance)
            # apical/basal-markers-and-masks 
            apical_markers,basal_markers,apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask = analysisModule.apical_basal_markers_and_masks_with_respect_to_midline(mid_markers,apical_markers_raw,basal_markers_raw,apical_markers,basal_markers,frameDimension,layer_widths)
            # process-piv 
            piv_tan = None 
            piv_norm = None 
            # piv-raw 
            x,y,u,v,_ = analysisModule.calculate_PIV(inOutTools.copy_DATA(piv_frame_pair[0]),inOutTools.copy_DATA(piv_frame_pair[1]),piv_interpol_window_size,overlap,self.time_between_frames,search_area_size,'peak2peak',piv_cutOff)
            # piv-interpolation-markers
            normal_dir_outer,normDist_outer = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,apical_markers,direction='outer')
            normal_dir_inner,normDist_inner = inOutTools.nearest_distance_and_direction_to_one_polygon_from_another_polygon(mid_markers,basal_markers,direction='inner')
            sub_apical_markers = numpy.array([midPoint - piv_interpol_depth*normDist*norm for midPoint,norm,normDist in zip(mid_markers,normal_dir_outer,normDist_outer)])  
            sub_basal_markers = numpy.array([midPoint + piv_interpol_depth*normDist*norm for midPoint,norm,normDist in zip(mid_markers,normal_dir_inner,normDist_inner)])
            # piv-interpolation-at-mid-markers
            if midline_PIV: 
                piv_tan,piv_norm,_ = analysisModule.split_PIV_in_components(x,y,u,v,[sub_apical_markers,mid_markers,sub_basal_markers],piv_interpol_window_size)
            # piv-interpolation-at-apical-markers
            else: 
                piv_tan,piv_norm,_ = analysisModule.split_PIV_in_components(x,y,u,v,[sub_apical_markers],piv_interpol_window_size) 
            # piv-interpolation-at-bulk-markers 
            bulk_piv = numpy.copy(mid_markers)
            bulk_markers = numpy.zeros_like(mid_markers)
            if bulk_PIV:
                frame_center = 0.5*numpy.array(frameDimension)
                bulk_markers = inOutTools.points_within_pair_of_polygons(inOutTools.uniform_points_within_rectangle(frame_center,frame_center*0.9,bulk_piv_refMarker_Number)[::-1],polygon_out=apical_markers,polygon_in=basal_markers) 
                bulk_piv,_ = analysisModule.interpolate_PIV_around_markers([bulk_markers],piv_interpol_window_size,x,y,u,v)
            # process-myosin-intensity 
            apical_intensity_perPixel_perLength,basal_intensity_perPixel_perLength = analysisModule.extract_MYOSIN_intensity_and_colorMap(apical_polygon_Mask,basal_polygon_Mask,semi_apical_polygon_Mask,semi_basal_polygon_Mask,frameDimension,RGB_scale_myo_pair,myoMask,apical_polygon_Mask,basal_polygon_Mask)
            # process-active-moment-incredients: apical-myosin,basal-myosin,cell-height 
            e_h,apical_myo,basal_myo = analysisModule.extract_activeMoment_ingredients(apical_intensity_perPixel_perLength,basal_intensity_perPixel_perLength,mid_markers,apical_markers,basal_markers) 
            # process-curvature 
            curv = inOutTools.curvature_along_polygon(mid_markers,closed=True)
            # convert-data-from-pix-unit-to-mic-unit 
            areas = []
            lengths = [s,e_h,piv_tan,piv_norm]
            inv_length = [curv,apical_myo,basal_myo]
            lengths,inv_lengths,areas = inOutTools.unit_conversion_Length_inverseLength_Area(lengths,inv_length,areas,self.pix_mic)
            s_mic,e_h,piv_tan,piv_norm = lengths
            curv,apical_myo,basal_myo = inv_length       
            # update-animal-individual-frame-information 
            ANIMAL.update(e_h,curv,s_mic,mem_frame,mem_frame_masked,myo_frame,myo_frame_masked,basal_myo,frame_indx,apical_myo,piv_norm,piv_tan,bulk_piv,mid_markers,bulk_markers,apical_markers,apical_markers_raw,basal_markers,basal_markers_raw,basal_polygon_Mask,apical_polygon_Mask,apical_intensity_perPixel_perLength,basal_intensity_perPixel_perLength)
        #***********************************#
        # transition-detection: sym-to-asym #
        #***********************************#
        transition_cutOff_val = self.transition_cutOff_val if self.temporal_allignment else -1.0*self.transition_cutOff_val
        transition_steepness_coeff,transition_frame_indx,full_piv_avg,full_apical_myo_avg,pos_piv_avg,pos_apical_myo_avg,vitelline_space = analysisModule.time_allignmnet(ANIMAL,transition_cutOff_val,self.window_avg_SIZE) 
        if transition_frame_indx is None: 
            print('--> transition can not be detected: !!! add more frames OR reduce transition cut-off !!!')
        # include-animal-transition-information 
        ANIMAL.include_allignment_information(transition_steepness_coeff,transition_frame_indx,full_piv_avg,full_apical_myo_avg,pos_piv_avg,pos_apical_myo_avg,vitelline_space)  
        ANIMAL.finalize()
        
        return ANIMAL   
    
    ##################
    # analyze-system #
    ##################
    def analysis_SYSTEM(self,sys_ID):
        animal_Store = []
        frameIndex_Map = self.frameIndex_Maps[sys_ID]
        for animal_counter,animal_ID in enumerate(frameIndex_Map.keys()): 
            ANIMAL = self.analysis_ANIMAL(sys_ID,animal_ID)
            animal_Store.append(ANIMAL) 
        #************************#
        # group-time-series-data #
        #************************#
        grouped_Data = []
        all_frames_List = []
        non_seg_frames_List = []
        vitelline_space_List = []
        pos_piv_tan_sp_time_series = []
        full_piv_tan_sp_time_series = []
        pos_apical_myo_sp_time_series = []
        full_apical_myo_sp_time_series = []
        myo_frames_after_transition = []
        myo_frames_before_transition = []
        mid_markers_after_transition = []
        mid_markers_before_transition = []
        seg_frames_after_transition_List = []
        seg_frames_before_transition_List = []
        for animan_counter,ANIMAL in enumerate(animal_Store):
            # frame-sequences 
            non_seg_frames_List.append(ANIMAL.frameIndex_List[0]-ANIMAL.initial_frame)
            seg_frames_before_transition_List.append(ANIMAL.transition_frame_indx-ANIMAL.frameIndex_List[0])
            seg_frames_after_transition_List.append(ANIMAL.frameIndex_List[-1]- ANIMAL.transition_frame_indx)
            all_frames_List.append(ANIMAL.frameIndex_List[0]-ANIMAL.initial_frame+len(ANIMAL.frameIndex_List))
            # vitelline-space
            vitelline_space_List.append(ANIMAL.vitelline_space)
            # piv-avg
            pos_piv_tan_sp_time_series.append(ANIMAL.pos_piv_avg)
            full_piv_tan_sp_time_series.append(ANIMAL.full_piv_avg)
            # apical-myo-avg
            pos_apical_myo_sp_time_series.append(ANIMAL.pos_apical_myo_avg)
            full_apical_myo_sp_time_series.append(ANIMAL.full_apical_myo_avg)
            # model-inputs
            animalData_List = [ANIMAL.mid_markers_List,ANIMAL.s_mic_List,ANIMAL.piv_tan_sign_mag_List,ANIMAL.piv_normal_List,ANIMAL.curv_List,ANIMAL.e_h_List,ANIMAL.apical_myo_List,ANIMAL.basal_myo_List] 
            # shift-reference-origin
            mid_markers_pix_List,s_mic_List,piv_tan_List,piv_norm_List,curv_List,e_h_List,apical_myo_List,basal_myo_List = [[numpy.roll(item,self.spatial_shift_by_node_index,axis=0) for item in items] for items in animalData_List]
            # close-epithelium
            mid_markers_pix_List,s_mic_List,piv_tan_List,piv_norm_List,curv_List,e_h_List,apical_myo_List,basal_myo_List = [[numpy.append(item,[item[0]],axis=0) for item in items] for items in [mid_markers_pix_List,s_mic_List,piv_tan_List,piv_norm_List,curv_List,e_h_List,apical_myo_List,basal_myo_List]]
            # mid-markers: after/before-transition
            mid_markers_after_transition.append(mid_markers_pix_List[seg_frames_before_transition_List[-1]:])
            mid_markers_before_transition.append(mid_markers_pix_List[:seg_frames_before_transition_List[-1]+1])
            # image-frames: after/before-transition
            myo_frames_after_transition.append(ANIMAL.myo_frame_List[seg_frames_before_transition_List[-1]:])
            myo_frames_before_transition.append(ANIMAL.myo_frame_List[:seg_frames_before_transition_List[-1]+1])
            # recalculate-arc-length
            s_pix_List = [numpy.insert(numpy.cumsum(numpy.sqrt(numpy.sum(numpy.diff(markers,axis = 0)**2,axis = 1))),0,1e-6) for markers in mid_markers_pix_List]
            s_mic_List,_,_ = inOutTools.unit_conversion_Length_inverseLength_Area(s_pix_List,[],[],self.pix_mic) # pix-to-mic-conversion
            # full-arc-length
            s_mic_ref_List = s_mic_List.copy() 
            # normalized-arc-length
            s_mic_List = [s/s[-1] for s in s_mic_ref_List] if self.normalized_epithelium else s_mic_List 
            # window-average-to-reduce-noise-in-input-data 
            grouped_Data.append(numpy.ma.array([inOutTools.sliding_window_average_data(item,self.window_avg_SIZE) for item in [s_mic_ref_List,s_mic_List,piv_tan_List,piv_norm_List,curv_List,e_h_List,apical_myo_List,basal_myo_List]]))
        #*****************
        # allign-animals #
        #****************#
        transition_frame_reference = max(seg_frames_before_transition_List)
        # piv-raw 
        frames_offSet_back_front = [[nsf_frame_indx,max(all_frames_List) - max_frame_indx] for nsf_frame_indx,max_frame_indx in zip(non_seg_frames_List,all_frames_List)]
        pos_piv_raw_List,indv_emb_piv_not_alligned,pos_apical_myo_raw_List,full_apical_myo_raw_List,vitelline_space_raw_List = [inOutTools.masked_data(item,array_shift=frames_offSet_back_front,matrix_shift=[]) for item in [pos_piv_tan_sp_time_series,full_piv_tan_sp_time_series,pos_apical_myo_sp_time_series,full_apical_myo_sp_time_series,vitelline_space_List]]
        # piv-alligned 
        frames_offSet_back_front = [[transition_frame_reference-sfbt_frame_indx,max(seg_frames_after_transition_List)-sfat_frame_indx] for sfbt_frame_indx,sfat_frame_indx in zip(seg_frames_before_transition_List,seg_frames_after_transition_List)]
        pos_piv_alligned_List,indv_emb_piv_alligned_List,pos_apical_myo_alligned_List,full_apical_myo_alligned_List,vitelline_space_alligned_List = [inOutTools.masked_data(item,array_shift=frames_offSet_back_front,matrix_shift=[]) for item in [pos_piv_tan_sp_time_series,full_piv_tan_sp_time_series,pos_apical_myo_sp_time_series,full_apical_myo_sp_time_series,vitelline_space_List]]
        # frames/markers-alligned
        emb_indx_with_max_seg_frames_before_transition, = numpy.where(numpy.array(seg_frames_before_transition_List)==transition_frame_reference)
        emb_indx_with_max_seg_frames_after_transition, = numpy.where(numpy.array(seg_frames_after_transition_List)==max(seg_frames_after_transition_List))
        myo_frames_alligned,mid_markers_alligned = [item_bf[emb_indx_with_max_seg_frames_before_transition[0]] + item_af[emb_indx_with_max_seg_frames_after_transition[0]] for item_bf,item_af in zip([myo_frames_before_transition,mid_markers_before_transition],[myo_frames_after_transition,mid_markers_after_transition])]
        #***************************************************************************#
        # orient-animal: left-right -> posterior-anterior (for-visual-purpose-only) #
        #***************************************************************************# 
        if self.spatial_allignment_anterior_posterior:
            animal_Store = [analysisModule.orient_animal(ANIMAL,self.crop_margin) for ANIMAL in animal_Store]
        #*******************#
        # initialize-system #
        #*******************#
        indv_emb_piv_not_alligned,indv_emb_piv_alligned_List,full_apical_myo_raw_List,full_apical_myo_alligned_List,pos_piv_raw_List,pos_piv_alligned_List,pos_apical_myo_raw_List,pos_apical_myo_alligned_List,vitelline_space_raw_List,vitelline_space_alligned_List = [[item] if numpy.array(item).ndim == 1 else item for item in [indv_emb_piv_not_alligned,indv_emb_piv_alligned_List,full_apical_myo_raw_List,full_apical_myo_alligned_List,pos_piv_raw_List,pos_piv_alligned_List,pos_apical_myo_raw_List,pos_apical_myo_alligned_List,vitelline_space_raw_List,vitelline_space_alligned_List]] 
        SYSTEM = System1D(sys_ID,self.inOut_path+'/movies',animal_Store,indv_emb_piv_not_alligned,indv_emb_piv_alligned_List,full_apical_myo_raw_List,full_apical_myo_alligned_List,pos_piv_raw_List,pos_piv_alligned_List,pos_apical_myo_raw_List,pos_apical_myo_alligned_List,vitelline_space_raw_List,vitelline_space_alligned_List,seg_frames_before_transition_List,transition_frame_reference,self.spatial_shift_by_node_index,self.normalized_epithelium,self.time_between_frames,self.pix_mic,self.sec_min) 
        # animal-allignment 
        time_series_data_animal = numpy.ma.array([numpy.ma.array([ inOutTools.masked_data(item,array_shift=[[0,0] for _ in range(len(item))],matrix_shift=frames_offSet_back_front[indx]) if item.shape[0] > 1 else [inOutTools.masked_data(item,array_shift=[[0,0] for _ in range(len(item))],matrix_shift=frames_offSet_back_front[indx])] for item in inputData_GROUPED]) for indx,inputData_GROUPED in enumerate(grouped_Data)]) 
        # animal-averaging-of-time-series-data 
        time_animalTypes_average_data = numpy.ma.swapaxes(numpy.ma.swapaxes(time_series_data_animal,1,2),0,1)
        # loop-over-time
        for time_counter,time_series_data in enumerate(time_animalTypes_average_data):
            s_List = []
            eh_List = []
            mom_List = []
            curv_List = []
            s_ref_List = []
            piv_tan_List = []
            eh_curv_List = []
            piv_norm_List = []
            total_myo_List = []
            basal_myo_List = []
            apical_myo_List = []
            curv_momGrad_List =[]
            piv_tanGrad_List = []
            mom_curvGrad_List = []
            total_myoGrad_List = []
            basal_myoGrad_List = []
            apical_myoGrad_List = []
            basal_mom_curvGrad_List = []
            apical_mom_curvGrad_List = []
            curv_basal_myoGrad_List = []
            curv_apical_myoGrad_List = []
            piv_tanGrad_correction_List = []
            piv_correction_factor_Grad_List = []
            # loop-over-animals
            for emb_counter,emb_series_data in enumerate(time_series_data): 
                s_ref,s,piv_tan,piv_norm,curv,e_h,apical_myo,basal_myo = emb_series_data 
                # myosin: raw 
                if self.normalize_myosin_intensity:
                    basal_myo = basal_myo/max(inOutTools.smooth_data(basal_myo)) # normalization
                    apical_myo = apical_myo/max(inOutTools.smooth_data(apical_myo)) # normalization
                total_myo = apical_myo + basal_myo      
                mom = 0.5*e_h*(apical_myo-basal_myo)
                basal_mom = 0.5*e_h*basal_myo
                apical_mom = 0.5*e_h*apical_myo
                # gradients: dT/ds,dc/ds,c*v_n 
                momGrad = inOutTools.gradients_of_data(s,mom,uniform_sampling=True,closed=True)
                curvGrad = inOutTools.gradients_of_data(s,curv,uniform_sampling=True,closed=True) 
                total_myoGrad = inOutTools.gradients_of_data(s,total_myo,uniform_sampling=True,closed=True)
                basal_myoGrad = inOutTools.gradients_of_data(s,basal_myo,uniform_sampling=True,closed=True)
                apical_myoGrad = inOutTools.gradients_of_data(s,apical_myo,uniform_sampling=True,closed=True)
                piv_correction_factor_Grad = inOutTools.gradients_of_data(s,curv*piv_norm,uniform_sampling=True,closed=True)
                piv_tanGrad = inOutTools.gradients_of_data(s,piv_tan,uniform_sampling=True,closed=True)/s_ref[-1] if self.normalized_epithelium else inOutTools.gradients_of_data(s,piv_tan,uniform_sampling=True,closed=True)
                # listing-measurements: individual-animal 
                s_List.append(s)
                eh_List.append(e_h)
                mom_List.append(mom)
                curv_List.append(curv)
                s_ref_List.append(s_ref)
                piv_tan_List.append(piv_tan)
                eh_curv_List.append(e_h*curv)
                piv_norm_List.append(piv_norm)
                total_myo_List.append(total_myo)
                basal_myo_List.append(basal_myo)
                apical_myo_List.append(apical_myo)
                piv_tanGrad_List.append(piv_tanGrad)
                mom_curvGrad_List.append(mom*curvGrad)
                curv_momGrad_List.append(curv*momGrad) 
                total_myoGrad_List.append(total_myoGrad) 
                basal_myoGrad_List.append(basal_myoGrad)
                apical_myoGrad_List.append(apical_myoGrad)
                basal_mom_curvGrad_List.append(basal_mom*curvGrad)
                curv_basal_myoGrad_List.append(curv*basal_myoGrad)
                apical_mom_curvGrad_List.append(apical_mom*curvGrad)
                curv_apical_myoGrad_List.append(curv*apical_myoGrad)
                piv_tanGrad_correction_List.append(piv_tanGrad+curv*piv_norm)
                piv_correction_factor_Grad_List.append(piv_correction_factor_Grad)
            # average-over-animal 
            time_val = time_counter*self.time_between_frames
            measurables_List = [s_ref_List,s_List,eh_List,eh_curv_List,mom_List,curv_List,total_myo_List,apical_myo_List,basal_myo_List,piv_tan_List,piv_tanGrad_List,piv_tanGrad_correction_List,piv_norm_List,apical_mom_curvGrad_List,curv_apical_myoGrad_List,basal_mom_curvGrad_List,curv_basal_myoGrad_List,mom_curvGrad_List,curv_momGrad_List,total_myoGrad_List,apical_myoGrad_List,basal_myoGrad_List,piv_correction_factor_Grad_List]
            measurables_avg,measurables_std = inOutTools.calculate_masked_avg_std(measurables_List)
            s_ref_avg,s_avg,eh_avg,eh_curv_avg,mom_avg,curv_avg,total_myo_avg,apical_myo_avg,basal_myo_avg,piv_tan_avg,piv_tanGrad_avg,piv_tanGrad_correction_avg,piv_norm_avg,apical_mom_curvGrad_avg,curv_apical_myoGrad_avg,basal_mom_curvGrad_avg,curv_basal_myoGrad_avg,mom_curvGrad_avg,curv_momGrad_avg,total_myoGrad_avg,apical_myoGrad_avg,basal_myoGrad_avg,piv_correction_factor_Grad_avg = measurables_avg
            s_ref_std,s_std,eh_std,eh_curv_std,mom_std,curv_std,total_myo_std,apical_myo_std,basal_myo_std,piv_tan_std,piv_tanGrad_std,piv_tanGrad_correction_std,piv_norm_std,apical_mom_curvGrad_std,curv_apical_myoGrad_std,basal_mom_curvGrad_std,curv_basal_myoGrad_std,mom_curvGrad_std,curv_momGrad_std,total_myoGrad_std,apical_myoGrad_std,basal_myoGrad_std,piv_correction_factor_Grad_std = measurables_std         
            # update-genotype-individual-time-information 
            SYSTEM.update(time_val,s_avg,s_std,eh_avg,eh_std,eh_curv_avg,eh_curv_std,mom_avg,mom_std,curv_avg,curv_std,s_ref_avg,s_ref_std,piv_tan_avg,piv_tan_std,piv_tanGrad_avg,piv_tanGrad_std,piv_tanGrad_correction_avg,piv_tanGrad_correction_std,piv_norm_avg,piv_norm_std,total_myo_avg,total_myo_std,basal_myo_avg,basal_myo_std,apical_myo_avg,apical_myo_std,mom_curvGrad_avg,mom_curvGrad_std,curv_momGrad_avg,curv_momGrad_std,basal_myoGrad_avg,basal_myoGrad_std,total_myoGrad_avg,total_myoGrad_std,apical_myoGrad_avg,apical_myoGrad_std,basal_mom_curvGrad_avg,basal_mom_curvGrad_std,curv_basal_myoGrad_avg,curv_basal_myoGrad_std,apical_mom_curvGrad_avg,apical_mom_curvGrad_std,curv_apical_myoGrad_avg,curv_apical_myoGrad_std,piv_correction_factor_Grad_avg,piv_correction_factor_Grad_std,myo_frames_alligned[time_counter],mid_markers_alligned[time_counter])           
        
        return SYSTEM

