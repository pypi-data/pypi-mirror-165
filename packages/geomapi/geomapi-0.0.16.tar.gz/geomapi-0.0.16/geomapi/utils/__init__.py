"""
General Basic functions to support other modules
"""

from distutils import extension
from doctest import testfile
from fileinput import filename
import os
import rdflib
from rdflib import XSD, Graph,URIRef,Literal
import re
import numpy as np
import ntpath
import datetime
import PIL.Image
from PIL.ExifTags import GPSTAGS, TAGS
from typing import List
from warnings import warn


#### GLOBAL VARIABLES ####

RDF_EXTENSIONS = [".ttl"]
IMG_EXTENSION = [".jpg", ".png", ".JPG", ".PNG", ".JPEG"]
MESH_EXTENSION = [".obj",".ply",".fbx" ]
PCD_EXTENSION = [".pcd", ".e57",".pts", ".ply", '.xml']
INT_ATTRIBUTES = ['pointCount','faceCount','e57Index'] #'label'
FLOAT_ATTRIBUTES = ['xResolution','yResolution','imageWidth','imageHeight','focalLength35mm','principalPointU','principalPointV','accuracy']
LIST_ATTRIBUTES =  ['distortionCoeficients']

exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
fog=rdflib.Namespace('https://w3id.org/fog#')
v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
e57=rdflib.Namespace('http://libe57.org#')
xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')

#### BASIC OPERATIONS ####

def get_extension(path:str) -> str:
    """Returns the filepath extensions.
    \n
    E.g. D://myData//test.txt -> .txt

    Args:
        path (str):

    Returns:
        str: 
    """
    filename,extension = os.path.splitext(path)
    return extension

def replace_str_index(text:str,index:int=0,replacement:str='_'):
    """Replace a string character at the location of the index with the replacement.
    \n

    replacement=_\n
    index=1\n
    text= 'text' -> t_xt\n

    Args:
        0. text (str)\n
        index (int, optional): _description_. Defaults to 0.
        replacement (str, optional): _description_. Defaults to '_'.

    Returns:
        _type_: _description_
    """
    return '%s%s%s'%(text[:index],replacement,text[index+1:])


def get_folder_path(path :str) -> str:
    """Returns the folderPath

    Raises:
        FileNotFoundError: If the given graphPath or sessionPath does not lead to a valid systempath

    Returns:
        str: The full systempath to its folder
    """
    folderPath= os.path.dirname(path)
    if not os.path.isdir(folderPath):
        print("The given path is not a valid folder on this system.")    
    return folderPath

def get_variables_in_class(cls) -> list: 
    """
    returns list of variables in the class
    """  
    return [i.strip('_') for i in cls.__dict__.keys() ] #if i[:1] != '_'

def get_list_of_files(directoryPath:str) -> list:
    """Get a list of all files in the directory and subdirectories (getListOfFiles)

    Args:
        directoryPath: directory path e.g. "D:\\Data\\2018-06 Werfopvolging Academiestraat Gent\\week 22\\"
            
    Returns:
        A list of files 
    """
    # names in the given directory 
    listOfFile = os.listdir(directoryPath)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(directoryPath, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)                
    return allFiles

def get_subject_graph(graph:Graph, subject:URIRef = None) -> Graph:
        """Subselects the full Graph to only contain 1 subject

        Args:
            graph (Graph, optional): 
            subject (URIRef, optional): If no subject is provided, the first one is picked. Defaults to None.
        """
        #input validation       
        if(subject and subject not in graph.subjects()): 
            raise ValueError('subject not in graph')
        elif (not subject): # No subject is defined yet, pick the first one
            subject=next(graph.subjects())        

        #create graph
        newGraph = Graph()
        newGraph += graph.triples((subject, None, None)) 
        newGraph._set_namespace_manager(graph._get_namespace_manager())

        #validate output
        if (len(newGraph) !=0):
            return newGraph
        else:
            return None

