import os
import re
import sys
import cv2 
import csv
import glob
import copy
import numpy
import pickle
import platform
import warnings 
import skimage.exposure
from scipy.signal import gaussian
from scipy.integrate import simps
from inspect import currentframe
from shapely.affinity import scale
import matplotlib.pyplot as pyplot
import matplotlib.colors as mcolors
import matplotlib._color_data as mcd
from sklearn.decomposition import PCA
from skimage.measure import EllipseModel
from shapely.geometry  import Point,Polygon
from scipy.interpolate import interp1d,griddata
from scipy.signal import find_peaks

warnings.filterwarnings("ignore")

colorMaps = pyplot.colormaps()
advColor = list(mcd.CSS4_COLORS)
baseColor = list(mcolors.BASE_COLORS) 
colors = baseColor[:-2] + advColor[20:-1] 

def ellipse(ellipse_semi_a,ellipse_semi_b,numNode):
    theta = numpy.linspace(0,2.0*numpy.pi,numNode)
    theta = theta[:-1]
    points = numpy.array([[ellipse_semi_a*numpy.cos(theta),ellipse_semi_b*numpy.sin(theta)] for theta in theta])
    polygon = Polygon(points)
    if polygon.exterior.is_ccw:
        points = numpy.flip(points, axis = 0)
    points = numpy.reshape(points,(-1, 2))
    return points

def shift_position_of_a_point_along_polygon(markers,ds,indx):
    # create-a-marker-at-the-desired-position
    s,s_max = arc_length_along_polygon(markers)
    s_next = s[indx]+ds*s_max
    markers_closed = numpy.insert(markers,len(markers),markers[0],axis=0)
    markers_interpolator,_,s_closed = interpolate_Points_and_Measurables_OnCurve(markers_closed,[],normalized=False)
    s_next = s_next - s_closed[-1] if s_next > s_closed[-1] else s_next
    markers_point_to_interpolate = markers_interpolator(s_next)
    # register-the-newly-created-marker: increases-total-number-of-marker-by-one
    markers = numpy.insert(markers,0,markers_point_to_interpolate,axis=0)
    markers = orient_polygon(markers,orientation_reference_indx=0,clockwise=True)   
    # uniformy-distribute-the-markers: reduce-total-number-of-makers-by-one (restore-defaut-configuration)
    markers,_ = uniform_distribution_along_polygon(markers,len(markers),closed=True)
    return markers

def set_ellipse_origin_on_semi_minor_axis(ellipse_semi_a,ellipse_semi_b,ellipse):
    axis_scale_factor = ellipse_semi_a + ellipse_semi_b
    ellipse_centre = numpy.array(Polygon(ellipse).centroid.coords).flatten()
    axis_orientation = normalize([-1.0*ellipse_semi_a,ellipse_centre[0]]-ellipse_centre)
    return [axis_scale_factor,axis_orientation]
    
def shift_origin_of_polygon_contour(polygon,arc_length_value_to_shift,shift_ref_axis_length,shift_ref_axis_orientation):
    polygon_centre = numpy.array(Polygon(polygon).centroid.coords).flatten()
    mid_origin_intersetion_axis = numpy.array([polygon_centre+2*(shift_ref_axis_length)*shift_ref_axis_orientation,polygon_centre])
    # reference-coordinate-origin 
    polygon,_ = uniform_distribution_along_polygon(polygon,len(polygon)+1,closed=True)
    polygon,mid_marker_parameters = reset_starting_point_of_polygon(polygon,mid_origin_intersetion_axis)
    polygon,_ = uniform_distribution_along_polygon(polygon,len(polygon),closed=True)
    # initial-myo-centre-to-curvature-peak-offSet 
    polygon_interpolator,_,_ = interpolate_Points_and_Measurables_OnCurve(polygon,[],normalized=True)
    initial_myo_position = polygon_interpolator(arc_length_value_to_shift+1e-6) 
    initial_myo_orientation = normalize(initial_myo_position-polygon_centre)
    myo_centre_intersetion_axis = numpy.array([polygon_centre+2*(shift_ref_axis_length)*initial_myo_orientation,polygon_centre])
    polygon,_ = reset_starting_point_of_polygon(polygon,myo_centre_intersetion_axis)  
    polygon,_ = uniform_distribution_along_polygon(polygon,len(polygon),closed=True)
    return polygon

def area_under_curve(x,y,closed):
    x_new = copy_DATA(x)
    y_new = copy_DATA(y)
    if closed:
        dx = x[-1] - x[-2]
        x_new = numpy.insert(x,[len(x)],[x[-1]+dx],axis=0)
        y_new = numpy.insert(y,[len(y)],[y[0]],axis=0)
    return simps(y_new,x_new)