def get_paths_in_class(cls) -> list: 
    """
    returns list of paths in the class
    """  
    from re import search
    return [i.strip('_') for i in cls.__dict__.keys() if search('Path',i) or search('path',i)] 

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def filter_exif_gps_data(data, reference:str) -> float:
    if type(data) is float:
        if reference in ['S','W','s','w']:
            return data*-1
        else:
            return data
    elif type(data) is tuple and len(data) == 3:
        value=dms2dd(data[0],data[1],data[2],reference)
        return value     

def dms2dd(degrees:float, minutes:float, seconds:float, direction:str) -> float:
    """Convert world angles (degrees, minutes, seconds) to decimal degrees

    Args:
        degrees (float)
        minutes (float)
        seconds (float)
        direction (str): 'N' and 'E' are positive, 'W' and 'S' are negative 

    Returns:
        dd (float)
    """
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd

def dd2dms(deg):
    """Convert decimal degrees to (degrees, minutes, seconds) 

    Args:
        degrees (float)
        minutes (float)
        seconds (float)

    Returns:
        dms (float)
    """
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def parse_dms(dms):
    # parts = re.split('[^\d\w]+', dms)
    # lat = dms2dd(parts[0], parts[1], parts[2], parts[3])            
    # temp=str(dms)
    try:
        if type(dms) is np.ndarray and dms.size==4:
            return dms2dd(dms[0],dms[1],dms[2], dms[3] )
        elif type(dms) is tuple and len(dms)==4:
            return dms2dd(dms[0],dms[1],dms[2], dms[3] )
        elif type(dms) is str and 'None' not in dms:
            temp=validate_string(dms, ' ')
            temp=temp.replace("\n","")
            temp=temp.replace("\r","")
            temp=temp.split(' ')
            temp=[x for x in temp if x]
            if temp:
                res=np.asarray(temp) 
                return dms2dd(res[0],res[1],res[2], res[3] )
        return None  
    except:
        raise ValueError


def get_exif_data(img:PIL.Image):
    """Returns a dictionary from the exif data of an Image item. Also
    converts the GPS Tags
    
    Returns:
        bool: True if exif data is sucesfully parsed
    """
    exifData = {}
    info = img._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exifData[decoded] = gps_data
            else:
                exifData[decoded] = value        
        return exifData      
    else:
        return None        

def get_filename(path :str) -> str:
    """ Deconstruct path into filename"""
    path=ntpath.basename(path)
    head, tail = ntpath.split(path)
    array=tail.split('.')
    return array[0]

def get_folder(path :str) -> str:
    """ Deconstruct path and return forlder"""
    return os.path.dirname(os.path.realpath(path))

def get_timestamp(path : str) -> str:
    ctime=os.path.getctime(path)
    dtime=datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%dT%H:%M:%S')
    return dtime

#### CONVERSIONS ####

def literal_to_cartesianTransform(literal:Literal) -> np.array:
    temp=str(literal)
    try:
        if 'None' not in temp:
            temp=validate_string(temp, ' ')
            temp=temp.replace("\n","")
            temp=temp.replace("\r","")
            temp=temp.split(' ')
            temp=[x for x in temp if x]
            if temp:
                res = list(map(float, temp))   
                res=np.reshape(res,(4,4))
                return np.asarray(res)  
        return None  
    except:
        raise ValueError

def literal_to_array(literal: Literal) -> np.array:
    temp=str(literal)
    return np.asarray(string_to_list(temp))

def literal_to_orientedBounds(literal: Literal)-> np.array:
    """
    Convert URIRef to cartesian bounds

    Args:
        literal (URIRef):  
    Returns:
        np.array([8x3])   
    """   
    temp=str(literal)
    try:
        if 'None' not in temp:
            temp=validate_string(temp, ' ')
            temp=temp.replace("\n","")
            temp=temp.replace("\r","")
            temp=temp.split(' ')
            temp=[x for x in temp if x]
            if temp:
                res = list(map(float, temp))   
                res=np.reshape(res,(8,3))
                return np.asarray(res)  
        return None  
    except:
        raise ValueError

def literal_to_float(literal: Literal) -> float:
    try:
        if 'None' in literal:
            return None
        return float(literal.toPython())
    except:
        raise ValueError

def literal_to_string(literal: Literal)->str:
    string=str(literal)
    try:
        if 'None' in string:
            return None
        else:
            return string
    except:
        raise ValueError

def literal_to_list(literal: Literal)->list:
    string=str(literal)
    try:
        if 'None' in string:
            return None
        else: 
            return string_to_list(string)
    except:
        raise ValueError

def literal_to_int(literal: Literal) -> int:
    try:
        if 'None' in literal:
            return None
        return int(literal.toPython())
    except:
        raise ValueError

def literal_to_uriref(literal: Literal)->URIRef:
    # string=str(literal)
    try:
        temp=literal.toPython()
        if type(temp) is float or type(temp) is int:
            raise ValueError('float causes errors')
        elif 'None' not in literal:            
            return URIRef(literal.toPython())
        # if 'None' in string:
        #     return None
        # else:
        #     temp=validate_string(string, ' ')
        #     temp=temp.replace("\n","")
        #     temp=temp.split(' ')
        #     temp=[x for x in temp if x]
        #     if temp:
        #         return [URIRef(item) for item in temp]
            # for idx,element in enumerate(string):
            #     if element in "[' ]":
            #         string=replace_str_index(string,index=idx,replacement='$')
            # res=[]
            # itemList=list(string.split(","))
            # for item in itemList:      
            #     item=item.strip("$")
            #     res.append(URIRef(item))
            # return res
        return None
    except:
        raise ValueError

def check_if_subject_is_in_graph(graph:Graph,subject=URIRef) ->bool:
    testSubject=subject.split('/')[-1]
    for s in graph.subjects():
        graphSubject= s.split('/')[-1]
        if testSubject==graphSubject:
            return True
    return False

def get_graph_subject(graph:Graph,subject=URIRef) ->URIRef:
    testSubject=subject.split('/')[-1]
    for s in graph.subjects():
        graphSubject= s.split('/')[-1]
        if testSubject==graphSubject:
            return s
    raise ValueError ('subject not in graph.')

def literal_to_linked_subjects(string:str) -> list:
    temp=string.split(',')
    temp=[re.sub(r"[\[ \' \]]",'',s) for s in temp]
    return temp

def string_to_list(string:str)->list:
    """
    Convert string of items to a list of their respective types
    """
    try:
        if 'None' not in string:
            temp=validate_string(string, ' ')
            temp=temp.replace("\n","")
            temp=temp.replace("\r","")
            temp=temp.split(' ')
            temp=[x for x in temp if x]
            # res = list(map(float, temp))  
            if temp:
                res=[]
                for item in temp:      
                    if is_float(item): 
                        res.append(float(item))
                    elif is_int(item): 
                        res.append(int(item))
                    elif is_string(item): 
                        res.append(str(item))
                    elif is_uriref(item): 
                        res.append(URIRef(item)) 
                return res
        return None  
    except:
        raise ValueError
    # for idx,element in enumerate(string):
    #     if element in "[!@#$%^&*()+?_ =<>]'":
    #         string=replace_str_index(string,index=idx,replacement='$')
    # res=[]
    # itemList=list(string.split(","))
    # for item in itemList:      
    #     item=item.strip("$")    
    #     if is_float(item): 
    #         res.append(float(item))
    #     elif is_int(item): 
    #         res.append(int(item))
    #     elif is_string(item): 
    #         res.append(str(item))
    #     elif is_uriref(item): 
    #         res.append(URIRef(item))
    # return res