def current_program_path():
    return os.getcwd() 

def operating_system():
    return platform.system()

def load_data_via_pickle(path):
    if os.path.exists(path):
        file_IN = open(path, 'rb')
        data = pickle.load(file_IN)
        file_IN.close()
        return data
    else:
        print('pickle file:',path,'does not exist !!')
        sys.exit()
        
def dump_data_via_pickle(path,data):
    file_OUT = open(path, 'wb')
    pickle.dump(data,file_OUT)
    file_OUT.close()
    return

def readImage(path,flag):
    if flag == 'color': 
        return cv2.imread(path,cv2.IMREAD_COLOR) # remove-transparency
    else:
        return cv2.imread(path,cv2.IMREAD_GRAYSCALE)

def interpolate_Points_and_Measurables_OnCurve(polygon,measurable,normalized):
    polygon = numpy.array(polygon)
    s_Values,_ = arc_length_along_polygon(polygon)
    if normalized:
        s_Values = s_Values/s_Values[-1]
    polygon_interpolator =  interp1d(s_Values, polygon,kind='linear', axis = 0)
    # measurable
    measurable_interpolator = None
    measurable = numpy.array(measurable)
    if measurable.size:
        measurable_interpolator =  interp1d(s_Values, measurable,kind='linear', axis = 0)
    return(polygon_interpolator,measurable_interpolator,s_Values)

def polygon_from_image_contour(contours_List,noder_Number):
    xp,yp = contours_List  #[selectedContour].T
    contour_polygon = [list(a) for a in zip(xp.ravel(), yp.ravel())] 
    contour_polygon = numpy.reshape(contour_polygon,(-1, 2))
    contour_polygon,_ = uniform_distribution_along_polygon(contour_polygon,noder_Number,closed=False) # reduce-number-of-points
    polygon = Polygon(contour_polygon)
    if not polygon.exterior.is_ccw:# correct-orientation (clockwise)
        contour_polygon = numpy.flip(contour_polygon, axis = 0)
    return(contour_polygon)

def listdir_nohidden(path):
    return glob.glob(os.path.join(path,'*'))

def decomment(infile):
    for row in infile:
        row = row.replace(',', '_')
        raw = row.split('#')[0].strip()
        if raw: yield raw


def read_parameters_from_file(fileName):
    varibales_List = {}
    str_varibales_List = {}
    bool_varibales_List = {}
    with open(fileName) as infile:
        reader = csv.reader(decomment(infile))
        for row in reader:
            h,x =  row[0].split() 
            x = True if x == 'True' else False if x == 'False' else [float(ele) for ele in re.sub('[\[\]]','',x).split("_")]
            if isinstance(x, bool):
                bool_varibales_List[h] = x 
            else:
                str_varibales_List[h] = x[-1] if len(x) == 1 else x
        infile.close()
    parameters = {**varibales_List,**str_varibales_List,**bool_varibales_List}
    return parameters

def normalize(a):
    a = numpy.array(a)
    a_mag = numpy.linalg.norm(a)
    if a_mag == 0:
        a_mag = 1.0
    return a/a_mag

def get_tangents_pairs_along_polygon(points,closed):
    edge_pair_tangents_List = []
    numNode = len(points)
    for node_indx in range(0,numNode):
        node_indx_right = (node_indx+1)%(numNode) 
        node_indx_centre = (node_indx)%(numNode)
        node_indx_left = (node_indx-1)%(numNode)
        p_L = points[node_indx_left]
        p_C = points[node_indx_centre]
        p_R = points[node_indx_right]
        points_triplet = numpy.array([p_L,p_C,p_R])
        points_triplet = numpy.reshape(points_triplet,(-1, 2))
        edge_pair = numpy.diff(points_triplet, axis = 0)
        edge_pair_tangents_List.append([normalize(edg) for edg in edge_pair])
    if not closed:
        edge_tangent_start = normalize(points[1] - points[0])
        edge_pair_tangents_List[0] = [edge_tangent_start,edge_tangent_start] 
        edge_tangent_end = normalize(points[-1] - points[-2])
        edge_pair_tangents_List[-1] = [edge_tangent_end,edge_tangent_end]
    return(edge_pair_tangents_List)