def string_to_rotation_matrix(string :str) -> np.array:
    array=np.asarray(string_to_list(string))
    if array.size==9:
        return np.reshape(array,(3,3))
    else:
        raise ValueError('array.size!=9')

    # list=matrixString.split(' ')
    # rotationMatrix=np.array([[float(list[0]),float(list[1]),float(list[2]),0],
    #                          [float(list[3]),float(list[4]),float(list[5]),0],
    #                          [float(list[6]),float(list[7]),float(list[8]),0],
    #                          [0,0,0,1]])
    # return rotationMatrix

# def string_to_array(string : str)-> np.array:
#     list=string.split(' ')
#     floatlist=[]
#     for x in list:
#         floatlist.append(float(x))
#     return np.array(floatlist)

def xml_to_float(xml) -> float:
    if xml is None:
        return None
    else:
        return float(xml)

def xcr_to_lat(xcr:str) -> float:
    if 'None' in xcr:
        return None
    else:
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        if 'N' in list[-1]:
            return float(list[0])
        elif 'S' in list[-1]:
            return - float(list[0])

def xcr_to_long(xcr:str) -> float:
    if 'None' in xcr:
        return None
    else:        
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        if 'E' in list[-1]:
            return float(list[0])
        elif 'W' in list[-1]:
            return - float(list[0])

def xcr_to_alt(xcr:str) -> float:
    if 'None' in xcr:
        return None
    else:
        list=list=re.findall(r'[A-Za-z]+|\d+(?:\.\d+)?', xcr)
        if list:
            return float(list[0])/float(list[-1])       

def cartesianTransform_to_literal(matrix : np.array) -> str:
    """ convert nparray [4x4] to str([16x1])"""
    if matrix.size == 16: 
        return str(matrix.reshape(16,1))
    else:
        Exception("wrong array size!")    

def featured3d_to_literal(value) -> str:
    "No feature implementation yet"

def featured2d_to_literal(value) -> str:
    "No feature implementation yet"

def item_to_list(item):
    if type(item) is np.ndarray:
        item=item.flatten()
        return item.tolist()
    elif type(item) is np.array:
        item=item.flatten()
        return item.tolist()
    elif type(item) is list:
        return item
    else:
        return [item]

#### VALIDATION ####

def check_if_uri_exists(list:List[URIRef], subject:URIRef) ->bool:
    list=item_to_list(list)
    list=[item.toPython() for item in list]
    subject=subject.toPython()
      
    if any(subject in s for s in list):
        return True
    else: 
        return False

    # subjects=[]
    # for subject in list:
    #     path=subject.toPython()
    #     path = os.path.normpath(path) # this split doesn't do anything
    #     path=path.split(os.sep)
    #     subjects.append(path[-1])

    # path=subject.toPython()
    # path = os.path.normpath(path)
    # path=path.split(os.sep)
    # path=path[-1]
   
    # if any(path in s for s in subjects):
    #     return True
    # else: 
    #     return False
def get_subject_name(subject:URIRef) -> str:
    """Get the main body of a URIRef graph subject

    Args:
        subject (URIRef)

    Returns:
        str
    """
    string=subject.toPython()
    return string.split('/')[-1]   

def validate_string(string:str, replacement ='_') -> str:
    """Checks path validity. If not valid, The function adjusts path naming to be Windows compatible

    Args:
        path (str): _description_

    Returns:
        str: _description_
    """
    prefix=''
    if 'file:///' in string:
        string=string.replace('file:///','')
        prefix='file:///'
    elif 'http://' in string:
        string=string.replace('http://','')
        prefix='http://'
    for idx,element in enumerate(string):
        if element in "()^[^<>{}[] ~`],|*$ /\:": #
            string=replace_str_index(string,index=idx,replacement=replacement)
    string=prefix+string
    return string

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def is_int(element) -> bool:
    try:
        int(element)
        return True
    except ValueError:
        return False

def is_string(element) -> bool:
    #special_characters = "[!@#$%^&*()-+?_= ,<>/]'"
    try:
        str(element)
        return True
    except ValueError:
        return False

def is_uriref(element) -> bool:
    try:
        if type(element) is float:
            return False
        else:
            URIRef(element)
            return True
    except ValueError:
        return False