def perpendicular_to(a):
    b = numpy.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def orient_polygon(polygon,orientation_reference_indx,clockwise):
    def clockwiseangle_and_distance(point,origin,refPoint):
        vector = numpy.array(point-origin)
        vector_mag = numpy.linalg.norm(vector)
        if vector_mag == 0:
            return numpy.pi,0
        vector_dir = normalize(vector)
        refvec_dir = normalize(refPoint-origin)
        dotprod  = vector_dir[0]*refvec_dir[0] + vector_dir[1]*refvec_dir[1]
        diffprod = refvec_dir[1]*vector_dir[0] - refvec_dir[0]*vector_dir[1]
        angle = numpy.arctan2(diffprod, dotprod)
        if angle < 0:
            return 2*numpy.pi+angle,vector_mag
        return angle,vector_mag
    polygon_centre = numpy.average(polygon,axis=0)
    polygon_oriented = numpy.array(sorted(polygon,key=lambda coord: clockwiseangle_and_distance(coord,polygon_centre,polygon[orientation_reference_indx])))
    if clockwise:
        return polygon_oriented
    else: 
        return numpy.roll(polygon_oriented[::-1], 1, axis=0)
    
def interpolate_vectors_around_point(vec_dir,vec_pos,ref_marker):
    interpolated_vector = [griddata(vec_pos,vec_comp,tuple(ref_marker),method='linear').tolist() for vec_comp in vec_dir]
    return interpolated_vector
    
def tangent_normals_along_polygon(points,closed):
    normals = []
    tangents = []
    edge_pair_tangents_List = get_tangents_pairs_along_polygon(points,closed)
    for edge_pair_tangents in edge_pair_tangents_List:
        edge_pair_normals = [perpendicular_to(edg) for edg in edge_pair_tangents]
        normal = 0.5*(edge_pair_normals[0]+edge_pair_normals[1])
        normal = normalize(normal)
        normals.append(normal)
        tangents.append(perpendicular_to(normal))
    tangents = -1.0*numpy.array(tangents)
    normals = numpy.array(normals)
    return(tangents,normals)

def principle_axes_to_polygon(ellipse_raw_markers):
    pca = PCA(n_components=2)
    pca.fit(ellipse_raw_markers) 
    principle_axis = numpy.array([pca.mean_ - vector * numpy.sqrt(length)  for length, vector in zip(pca.explained_variance_, pca.components_)])
    pca_axis_major,pca_axis_minor = principle_axis
    pca_axis_major = numpy.reshape([pca_axis_major,pca.mean_],(-1,2))
    pca_axis_minor = numpy.reshape([pca_axis_minor,pca.mean_],(-1,2))
    return pca.mean_,[pca_axis_major,pca_axis_minor]

def coordinate_frame_with_respect_to_polygon(polygon):
    polygon = numpy.array(polygon)
    interpol_polygon,_ = uniform_distribution_along_polygon(polygon,len(polygon),closed=False)
    PCA_centre,principle_axes = principle_axes_to_polygon(interpol_polygon) # symmetry-axes: PCA-based-estimation
    ellipse_markers,ellipse_centre,ellipse_semi_axes = ellipse_fit_to_polygon(interpol_polygon) # ellipse: least-square-fitting
    # merge-ellipse-fit/PCA-based-centers
    shift_centre = ellipse_centre - PCA_centre
    ellipse_markers = ellipse_markers - shift_centre
    ellipse_semi_axes = ellipse_semi_axes - shift_centre
    return PCA_centre,principle_axes,ellipse_markers,ellipse_semi_axes

def ellipse_fit_to_polygon(polygon):
    ellipse = EllipseModel()
    ellipse.estimate(polygon)
    ellipseFit_C_x, ellipseFit_C_y, semi_a, semi_b, theta_offset = ellipse.params
    theta = numpy.linspace(0,2*numpy.pi,len(polygon))
    xpos = semi_a*numpy.cos(theta)
    ypos = semi_b*numpy.sin(theta)
    # rotate-ellipse
    theta_offset *= -1.0 # clock-wise-orientation-of-ellipse
    new_xpos = xpos*numpy.cos(theta_offset)+ypos*numpy.sin(theta_offset)
    new_ypos = -xpos*numpy.sin(theta_offset)+ypos*numpy.cos(theta_offset)
    # traslate-ellipse
    new_xpos = ellipseFit_C_x + new_xpos
    new_ypos = ellipseFit_C_y + new_ypos
    ellipse_markers = numpy.column_stack([new_xpos,new_ypos])
    ellipse_markers = numpy.reshape(ellipse_markers,(-1,2))
    # semi_axis
    ellipse_centre = numpy.array([ellipseFit_C_x,ellipseFit_C_y])
    semi_b_axis_tip = numpy.array([0.0*numpy.cos(theta_offset)+semi_b*numpy.sin(theta_offset),- 0.0*numpy.sin(theta_offset)+semi_b*numpy.cos(theta_offset)])
    semi_a_axis_tip = numpy.array([semi_a*numpy.cos(theta_offset)+0.0*numpy.sin(theta_offset),-semi_a*numpy.sin(theta_offset)+0.0*numpy.cos(theta_offset)])
    semi_a_axis_tip = ellipse_centre + semi_a_axis_tip
    semi_b_axis_tip = ellipse_centre - semi_b_axis_tip
    semi_a_axis = numpy.reshape([semi_a_axis_tip,2*ellipse_centre - semi_a_axis_tip],(-1,2))
    semi_b_axis = numpy.reshape([semi_b_axis_tip,2*ellipse_centre - semi_b_axis_tip],(-1,2))
    return ellipse_markers,ellipse_centre,[semi_a_axis,semi_b_axis]

def detection_of_peak_pairs_in_defined_region(s,measurable,ROI,height,sorted_peaks):
    s_max_R,s_max_L = ROI
    # detect-peak
    peaks, properties = find_peaks(measurable,height=height)
    measurable_peak_indices = [indx for indx in peaks if (s[indx] > s_max_L) and (s[indx] < s_max_R)]
    measurable_peak_indices = numpy.array(measurable_peak_indices) 
    if sorted_peaks:
        measurable_peak_indices = measurable_peak_indices[numpy.argsort(measurable[measurable_peak_indices])]
    if measurable_peak_indices.size == 1:
        return numpy.array([measurable_peak_indices[0]]*2)
    return measurable_peak_indices[-2:]

def rectangular_function(s,step):
    fun = numpy.zeros_like(s)
    jump_start,jump_end = step
    if jump_start < jump_end:
        patch_indices = numpy.arange(jump_start,jump_end+1)
        fun[patch_indices] = 1.0
    return(fun)

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def delete_files_with_specific_extension(path,fileExtension):
    for images in os.listdir(path):
        if images.endswith(fileExtension):
            os.remove(os.path.join(path,images))
    return

def isFileExists(path):
    flag = os.path.isfile(path) 
    return(flag)

def deleteFile(fileName): 
    if isFileExists(fileName):
        os.remove(fileName)
        
def truncate_Data_Range(measurables,trunction_range):
    trunction_range = numpy.array(trunction_range)
    measurables_trunct = []
    for measurable in measurables:
        if trunction_range.size > 0:
            min_lim,max_lim = trunction_range
            measurables_trunct.append(measurable[numpy.arange(min_lim,max_lim+1)])
        else:
            measurables_trunct.append(measurable)
    return measurables_trunct

def get_min_max_of_Data(measurables):
    if len(measurables) > 1:
        return [[numpy.amin(item),numpy.amax(item)] for item in measurables]
    else:
        return [numpy.amin(measurables),numpy.amax(measurables)]

def adjustBrightnessImage(img,brightNessParam):
    return skimage.exposure.rescale_intensity(img,in_range=(0-brightNessParam,255-brightNessParam),out_range=(0,255)).astype('uint8')

def open_to_closed_polygon(polygon):
    polygon = numpy.array(polygon)
    return numpy.insert(polygon,[len(polygon)],[polygon[0]],axis=0)

def transparent_cmap(cmap,N = 255):
    mycmap = cmap
    mycmap._init()
    mycmap._lut[:,-1] = numpy.linspace(0, 0.99, N + 4)
    return mycmap

def point_at_which_quandrant(point):
    x,y = point
    if x > 0 and y > 0:
        return('Q-1')
    elif x < 0 and y > 0:
        return('Q-2')
    elif x < 0 and y < 0:
        return('Q-3')
    elif x > 0 and y < 0:
        return('Q-4')
    else:
        return None
    
def intersection_point_on_polygon_from_a_point(line_segments,u1,u2):
    v_out = None
    dist = None
    for ls in line_segments:
        flag,v_intrm,_ = intersection_of_two_LineSegments(u1,u2,ls[0],ls[1])
        if(flag == True):
            dist_vec = u1 - v_intrm
            dist_new = numpy.dot(dist_vec,dist_vec)
            if dist is None or dist_new < dist:
                dist = dist_new
                v_out = v_intrm
    return(v_out) 

def line_segments_along_polygon(markers):
    line_segments = [[markers[indx],markers[indx+1]] for indx in range(len(markers)-1)]
    line_segments.append([markers[-1],markers[0]])
    return line_segments 

def intersection_of_two_LineSegments(v1,v2,u1,u2):
    encounter = False
    u = [a_i - b_i for a_i, b_i in zip(u2,u1)] 
    v = [a_i - b_i for a_i, b_i in zip(v2,v1)] 
    w = [a_i - b_i for a_i, b_i in zip(u1,v1)] 
    s1 = (v[1]*w[0]-v[0]*w[1])/(v[0]*u[1]-v[1]*u[0]) 
    w = [a_i - b_i for a_i, b_i in zip(v1,u1)]
    s2 = (u[1]*w[0]-u[0]*w[1])/(u[0]*v[1]-u[1]*v[0])
    interSecPoint = None
    if(((s1 >= 0.0) and (s1 <= 1.0)) and ((s2 >= 0.0) and (s2 <= 1.0))):
        encounter = True
        interSecPoint = [u1[0]+s1*(u2[0]-u1[0]),u1[1]+s1*(u2[1]-u1[1])]  
    return(encounter,numpy.array(interSecPoint),[s1,s2])