# #### RDF ####

def get_attribute_from_predicate(graph: Graph, predicate : Literal) -> str:
    """Returns the attribute witout the namespace

    Args:
        graph (Graph): The Graph containing the namespaces
        predicate (Literal): The Literal to convert

    Returns:
        str: The attribute name
    """
    predStr = str(predicate)
    #Get all the namespaces in the graph
    for nameSpace in graph.namespaces():
        nameSpaceStr = str(nameSpace[1])
        if(predStr.__contains__(nameSpaceStr)):
            predStr = predStr.replace(nameSpaceStr, '')
            break
    return predStr

def bind_ontologies(graph : Graph) -> Graph:
    """
    Bind additional ontologies that aren't in rdflib
    """
    exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
    graph.bind('exif', exif)
    geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
    graph.bind('geo', geo)
    gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
    graph.bind('gom', gom)
    omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
    graph.bind('omg', omg)
    fog=rdflib.Namespace('https://w3id.org/fog#')
    graph.bind('fog', fog)
    v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
    graph.bind('v4d', v4d)
    v4d3D=rdflib.Namespace('https://w3id.org/v4d/3D#')
    graph.bind('v4d3D', v4d3D)
    openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
    graph.bind('openlabel', openlabel)
    e57=rdflib.Namespace('http://libe57.org#')
    graph.bind('e57', e57)
    xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    graph.bind('xcr', xcr)
    ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')
    graph.bind('ifc', ifc)
    return graph

def clean_attributes_list(list:list) -> list:
    #NODE
    excludedList=['graph','graphPath','subject','resource','fullResourcePath','kwargs', 'orientedBoundingBox','type']
    #BIMNODE    
    excludedList.extend(['ifcElement'])
    #MESHNODE
    excludedList.extend(['mesh'])
    #IMGNODE
    excludedList.extend(['exifData','xmlData','image','features2d','pinholeCamera'])
    #PCDNODE
    excludedList.extend(['pcd','e57Pointcloud','e57xmlNode','e57image','features3d'])
    #SESSIONNODE
    excludedList.extend(['linkedNodes'])

    cleanedList = [ elem for elem in list if elem not in excludedList]
    return cleanedList

def check_if_path_is_valid(path:str)-> bool:
    folder=get_folder(path)
    if os.path.isdir(path):
        return True
    elif os.path.exists(folder):
        return True
    else:
        return False

def validate_timestamp(value) -> datetime:
    """Format value as datetime ("%Y-%m-%dT%H:%M:%S")

    Args:
        1.value ('Tue Dec  7 09:38:13 2021')
        2.value ("1648468136.033126")
        3.value ("2022:03:13 13:55:30")
        4.value (datetime)
        5.value ("2022-03-13 13:55:30")

    Raises:
        ValueError: 'timestamp formatting ("%Y-%m-%dT%H:%M:%S") failed for tuple, datetime and string formats. '

    Returns:
        datetime
    """
    string=str(value)
  
    try:
        return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S") 
    except:
        pass
    try:         
        test=datetime.datetime.strptime(string, "%Y:%m:%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S") 
        return test
    except:
        pass
    try:         
        test=datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S") 
        return test
    except:
        pass
    try:         
        test=datetime.datetime.strptime(string, "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%dT%H:%M:%S") 
        return test
    except:
        pass
    try:
        return datetime.datetime.fromtimestamp(float(string)).strftime('%Y-%m-%dT%H:%M:%S')
    except:
        raise ValueError('no valid time formatting found e.g. 1.value (Tue Dec  7 09:38:13 2021) 2.value (1648468136.033126) 3.value (2022:03:13 13:55:30)')

def get_node_resource_extensions(objectType:str) -> list:
    """Return potential file formats for different types of node resources (images, pcd, ortho, etc.)

    Args:
        objectType (str): Type of node class

    Returns:
        list with possible extensions
    """    
    if 'MeshNode' in objectType:        
        return MESH_EXTENSION
    if 'SessionNode' in objectType:        
        return MESH_EXTENSION
    elif 'BIMNode' in objectType:        
        return MESH_EXTENSION
    elif 'PointCloudNode' in objectType:        
        return PCD_EXTENSION    
    elif 'ImageNode' in objectType:        
        return IMG_EXTENSION
    elif 'OrthoNode' in objectType:        
        return IMG_EXTENSION
    else:
        return ['.txt']+MESH_EXTENSION+PCD_EXTENSION+IMG_EXTENSION+RDF_EXTENSIONS

def get_node_type(objectType:str) -> URIRef:
    """Return nodeType as literal.

    Args:
        objectType (str): Type of node class

    Returns:
        URIRef
    """
    if 'MeshNode' in objectType:        
        return v4d['MeshNode']
    elif 'BIMNode' in objectType:        
        return v4d['BIMNode']
    elif 'PointCloudNode' in objectType:        
        return v4d['PointCloudNode']
    elif 'GeometryNode' in objectType:        
        return v4d['GeometryNode']
    elif 'ImageNode' in objectType:        
        return v4d['ImageNode']
    elif 'OrthoNode' in objectType:        
        return v4d['OrthoNode']
    elif 'SessionNode' in objectType:        
        return v4d['SessionNode']
    elif 'linesetNode' in objectType:        
        return v4d['linesetNode']
    else:
        return v4d['Node']

def get_data_type(value) -> XSD.ENTITY:
    """Return XSD dataType of value

    Args:
        value (any): data

    Returns:
        XSD.ENTITY 
    """
    if 'bool' in str(type(value)):        
        return XSD.boolean
    elif 'int' in str(type(value)):  
        return XSD.integer
    elif 'float' in str(type(value)):  
        return XSD.float
    elif 'date' in str(type(value)):  
        return XSD.dateTime   
    else:
        return XSD.string

def match_uri(attribute :str) -> URIRef:
    """
    Match attribute name with Linked Data URI's. Non-matches are serialized as v4d."attribute"
    """
    #NODE
    
    # exif = rdflib.Namespace('http://www.w3.org/2003/12/exif/ns#')
    # geo=rdflib.Namespace('http://www.opengis.net/ont/geosparql#') #coordinate system information
    # gom=rdflib.Namespace('https://w3id.org/gom#') # geometry representations => this is from mathias
    # omg=rdflib.Namespace('https://w3id.org/omg#') # geometry relations
    # fog=rdflib.Namespace('https://w3id.org/fog#')
    # v4d=rdflib.Namespace('https://w3id.org/v4d/core#')
    # openlabel=rdflib.Namespace('https://www.asam.net/index.php?eID=dumpFile&t=f&f=3876&token=413e8c85031ae64cc35cf42d0768627514868b2f#')
    # e57=rdflib.Namespace('http://libe57.org#')
    # xcr=rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    # ifc=rdflib.Namespace('http://ifcowl.openbimstandards.org/IFC2X3_Final#')

    #OPENLABEL
    if attribute in ['timestamp','sensor']:
        return openlabel[attribute]
    #E57
    elif attribute in ['cartesianBounds','cartesianTransform','geospatialTransform','pointCount','e57XmlPath','e57Path','e57Index','e57Image']:
        return  e57[attribute]
    #GOM
    elif attribute in ['coordinateSystem']:
        return  gom[attribute]
    #IFC
    elif attribute in ['ifcPath','className','globalId','phase','ifcName']:
        return  ifc[attribute]
    #EXIF
    elif attribute in ['xResolution','yResolution','resolutionUnit','imageWidth','imageHeight']:
        return  exif[attribute]
    #XCR
    elif attribute in ['focalLength35mm','principalPointU','principalPointV','distortionCoeficients','gsd']:
        return  xcr[attribute]
    #XCR
    elif attribute in ['isDerivedFromGeometry']:
        return  omg[attribute]
    #V4D
    else:
        return v4d[attribute]