def reset_starting_point_of_polygon(polygon_markers,intersetion_axis):
    polygon_markers = numpy.reshape(polygon_markers,(-1,2))
    inner_line_segments = line_segments_along_polygon(polygon_markers)
    v_ref = None
    flag = False
    indx_ref = None
    for indx,ls in enumerate(inner_line_segments):
        flag,v,_ = intersection_of_two_LineSegments(intersetion_axis[0],intersetion_axis[1],ls[0],ls[1])
        if flag:
            v_ref = v
            indx_ref = indx
            polygon_markers = numpy.insert(polygon_markers, indx+1, v_ref, axis=0)
            polygon_markers = numpy.roll(polygon_markers, -(indx+1), axis = 0)
            break
    if not flag:
        print('no intersection for starting arc-length reference')
    return(polygon_markers,[v_ref,indx_ref])

def nearest_point_on_line_segment_from_a_point(p,line):
    out_point = None
    p = numpy.array(p,float)
    p1 = numpy.array(line[0],float)
    p2 = numpy.array(line[1],float)
    u = p1 - p
    v = p2 - p1
    t = - numpy.dot(v,u)/numpy.dot(v,v)
    if t > 0.0 and t < 1.0:
        out_point = p1 + t*(p2 - p1)
    else:
        res = []
        for tval in [0.0,1.0]:
            res.append(tval*tval*numpy.sqrt(numpy.dot(v,v)) + 2.0*tval*numpy.dot(v,u) + numpy.dot(u,u))
        if res[0] < res[1]:
            out_point = copy_DATA(p1)
        else:
            out_point = copy_DATA(p2)
    return(out_point)

def arc_length_along_polygon(points):
    d_cumsum  = numpy.cumsum(numpy.sqrt(numpy.sum(numpy.diff(points,axis = 0)**2,axis = 1)))
    s  = numpy.insert(d_cumsum,0,1e-6)
    return s,s[-1]

def terminate():
    sys.exit()

def rotateImage(img,rotation_angle):
    (h, w) = img.shape[:2]# img-dim
    (cX, cY) = (w//2,h//2)# img-centre
    if abs(rotation_angle) > 0.0:# rotate-img
        M = cv2.getRotationMatrix2D((cX, cY), -rotation_angle, 1.0)
        cos = numpy.abs(M[0, 0])
        sin = numpy.abs(M[0, 1])
        nW = int((h*sin)+(w*cos))
        nH = int((h*cos)+(w*sin))
        M[0, 2] += (nW/2)-cX
        M[1, 2] += (nH/2)-cY
        return cv2.warpAffine(img,M,(nW,nH))
    else:
        return img

def flipImage(img,flipMode):
    img = cv2.flip(img, 0) if flipMode == 'H' else cv2.flip(img, 1) if flipMode == 'V' else img
    return img

def flipPointsOnImage(img,points,flipMode):
    height,width,_ = img.shape
    points = numpy.array([[width-p[0]-1,p[-1]] for p in points]) if flipMode == 'V' else numpy.array([[p[0],height-p[-1]-1] for p in points]) if flipMode == 'H' else points
    return points
    
def rotatePointsOnImage(img,points,rotation_angle):
    (h, w) = img.shape[:2]# img-dim
    (cX, cY) = (w//2,h//2)# img-centre
    if abs(rotation_angle) > 0.0:# rotate-img
        M = cv2.getRotationMatrix2D((cX, cY), -rotation_angle, 1.0)
        cos = numpy.abs(M[0, 0])
        sin = numpy.abs(M[0, 1])
        nW = int((h*sin)+(w*cos))
        nH = int((h*cos)+(w*sin))
        M[0, 2] += (nW/2)-cX
        M[1, 2] += (nH/2)-cY
        # points
        points = numpy.array(points)
        points = numpy.hstack([points,numpy.ones(shape=(len(points), 1))])
        points = M.dot(points.T).T
    return points

def angle_between(v1, v2):
    cosang  = v1[0]*v2[0] + v1[1]*v2[1] 
    sinang = v1[0]*v2[1] - v1[1]*v2[0] 
    return numpy.arctan2(sinang,cosang)*180/numpy.pi 

def angle_between_in_degree(v1,v2):
    v1 = normalize(v1)
    v2 = normalize(v2)
    angle = numpy.arccos(numpy.dot(v1,v2))*180/numpy.pi
    return angle
    
def error(flag,line_number,message):
    if flag:
        print('line number:',line_number,',',message)
        terminate()
        
def uniform_distribution_along_polygon(polygon,numPoints,closed):
    polygon = numpy.array(polygon)
    if closed:
        polygon = numpy.append(polygon, [polygon[0]], axis = 0)
    interpol_polygon = numpy.reshape(polygon,(-1, 2))
    s_Values,_  = arc_length_along_polygon(interpol_polygon)
    polygon_interpolator =  interp1d(s_Values, interpol_polygon, kind='linear', axis = 0)
    which_s_Values = numpy.linspace(1e-6,s_Values[-1],numPoints)
    polygon = polygon_interpolator(which_s_Values)
    if closed:
        polygon = numpy.delete(polygon,-1, axis = 0)
        which_s_Values = numpy.delete(which_s_Values,-1, axis = 0)
    return polygon,which_s_Values

def nearest_point_on_contour_from_external_point(polygon,v_in):
    line_segments = line_segments_along_polygon(polygon)
    p_target = None
    dist = None
    for ls in line_segments:
        p_out = nearest_point_on_line_segment_from_a_point(v_in,ls) 
        if not p_out is None:
            dist_vec = v_in - p_out
            dist_new = numpy.dot(dist_vec,dist_vec)
            if dist is None or dist_new < dist:
                dist = dist_new
                p_target = p_out  
    return(p_target) 

def midline_polygon_from_a_pair_of_ploygons(outer_markers,inner_markers,start_point_intersetion_axis,equal_apical_basal_distance):
    # inner/outer-markers-and-line-segments 
    outer_markers = numpy.array(outer_markers)
    inner_markers = numpy.array(inner_markers)
    # generate-midline-markers 
    mid_markers = []
    # loop-through-the-outer-markers
    for indx,outer_marker in enumerate(outer_markers):
        dist = None
        inner_marker = None
        # coresponding-to-each-outer-marker: find-the-nearest-marker-on-the-inner-contour
        for inner_line_segment in line_segments_along_polygon(inner_markers):
            raw_inner_marker = nearest_point_on_line_segment_from_a_point(outer_marker,inner_line_segment) 
            if not raw_inner_marker is None:
                dist_vec = outer_marker - raw_inner_marker
                dist_new = numpy.dot(dist_vec,dist_vec)
                if dist is None or dist_new < dist:
                    dist = dist_new
                    inner_marker = raw_inner_marker           
        if inner_marker is None: 
            print("No closest point found for point!",indx)
        else:
            # mid-marker: average-of-outer-marker-and-inner-marker
            mid_markers.append(0.5*(outer_marker+inner_marker))      
    mid_markers  = numpy.array(mid_markers)
    # reset-origin-of-midline-markers: intersection-o-given-vextor-with-the-midline-contour 
    if numpy.array(start_point_intersetion_axis).size:
        mid_markers,_ = reset_starting_point_of_polygon(mid_markers,start_point_intersetion_axis)
    # uniform-distribution-of-mid-markers 
    mid_markers,s = uniform_distribution_along_polygon(mid_markers,len(mid_markers),closed=True)
    # corresponding-to-uniformly-distributes-midline-markers: redefine-outer/inner-markers 
    outer_markers = numpy.array([nearest_point_on_contour_from_external_point(outer_markers,mid_marker) for mid_marker in mid_markers])
    inner_markers = numpy.array([nearest_point_on_contour_from_external_point(inner_markers,mid_marker) for mid_marker in mid_markers])
    # distance-from-mid-marker: to-inner/outer-marker-should-be-eaual 
    if equal_apical_basal_distance:
        for indx,(outer,mid,iner) in enumerate(zip(outer_markers,mid_markers,inner_markers)):
            lateral_edge_markers,_ = uniform_distribution_along_polygon([outer,mid,iner],3,closed=False)
            outer_markers[indx],mid_markers[indx],inner_markers[indx] = lateral_edge_markers
    # arc-length-of-mid-line 
    s,_ = arc_length_along_polygon(mid_markers)
    return(s,mid_markers,outer_markers,inner_markers)

def copy_DATA(MEASURABLE):
    copied_MEASURABLE = copy.deepcopy(MEASURABLE)
    return copied_MEASURABLE

def distance_between_pair_of_polygons(outer_markers,inner_markers):
        distance_edges = outer_markers - inner_markers
        distance_vaues = []
        for edges in distance_edges:
            distance_vaues.append(numpy.linalg.norm(edges))
        return numpy.mean(distance_vaues),numpy.array(distance_vaues)
    
def nearest_distance_and_direction_to_one_polygon_from_another_polygon(markers,markers_ref,direction='outer'): 
    nearest_markers = numpy.array([nearest_point_on_contour_from_external_point(markers_ref,marker) for marker in markers])
    normDist = [numpy.linalg.norm(nearest_marker-marker) for nearest_marker,marker in zip(nearest_markers,markers)]
    normal_dir = None
    if direction=='outer': 
        normal_dir = [-1.0*normalize(nearest_marker-marker) for nearest_marker,marker in zip(nearest_markers,markers)]
    else:
        normal_dir = [normalize(nearest_marker-marker) for nearest_marker,marker in zip(nearest_markers,markers)]
    return normDist,normal_dir 


def scaled_polygon(polygon,scaleFact):
    polygon = scale(Polygon(polygon),xfact=scaleFact,yfact=scaleFact)
    return numpy.reshape(polygon.exterior.coords,(-1,2))

def points_inside_polygon(points,polygon):
    points_inside = []
    polygon = scaled_polygon(polygon,scaleFact=1.0)
    for p in points:
        point = Point(p[0],p[1])
        polygon = Polygon(polygon)
        if polygon.contains(point):
            points_inside.append(p)
    return numpy.reshape(points_inside,(-1,2))


def points_outside_polygon(points,polygon):
    points_inside = []
    polygon = scaled_polygon(polygon,scaleFact=1.0)
    for p in points:
        point = Point(p[0],p[1])
        polygon = Polygon(polygon)
        if not polygon.contains(point):
            points_inside.append(p)
    return numpy.reshape(points_inside,(-1,2))

def points_within_pair_of_polygons(points,polygon_out,polygon_in):
    polygon_out,polygon_in = [numpy.array(polygon) for polygon in [polygon_out,polygon_in]]
    points = points_inside_polygon(points,polygon_out)
    if polygon_in.size > 0:
        points = points_outside_polygon(points,polygon_in)
    return numpy.reshape(points,(-1,2))

def uniform_points_within_rectangle(window_center,width_height,numPoint):
    window_width,window_height = width_height
    window_center_x,window_center_y = window_center
    numPoint = int(numpy.sqrt(numPoint))
    return numpy.array(numpy.meshgrid(numpy.linspace(window_center_x-window_width,window_center_x+window_width,numPoint),numpy.linspace(window_center_y-window_height,window_center_y+window_height,numPoint))).T.reshape(-1, 2)

def gradients_of_data_2D(points,measurable,closed):  
    if closed:
        points = numpy.insert(points,[0,len(points)],[points[-1],points[0]],axis=0) 
        s,_ =  arc_length_along_polygon(points)
        measurable = numpy.insert(measurable,[0,len(measurable)],[measurable[-1],measurable[0]],axis=0)
        measurable_grad = numpy.gradient(measurable,s)
        measurable_grad = measurable_grad[1:-1]
        return(measurable_grad)
    else:
        s,_ = arc_length_along_polygon(points)
        measurable_grad = numpy.gradient(measurable,s)
        return measurable_grad
    
def curvature_along_polygon(points,closed):
    points = numpy.array(points)
    x = points[:,0]
    y = points[:,1]
    x_grad = gradients_of_data_2D(points,x,closed)
    x_double_grad = gradients_of_data_2D(points,x_grad,closed)
    y_grad = gradients_of_data_2D(points,y,closed)
    y_double_grad = gradients_of_data_2D(points,y_grad,closed)
    nominator = (y_double_grad*x_grad-x_double_grad*y_grad)
    denominator = (x_grad*x_grad+y_grad*y_grad)**(3/2)
    curvature = nominator/denominator
    # curvature: > 0 if-tangent-vector-turns-counterclockwise
    if not Polygon(points).exterior.is_ccw:
        curvature = -1.0*curvature 
    return curvature

def unit_conversion_Length_inverseLength_Area(lengths,inv_lengths,areas,conversion_factor):
    lengths_converted = [ele*conversion_factor for ele in lengths]# lengths
    inv_lengths_converted = [ele/conversion_factor for ele in inv_lengths]# lengths
    areas_converted = [area*conversion_factor*conversion_factor for area in areas]# areas
    return(lengths_converted,inv_lengths_converted,areas_converted)

def sliding_window_average_data(measurables,window_SIZE):
    measurables = numpy.ma.array(measurables)
    if len(measurables.shape) == 1:
        measurables = numpy.reshape(measurables, (-1, 1))
    # masking
    measurables_masked = []
    for item in measurables:
        item_masked = numpy.ma.array(item,mask = True)
        item_masked[:] = item
        measurables_masked.append(item_masked)
    # managing-boundary
    empty_measurables = numpy.ma.empty(measurables.shape[1])
    empty_measurables.mask = True
    measurables_masked  = [empty_measurables]*window_SIZE + measurables_masked + [empty_measurables]*window_SIZE
    # average
    measurables_window_avg = []
    for indx,item in enumerate(measurables): 
        item_avg_List = measurables_masked[indx:indx+2*window_SIZE+1]
        measurables_window_avg.append(numpy.ma.mean(item_avg_List, axis = 0))
    measurables_window_avg = numpy.ma.array(measurables_window_avg)
    # 1D-array 
    if measurables_window_avg.shape[1] == 1:
        measurables_window_avg  = measurables_window_avg.flatten()
    return measurables_window_avg

def masked_data(measurables,array_shift,matrix_shift):
    measurables = numpy.ma.array(measurables)
    # masking-individual-arrays 
    if array_shift:
        measurables_masked = []
        for m,a_s in zip(measurables,array_shift):
            array_shift_front,array_shift_back = a_s
            empty_m = numpy.ma.empty(1)
            empty_m.mask = True
            empty_m_List = numpy.tile(empty_m,array_shift_front)
            m = numpy.ma.hstack((empty_m_List,m))
            empty_m_List = numpy.tile(empty_m,array_shift_back)
            m = numpy.ma.hstack((m,empty_m_List))
            measurables_masked.append(m)
        measurables = numpy.ma.array(measurables_masked)
    # masking-whole-matirx 
    if matrix_shift:
        measurables_shift_front,measurables_shift_back = matrix_shift
        empty_measurables = numpy.ma.empty(max([len(m) for m in measurables]))
        empty_measurables.mask = True
        empty_measurables_List = numpy.tile(empty_measurables,(measurables_shift_front,1))
        measurables = numpy.ma.vstack((empty_measurables_List,measurables))
        empty_measurables_List = numpy.tile(empty_measurables,(measurables_shift_back,1))
        measurables = numpy.ma.vstack((measurables,empty_measurables_List)) 
    # distinguish-between-1D/2D-arrays 
    measurables_num,_ = measurables.shape
    measurables= measurables[-1] if measurables_num == 1 else measurables
    return measurables

def smooth_data(measurable):
    numNode = len(measurable)
    smoothing_sigma = numNode/50
    smoothing_window = gaussian(numNode,smoothing_sigma)
    smoothing_window = smoothing_window/smoothing_window.sum()
    measurable_extended = list(measurable)
    measurable_extended[0:0] = measurable # copy-in-front
    measurable_extended[len(measurable_extended):len(measurable_extended)] = measurable # copy-in-back
    measurable_extended = numpy.array(measurable_extended)
    measurable_extended = numpy.convolve(measurable_extended,smoothing_window,mode='same')
    # if-measurable-is-masked-array
    if numpy.ma.isMaskedArray(measurable):
        measurable_extended = numpy.ma.masked_invalid(measurable_extended)
    measurable_smoothed = measurable_extended[len(measurable):-len(measurable)] # remove-copies
    return(measurable_smoothed)

def gradients_of_data(s,measurable,uniform_sampling,closed):
    # for-no-arc-length-value: masked-array  
    if numpy.ma.is_masked(s) and s.mask.all():
        measurable_grad = numpy.ma.empty(len(measurable))
        measurable_grad.mask = True
        return measurable_grad
    # for-closed-arc-length 
    if closed:
        s = numpy.insert(s,[0,len(s)],[s[0]-(s[-1]-s[-2]),s[-1]+(s[1]-s[0])],axis=0)
        measurable = numpy.insert(measurable,[0,len(measurable)],[measurable[-2],measurable[1]],axis=0) # measurable = numpy.insert(measurable,[0,len(measurable)],[measurable[-1],measurable[0]],axis=0)
        if uniform_sampling:
            ds = numpy.average(s[1:]-s[:-1])
            measurable_grad = numpy.gradient(measurable,ds)
        else:
            measurable_grad = numpy.gradient(measurable,s)
        measurable_grad = measurable_grad[1:-1]
        return(measurable_grad)
    # for-open-x-axis 
    else:
        if uniform_sampling:
            ds = numpy.average(s[1:]-s[:-1])
            measurable_grad = numpy.gradient(measurable,ds)
        else:    
            measurable_grad = numpy.gradient(measurable,s)
        return measurable_grad
    
def calculate_masked_avg_std(measurables):
    measurables_avg = []
    measurables_std = []
    for measurable in measurables:
        measurables_avg.append(numpy.ma.mean(measurable,axis=0))
        measurables_std.append(numpy.ma.std(measurable,axis=0))
    return measurables_avg,measurables_std