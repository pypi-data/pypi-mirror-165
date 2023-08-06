# Script with functions to read, modify, and re-write ex-file formats used with JETTO

# Required imports
import os.path
try:
    import pwd
except ImportError:
    pwd = None
import datetime
import re
import struct
import shutil
import copy
import collections
from itertools import tee
from pathlib import Path

import numpy as np
try:
    from scipy.io import savemat
except:
    savemat = None

dtypes = {'int':'i', 'float':'f', 'double':'d', 'char':None}
byte_orderingtag = {'>':'Big-endian', '<':'Little-endian'}
byte_ordering = {'b': '>', 'l': '<'}

header_finder = re.compile(b'\*\n\*[\w, \d]+\n')
spec_finder = re.compile(b'#\w+;\d+;\d+;[\w, \d\-]+;\d+\n')

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def decode_spec(spec):
    """
    A spec line has the following format:

    #<dtype>;<no. of time steps (separated by newline)>;<no. of radial points (no separation character)>;<quantity name>;<no. of lines of metadata (always before binary)>
    """

    if not spec.startswith('#'):
        raise Exception(spec, ' is not a spec line')
    splitted = spec[1:-1].split(';')
    if len(splitted) != 5:
        raise Exception(spec, ' is not a spec line')

    jet_format = splitted[0]
    ignored = splitted[1]
    npoints = int(splitted[2])
    label = splitted[3]
    nlines = int(splitted[4])
    return label, jet_format, npoints, nlines

def decode_section(section, sec_num, endianness='>'):
    m = header_finder.match(section)
    header_string = section[:m.end()]
    section_string = section[m.end():]

    # Look for all data specs in the section (starts with #dtype;....)
    spec_starts = [match.start() for match in spec_finder.finditer(section_string)]
    spec_starts.append(len(section_string)) # To also read the last block
    blocks = [section_string[start:next_start] for start, next_start in pairwise(spec_starts)]
    if b''.join(blocks) != section_string:
        raise Exception('Something weird happened, did not split all blocks correctly')

    section_data = collections.OrderedDict()
    section_info = collections.OrderedDict()
    for block_num, block in enumerate(blocks):
        var_label, block_data, var_info = decode_block(block)
        section_data[var_label] = block_data
        section_info[var_label] = var_info
        section_info[var_label]['SECNUM'] = sec_num + 1

    section_header = header_string[3:-1].decode('latin-1')
    return section_header, section_data, section_info


def decode_metadata(raw_metadata):
    itag = None
    tags = ['UNITS', 'DESC', 'SCSTR', 'XBASE', 'UID', 'DDA', 'DTYPE', 'SEQ']
    meta = list(map(lambda x: x.decode('latin-1').strip(), raw_metadata))
    metadata = dict(zip(tags, meta))
    if 'SCSTR' in metadata:
        metadata['SCALE'] = float(metadata['SCSTR'].strip())
    if 'UNITS' in metadata:
        if metadata['UNITS'] == '':
            metadata['UNITS'] = None
    return metadata

def decode_block(block, endianness='>'):
    m = spec_finder.match(block)
    spec_string = block[:m.end()]
    block_string = block[m.end():]
    spec = spec_string.decode('latin-1')
    var_label, jet_format, npoints, nlines = decode_spec(spec)
    var_format = dtypes[jet_format]
    # Read metadata
    splitted = re.split(b'(\n)', block_string)
    raw_metadata = splitted[:2*nlines:2]
    raw_data = b''.join(splitted[2*nlines:-2])
    var_metadata = decode_metadata(raw_metadata)
    var_metadata['LABEL'] = var_label
    var_metadata['FORM'] = jet_format
    if var_format is None:
        # No decoding needed, just read
        decoded_var = raw_data.decode('latin-1').strip()
    else:
        if len(raw_data) == 0:
            # Empty variable
            if var_format in ['i', 'f', 'd']:
                # Empty float array with a shape, fill with nans
                decoded_var = np.full(npoints, np.nan)
        else:
            try:
                decoded_var = struct.unpack(endianness + npoints*var_format, raw_data)
                if var_format is None:
                    decoded_var = decoded_var[0]
                elif var_format in ['i', 'f', 'd']:
                    decoded_var = np.array(decoded_var)
            except:
                raise Exception('Could not decode {!s} with spec {!s}'.format(var_label, spec))
    if 'SCALE' in var_metadata:
        try:
            decoded_var *= var_metadata['SCALE']
        except:
            raise Exception('Cannot rescale', var_label)
    return var_label.upper(), decoded_var, var_metadata

def convert_binary_file(input_file, output_file='binconv.txt'):
    """
    Converts a JETTO binary file into a text file with the same
    format as the original binary file. Effectively all binary
    numerical data is converted into ASCII. Can read .ex, .ext,
    .jsp, .jst, .jss, .jse files.
    """
    supported_file_extensions = ['.ex', '.ext', '.jsp', '.jst', '.jss', '.jse']
    ipath = Path(input_file)
    if not ipath.is_file():
        raise IOError("File %s not found. Abort." % (str(ipath.absolute())))
    if ipath.suffix not in supported_file_extensions:
        raise TypeError("Invalid input file format. Abort.")

    ofname = 'binconv.txt'
    if isinstance(output_file,str):
        ofname = output_file
    if not ofname.endswith('.txt'):
        ofname = ofname + '.txt'
    opath = Path(ofname)
    if not opath.parent.exists():
        opath.parent.mkdir(parents=True)

    status = 1
    with open(str(opath.absolute()),'w') as ofile:
        with open(str(ipath.absolute()),'rb') as ifile:
            bord = None
            bform = None
            npoints = 0
            label = None
            nlines = 0
            scale = 1.0
            fblock = False
            rlines = 0
            eof = False
            while not eof:
                if fblock:
                    rlines = rlines + 1
                    dline = None
                    if (nlines - rlines) >= 0:
                        dline = ifile.readline().decode('latin-1')
                    if bform is None and bord is None:
                        if (nlines - rlines) < 0:
                            dline = ifile.readline().decode('latin-1')
                            bord = dline.strip()
                            bord = byte_ordering[bord]
                    if bform is not None:
                        if (nlines - rlines) <= 0:
                            fsize = struct.calcsize(bord+bform)
                            bdata = ifile.read(npoints*fsize)
                            nstr = "%d" % (npoints)
                            vals = struct.unpack(bord+nstr+bform,bdata)
                            for ii in np.arange(0,len(vals)):
                                if re.match(r'^[fd]$',bform,flags=re.IGNORECASE):
#                                    ofile.write("%20.10e" % (scale * vals[ii]))
                                    ofile.write("%20.10e" % (vals[ii]))
                                else:
#                                    ofile.write("%20d" % (int(scale * vals[ii])))
                                    ofile.write("%20d" % (int(vals[ii])))
                                if (ii + 1) % 5 == 0 or (ii + 1) == npoints:
                                    ofile.write('\n')
                        else:
                            ofile.write(dline)
#                            if rlines == 3:
#                                scale = float(dline.strip())
                    else:
                        if (nlines - rlines) < 0 and dline is None:
                            dline = ifile.readline().decode('latin-1')
                        ofile.write(dline)
                    if (nlines - rlines) <= 0:
                        fblock = False
                        rlines = 0
                else:
                    dline = ifile.readline().decode('latin-1')
                    if dline.startswith('*'):
                        bform = None
                        npoints = 0
                        label = None
                        nlines = 0
                        scale = 1.0
                        fblock = False
                        rlines = 0
                        ofile.write(dline)
                        sline = dline.strip()
                        if sline.endswith("EOF"):
                            eof = True
                    elif dline.startswith('#'):
                        sline = dline[1:-1].split(';')
                        bstr = sline[0]
                        bform = dtypes[bstr]
                        npoints = int(sline[2])
                        label = sline[3]
                        nlines = int(sline[4])
                        ofile.write(dline)
                        fblock = True
                        rlines = 0
            status = 0

    return status

def replace_none(any_dict, replace_val=[]):
    """
    Recursively replace None values in dict with replace_val.
    Modifies in place!
    """
    for k, v in any_dict.items():
        if v is None:
            any_dict[k] = replace_val
        elif isinstance(v, (dict, collections.OrderedDict)):
            replace_none(v)

def write_mat(binary_dict, output_file):
    if savemat is not None:
        bf = copy.deepcopy(binary_dict)
        replace_none(bf)
        savemat(output_file, bf, oned_as='column')
    else:
        raise IOError("MATLAB write requires scipy.io.savemat - please install scipy first.")

def read_binary_file(input_path, output_file=None):
    """
    Reads a JETTO binary file into memory, for use within
    Python scripts or IPython. Resulting data structure
    should be used for writing custom JETTO binary files
    using this tool. Can read .ex, .ext, .jsp, .jst, .jss,
    .jse files.
    """
    supported_file_extensions = ['.ex', '.ext', '.jsp', '.jst', '.jss', '.jse', '.jhp', '.jht', '.ssp', '.sst', '.jasp', '.jast', '.jsd']
    ipath = Path(input_path)
    if not ipath.is_file():
        raise Exception("File %s not found. Abort." % (str(ipath.absolute())))
    if ipath.suffix not in supported_file_extensions and not ipath.suffix.startswith('.ssp') and not ipath.suffix.startswith('.sst'):
        raise Exception("Extention of file %s not in allowed list. Abort." % (str(ipath.absolute())))

    if isinstance(output_file,str):
        convert_binary_file(str(ipath.absolute()),output_file)

    # Store data from input file in dictionary
    data = collections.OrderedDict()
    data['INFO'] = collections.OrderedDict()

    data_types    = {'int': 'i', 'float': 'f', 'double': 'd'}
    data_size    = {'int': 4, 'float': 4, 'double': 8}

    with open(str(ipath.absolute()), 'rb') as inh:
        indata = inh.read()

    # First split the huge string into sections. A section starts with *\n*HEADER
    section_header_starts = [match.start() for match in header_finder.finditer(indata)]
    section_header_starts.append(len(indata)) # Also read the last section
    sections = [indata[start:next_start] for start, next_start in pairwise(section_header_starts)]
    if b''.join(sections) != indata:
        raise Exception('Something weird happened, did not split all sections correctly')

    # First section has info we need to decode the rest
    section_header, section_data, header_info = decode_section(sections[0], 0)
    data[section_header] = section_data
    endianness = byte_ordering[section_data['FILE FORMAT']]

    # Now decode all sections
    for sec_num, section in enumerate(sections[1:-1], start=1):
        section_header, section_data, section_info = decode_section(section, sec_num, endianness=endianness)
        if section_header == 'Profiles':
            if 'Profiles' not in data:
                data['Profiles'] = []
            data[section_header].append(section_data)
        else:
            data[section_header] = section_data

        for k, v in section_info.items():
            if k not in data['INFO']:
                 data['INFO'][k] = v

    # Merge all profiles together into 2D arrays
    if 'Profiles' in data:
        profiles = collections.OrderedDict()
        for prof in data['Profiles']:
            for key in prof.keys():
                if key not in profiles:
                    profiles[key] = []
                profiles[key].append(prof[key])

        for key in list(profiles.keys()):
            profiles[key] = np.stack(profiles[key])

        data['Profiles'] = profiles

    data = convert_data_to_EX2GK(data, header_info, endianness)
    return data

def convert_data_to_EX2GK(data, header_info, endianness):
    data['SECTIONS'] = [key for key in data.keys() if key != 'INFO']
    for key in data['SECTIONS']:
        dateval = None
        timeval = None
        if key == 'File Header':
            dateval = data['File Header'].pop('DATE')
            timeval = data['File Header'].pop('TIME')
        data.update(data.pop(key))
        if dateval is not None:
            data['CREATION_DATE'] = dateval
        if timeval is not None:
            data['CREATION_TIME'] = timeval
    for timename in ['TIME', 'TVEC1']:
        if timename in data:
            data[timename] = data[timename][:, np.newaxis]
    dateinf = header_info.pop('DATE')
    timeinf = header_info.pop('TIME')
    data['INFO'].update(header_info)
    data['INFO']['FILE FORMAT']['FULLNAME'] = byte_orderingtag[endianness]
    data['INFO']['CREATION_DATE'] = dateinf
    data['INFO']['CREATION_TIME'] = timeinf
    data['INFO']['INFO'] = {'DESC': 'Additional information on data fields'}
    data['INFO']['SECTIONS'] = {'DESC': 'Labelled section and order within EX-FILE'}
    for key, val in data.items():
        if key not in ['INFO', 'SECTIONS']:
            if isinstance(val, np.ndarray) and val.ndim < 2:
                data[key] = np.atleast_2d(val)
    return data


def write_as_EX2GK_output(data,varlist=None,output_file='custom.txt',timeslice=None,timeout=None):
    """
    Writes JETTO binary data, read using the function
    found within these tools, in the standardized ASCII
    format of the EX2GK program, for use in comparisons
    between fitted and simulated profiles. Recommended
    to use .txt extension, but not necessary.
    """
    if not isinstance(data,(dict,collections.OrderedDict)):
        raise TypeError("Invalid input data structure, must be a dictionary. Abort.")
    elif "INFO" not in data:
        raise TypeError("Input data dictionary not correctly formatted. Abort.")
    conv = {"TI": "TI1", "ANGF": "AFTOR"}

    qlist = []
    ofname = 'custom.txt'
    tsi = -1
    time = None
    if isinstance(varlist,(list,tuple)):
        for qi in np.arange(0,len(varlist)):
            if varlist[qi] in data:
                qlist.append(varlist[qi])
    if isinstance(output_file,str):
        ofname = output_file
    opath = Path(ofname)
    if not opath.parent.exists():
        opath.parent.mkdir(parents=True)
    if isinstance(timeslice,(int,float,np.float16,np.float32,np.float64)) and "TIME" in data:
        tvec = data["TIME"].flatten()
        idxv = np.where(tvec >= float(timeslice))[0]
        if len(idxv) > 0:
            tsi = idxv[0] if np.abs(tvec[idxv[0]] - float(timeslice)) <= np.abs(tvec[idxv[0] - 1] - float(timeslice)) else idxv[0] - 1
    if isinstance(timeout,(int,float,np.float16,np.float32,np.float64)):
        time = float(timeout)
    if time is None and "TIME" in data:
        tvec = data["TIME"].flatten()
        time = float(tvec[tsi])

    if len(qlist) > 0:
        with open(str(opath.absolute()),'w') as ofile:
            if data:
                ofile.write("### EX2GK - JSP Data Conversion File ###\n")
                ofile.write("\n")
                ofile.write("START OF HEADER\n")
                ofile.write("\n")
                ofile.write("        Shot Number: %20d\n" % (int(data["SHOT"])))
                ofile.write("  Radial Coordinate: %20s\n" % ("RHOTORN"))
                ofile.write("               Time: %18.6f s\n" % (time))
                ofile.write("\n")
                ofile.write("END OF HEADER\n")
                ofile.write("\n")
            for jj in np.arange(0,len(qlist)):
                xbase = data["INFO"][qlist[jj]]["XBASE"]
                xfit = data[xbase][tsi,:].flatten()
                yfit = data[qlist[jj]][tsi,:].flatten()
                yefit = np.zeros(xfit.shape)
                qtag = conv[qlist[jj]] if qlist[jj] in conv else qlist[jj]
                ofile.write("%15s%20s%20s\n" % ("RHOTORN",qtag+" Sim","Err. "+qtag+" Sim"))
                for ii in np.arange(0,xfit.size):
                    ofile.write("%15.4f%20.6e%20.6e\n" % (xfit[ii],yfit[ii],yefit[ii]))
                ofile.write("\n")


def create_exfile_structure(database,shot,version_tag=None,extfile=False):
    """
    Creates an empty structure for JETTO binary ex-file
    representation in memory. The structure is only useful
    for use in functions within this tool!
    """
    # Required user input - forced crash if improper
    if not isinstance(database,str):
        raise ValueError('Database field for ex-file generation must be a string')
    if not isinstance(shot,(int,float,np.int8,np.int16,np.int32,np.float16,np.float32,np.float64)):
        raise ValueError('Shot number field for ex-file generation must be numeric')
    datablock_tag = 'Traces' if extfile else 'Profiles'

    # Initialize structure
    data = collections.OrderedDict()
    data['INFO'] = collections.OrderedDict()
    data['SECTIONS'] = ['File Header', 'General Info', 'PPF Attributes', 'PPF Base Vectors', datablock_tag]

    # Add standard descriptions of required metadata - covers until end of 'PPF Attributes' section
    data['INFO']['INFO'] = {'DESC': 'Additional information on data fields'}
    data['INFO']['SECTIONS'] = {'DESC': 'Labelled section and order within EX-FILE'}
    data['INFO']['FILE FORMAT'] = {'FORM': 'char', 'FULLNAME': 'Big-endian', 'LABEL': 'File Format', 'SECNUM': 1}
    data['INFO']['FILE DESCRIPTION'] = {'FORM': 'char', 'LABEL': 'File Description', 'SECNUM': 1}
    data['INFO']['VERSION'] = {'FORM': 'char', 'LABEL': 'Version', 'SECNUM': 1}
    data['INFO']['CREATION_DATE'] = {'FORM': 'char', 'LABEL': 'Date', 'SECNUM': 1}
    data['INFO']['CREATION_TIME'] = {'FORM': 'char', 'LABEL': 'Time', 'SECNUM': 1}
    data['INFO']['DATABASE NAME'] = {'FORM': 'char', 'LABEL': 'Database Name', 'SECNUM': 2}
    data['INFO']['USER EX-FILE'] = {'FORM': 'char', 'LABEL': 'User EX-file', 'SECNUM': 2}
    data['INFO']['USER PRE-MODEX EX-FILE'] = {'FORM': 'char', 'LABEL': 'User Pre-Modex EX-file', 'SECNUM': 2}
    data['INFO']['SHOT'] = {'FORM': 'int', 'LABEL': 'Shot', 'SECNUM': 3}
    data['INFO']['DDA NAME'] = {'FORM': 'char', 'LABEL': 'DDA Name', 'SECNUM': 3}

    # Add required metadata - covers until end of 'PPF Attributes' section
    data['FILE FORMAT'] = 'b'
    data['FILE DESCRIPTION'] = 'EX-FILE'
    data['VERSION'] = version_tag if isinstance(version_tag,str) else '1.0 : JETTO Python tools'
    data['CREATION_DATE'] = datetime.datetime.now().strftime("%d/%m/%Y")
    data['CREATION_TIME'] = datetime.datetime.now().strftime("%H:%M:%S")
    data['DATABASE NAME'] = database
    data['USER EX-FILE'] = ''
    data['USER PRE-MODEX EX-FILE'] = ''
    data['SHOT'] = np.atleast_2d([int(shot)]) 
    data['DDA NAME'] = 'EX'

    return data


def write_binary_exfile(data,output_file='custom'):
    """
    Writes a customized JETTO binary ex-file, for use
    within JETTO. Recommended to read in a similar ex-file
    to acquire the necessary data structure used by this
    tool. Only writes .ex and .ext files.
    """
    if not isinstance(data,(dict,collections.OrderedDict)):
        raise TypeError("Invalid input data structure, must be a dictionary. Abort.")
    elif "INFO" not in data or "SECTIONS" not in data:
        raise TypeError("Input data dictionary not correctly formatted. Abort.")

    dsizes = {'int':4, 'float':4, 'double':8, 'char':None}

    di = data["INFO"]
    ds = data["SECTIONS"]
    baseidx = ds.index('PPF Base Vectors') if 'PPF Base Vectors' in ds else 3
    ofname = 'custom.ex'
    if isinstance(output_file,str):
        ofname = output_file
    if not ofname.endswith('.ex'):
        ofname = ofname + '.ex'
    if "TVEC1" in di and di["TVEC1"]["SECNUM"] == (baseidx + 1) and not ofname.endswith('.ext'):
        ofname = ofname + 't'
    opath = Path(ofname)
    if not opath.parent.exists():
        opath.parent.mkdir(parents=True)

    status = 1
    bord = byte_ordering[data["FILE FORMAT"]] if "FILE FORMAT" in data else byte_ordering['b']
    with open(str(opath.absolute()),'wb') as ofile:
        NL = '\n'.encode()
        for ii in np.arange(1,len(ds) + 1):

            if not re.match('^Profiles$',ds[ii-1],flags=re.IGNORECASE):
                hstr1 = '*'
                ofile.write(hstr1.encode() + NL)
                hstr2 = '*' + ds[ii-1]
                ofile.write(hstr2.encode() + NL)
                for key in data:
                    if "SECNUM" in di[key] and di[key]["SECNUM"] == ii:
                        nstr = '1'
                        rnum = 0
                        if not re.match(r'^char$',di[key]["FORM"],flags=re.IGNORECASE):
                            nstr = "%d" % (data[key].shape[1])
                            rnum = -1
                        if "SEQ" in di[key]:
                            rnum = 8
                        elif "DTYPE" in di[key]:
                            rnum = 7
                        elif "DDA" in di[key]:
                            rnum = 6
                        elif "UID" in di[key]:
                            rnum = 5
                        elif "XBASE" in di[key]:
                            rnum = 4
                        elif "SCSTR" in di[key]:
                            rnum = 3
                        elif "DESC" in di[key]:
                            rnum = 2
                        elif "UNITS" in di[key]:
                            rnum = 1
                        rstr = '%d' % (rnum) if rnum >= 0 and not re.match(r'^Shot$',key,flags=re.IGNORECASE) else '0'
                        hdelim = ';'
                        fstr = '#' + hdelim.join((di[key]["FORM"],'1',nstr,di[key]["LABEL"],rstr))
                        ofile.write(fstr.encode() + NL)
                        if rnum >= 1:
                            estr = di[key]["UNITS"] if isinstance(di[key]["UNITS"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 2:
                            estr = di[key]["DESC"] if isinstance(di[key]["DESC"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 3:
                            estr = di[key]["SCSTR"] if isinstance(di[key]["SCSTR"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 4:
                            estr = di[key]["XBASE"] if isinstance(di[key]["XBASE"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 5:
                            estr = di[key]["UID"] if isinstance(di[key]["UID"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 6:
                            estr = di[key]["DDA"] if isinstance(di[key]["DDA"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 7:
                            estr = di[key]["DTYPE"] if isinstance(di[key]["DTYPE"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum >= 8:
                            estr = di[key]["SEQ"] if isinstance(di[key]["SEQ"],str) else ''
                            ofile.write(estr.encode() + NL)
                        if rnum == 0:
                            ofile.write(data[key].encode() + NL)
                        else:
                            scale = di[key]["SCALE"] if "SCALE" in di[key] else 1.0
                            dtype = dtypes[di[key]["FORM"]]
                            dsize = dsizes[di[key]["FORM"]]
                            for jj in np.arange(0,data[key].shape[1]):
                                dstr = b''
                                if re.match(r'^[fd]$',dtype,flags=re.IGNORECASE):
                                    dstr = struct.pack(bord+dtype,float(data[key][0,jj] / scale))
                                else:
                                    dstr = struct.pack(bord+dtype,int(data[key][0,jj] / scale))
                                ofile.write(dstr)
                            ofile.write(NL)

            elif "TVEC1" in data and isinstance(data["TVEC1"],np.ndarray):
                for tt in np.arange(0,data["TVEC1"].shape[0]):
                    hstr1 = '*'
                    ofile.write(hstr1.encode() + NL)
                    hstr2 = '*' + ds[ii-1]
                    ofile.write(hstr2.encode() + NL)
                    for key in data:
                        if "SECNUM" in di[key] and di[key]["SECNUM"] == ii:
                            nstr = '1'
                            rnum = 0
                            if not re.match(r'^char$',di[key]["FORM"],flags=re.IGNORECASE):
                                nstr = "%d" % (data[key].shape[1])
                                rnum = -1
                            if "SEQ" in di[key]:
                                rnum = 8
                            elif "DTYPE" in di[key]:
                                rnum = 7
                            elif "DDA" in di[key]:
                                rnum = 6
                            elif "UID" in di[key]:
                                rnum = 5
                            elif "XBASE" in di[key]:
                                rnum = 4
                            elif "SCSTR" in di[key]:
                                rnum = 3
                            elif "DESC" in di[key]:
                                rnum = 2
                            elif "UNITS" in di[key]:
                                rnum = 1
                            rstr = '%d' % (rnum) if rnum >= 0 else '0'
                            hdelim = ';'
                            fstr = '#' + hdelim.join((di[key]["FORM"],'1',nstr,di[key]["LABEL"],rstr))
                            ofile.write(fstr.encode() + NL)
                            if rnum >= 1:
                                estr = di[key]["UNITS"] if isinstance(di[key]["UNITS"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 2:
                                estr = di[key]["DESC"] if isinstance(di[key]["DESC"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 3:
                                estr = di[key]["SCSTR"] if isinstance(di[key]["SCSTR"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 4:
                                estr = di[key]["XBASE"] if isinstance(di[key]["XBASE"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 5:
                                estr = di[key]["UID"] if isinstance(di[key]["UID"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 6:
                                estr = di[key]["DDA"] if isinstance(di[key]["DDA"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 7:
                                estr = di[key]["DTYPE"] if isinstance(di[key]["DTYPE"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum >= 8:
                                estr = di[key]["SEQ"] if isinstance(di[key]["SEQ"],str) else ''
                                ofile.write(estr.encode() + NL)
                            if rnum == 0:
                                ofile.write(data[key].encode() + NL)
                            else:
                                scale = di[key]["SCALE"] if "SCALE" in di[key] else 1.0
                                dtype = dtypes[di[key]["FORM"]]
                                dsize = dsizes[di[key]["FORM"]]
                                for jj in np.arange(0,data[key].shape[1]):
                                    dstr = b''
                                    if re.match(r'^[fd]$',dtype,flags=re.IGNORECASE):
                                        if data[key].shape[0] > tt:
                                            dstr = struct.pack(bord+dtype,float(data[key][tt,jj] / scale))
                                        else:
                                            dstr = struct.pack(bord+dtype,float(data[key][-1,jj] / scale))
                                            print("   Less time slices than expected in field: %10s" % (di[key]["LABEL"]))
                                    else:
                                        if data[key].shape[0] > tt:
                                            dstr = struct.pack(bord+dtype,int(data[key][tt,jj] / scale))
                                        else:
                                            dstr = struct.pack(bord+dtype,int(data[key][-1,jj] / scale))
                                            print("   Less time slices than expected in field: %10s" % (di[key]["LABEL"]))
                                    ofile.write(dstr)
                                ofile.write(NL)

        hstr1 = '*'
        ofile.write(hstr1.encode() + NL)
        hstr2 = '*EOF'
        ofile.write(hstr2.encode() + NL)
        if ii == len(ds):
            status = 0

    return status


def add_entry(data,key,moddata,dtype,units,description,scale,xbase,tag=None):
    """
    Use this function to add fields to the Python data structure
    generated by this tool. Providence must be explicitly
    provided by the user.
    """
    ikey = None
    idata = None
    ibase = None
    itag = 'Python Addition Tool'
    if isinstance(key,str):
        ikey = key
    if isinstance(moddata,(list,tuple,np.ndarray)):
        idata = np.atleast_2d(moddata)
    if isinstance(xbase,str):
        ibase = xbase
    if isinstance(tag,str):
        itag = itag + ' - ' + tag

    odata = copy.deepcopy(data)
    if pwd is None:
        raise Exception('pwd python module not loaded. Are you sure this is a Linux system?')
    if isinstance(data,(dict,collections.OrderedDict)) and ikey is not None:
        check_flag = True
        if ikey not in ["TVEC1", "XVEC1"]:
            check_array = [False] * idata.ndim
            for ii in range(0,len(check_array)):
                if "TVEC1" in data and idata.shape[ii] == data["TVEC1"].size:
                    check_array[ii] = True
                if "XVEC1" in data and idata.shape[ii] == data["XVEC1"].size:
                    check_array[ii] = True
                if idata.shape[ii] == 1:
                    check_array[ii] = True
            check_flag = all(check_array)
        if check_flag:
            if ikey not in data:
                uname = pwd.getpwuid(os.getuid())[0]
                odata[ikey] = idata.copy()
                odata["INFO"][ikey] = dict()
                odata["INFO"][ikey]["UNITS"] = units            # Units string
                odata["INFO"][ikey]["DESC"] = description       # Description string
                odata["INFO"][ikey]["SCSTR"] = scale            # String representation of scaling for writing into ex-file
                odata["INFO"][ikey]["SCALE"] = float(scale)     # Numeric value for actual scaling operation
                odata["INFO"][ikey]["FORM"] = dtype             # Data type for conversion to binary representation
                odata["INFO"][ikey]["LABEL"] = ikey             # Name of data field, printed verbatim into ex-file
                secnum = odata["SECTIONS"].index('Profiles') + 1 if 'Profiles' in odata["SECTIONS"] else odata["SECTIONS"].index('Traces') + 1
                if ikey == "XVEC1":
                    secnum = odata["SECTIONS"].index('PPF Base Vectors') + 1
                elif ikey == "TVEC1" and "XVEC1" not in odata:
                    secnum = odata["SECTIONS"].index('PPF Base Vectors') + 1
                elif ikey not in ["TVEC1", "XVEC1"]:
                    if ibase is None:
                        ibase = "XVEC1" if "XVEC1" in odata else "TVEC1"
                    odata["INFO"][ikey]["XBASE"] = ibase        # Data field name of reference vector as given in PPF Base Vectors section
                    odata["INFO"][ikey]["UID"] = uname          # User ID (auto-detected)
                    odata["INFO"][ikey]["DDA"] = itag           # DDA name in PPF system (replaced with metadata)
                    odata["INFO"][ikey]["DTYPE"] = ''           # Data field name in PPF system (replaced with empty string)
                    odata["INFO"][ikey]["SEQ"] = '0'            # Sequence number in PPF system (replaced with zero string)
                odata["INFO"][ikey]["SECNUM"] = secnum          # Section number of data field for proper separation in ex-file
            else:
                print("   Requested field already present in data structure. Addition aborted.")
        else:
            print("   Input %s data is not consistent with base vectors present in data structure. Addition aborted." % (ikey))
    else:
        print("   Base data to be modified is not a dictionary. Use read_binary_file() or create_exfile_structure() function to create it.")

    return odata


def modify_entry(data,key,moddata,tag=None):
    """
    Use this function to modify the Python data structure
    generated by this tool, in order to prepare it for
    writing. This function is recommended as it automatically
    modifies the necessary tags for providence, although
    the user must provide the appropriate tag to be written.
    """
    ikey = None
    idata = None
    itag = 'Python Modification Tool'
    if isinstance(key,str):
        ikey = key
    if isinstance(moddata,(list,tuple)):
        idata = np.array(moddata)
    elif isinstance(moddata,np.ndarray):
        idata = moddata.copy()
    if isinstance(tag,str):
        itag = itag + ' - ' + tag

    odata = None
    if pwd is None:
        raise Exception('pwd python module not loaded. Are you sure this is a Linux system?')
    if isinstance(data,(dict,collections.OrderedDict)) and ikey in data:
        if data[ikey].size == idata.size:
            idata = np.reshape(idata,data[ikey].shape)
        if data[ikey].shape == idata.shape:
            uname = pwd.getpwuid(os.getuid())[0]
            odata = copy.deepcopy(data)
            odata[ikey] = idata.copy()
            odata["INFO"][ikey]["UID"] = uname    # User ID (auto-detected)
            odata["INFO"][ikey]["DDA"] = itag     # DDA name in PPF system (replaced with metadata)
            odata["INFO"][ikey]["DTYPE"] = ''     # Data field name in PPF system (replaced with empty string)
            odata["INFO"][ikey]["SEQ"] = '0'      # Sequence number in PPF system (replaced with zero string)
        else:
            print("   Input data is not the same shape as existing data structure: ", data[ikey].shape)
    elif isinstance(data,(dict,collections.OrderedDict)):
        print("   Base data to be modified does not contain the entry %s. Modification aborted.")
    else:
        print("   Base data to be modified is not a dictionary. Use read_binary_file() function to create it.")

    return odata


def modify_exfile(inputdata=None,qlist=None,exfilename=None,outfile=None,globaltag=None):
    """
    Use this function to modify the Python data structure
    generated by this tools via an input dictionary
    containing similarly labelled data. This function is
    recommended for applying multiple modifications
    simultaneously.
    """
    pdata = None
    qqlist = None
    gtag = None
    expath = None
    opath = Path('./modded_exfile.txt')
    if isinstance(inputdata,(dict,collections.OrderedDict)):
        pdata = copy.deepcopy(inputdata)
    if isinstance(qlist,(list,tuple)) and len(qlist) > 0:
        qqlist = []
        for item in qlist:
            if isinstance(pdata,(dict,collections.OrderedDict)) and item in pdata:
                qqlist.append(item)
    if isinstance(exfilename,str):
        exname = exfilename
        if not exname.endswith('.ex'):
            exname = exname + '.ex'
        expath = Path(exname)
    if isinstance(outfile,str):
        opath = Path(outfile)
    if not opath.parent.exists():
        opath.parent.mkdir(parents=True)
    if isinstance(globaltag,str):
        gtag = globaltag

    status = 1
    if pdata is not None and qqlist is not None:
        if expath is not None and expath.is_file():
            exdata = read_binary_file(str(expath.absolute()))
            fmodified = False
            for qq in qqlist:
                if qq in exdata:
                    exdata = modify_entry(exdata,qq,pdata[qq].flatten(),tag=gtag)
                    fmodified = True
                else:
                    print("Quantity %s not found in ex-file, %s. Quantity not changed." % (qq,exname))
            if fmodified:
                exfile = opath.parent / (str(opath.stem) + '.ex')
                status = write_binary_exfile(exdata,str(exfile.absolute()))
                if status != 0:
                    print("Error occurred while writing binary file. Check inputs and try again.")
            else:
                print("No quantities changed. Binary writing aborted.")
        else:
            print("Ex-file %s not found. Binary writing aborted." % (str(expath.absolute())))
        extpath = Path(exname+'t')
        if extpath.is_file():
            extfile = opath.parent / (str(opath.stem) + '.ext')
            shutil.copy2(str(extpath.absolute()),str(extfile.absolute()))

    return status


def repackage_data(data,quantities):
    """
    Use this function to keep only the specified quantities, reducing the amount of
    memory required to store the JETTO output data.
    """
    odata = None
    qlist = []
    if isinstance(data,(dict,collections.OrderedDict)):
        odata = copy.deepcopy(data)
    if isinstance(quantities,str):
        qlist = quantities.split(',')
    elif isinstance(quantities,(list,tuple)):
        qlist = list(quantities)

    if odata is not None and qlist:
        qlist.extend(["INFO","SECTIONS","CREATION_DATE","CREATION_TIME"])
        dlist = []
        for key in odata:
            if key not in qlist:
                dlist.append(key)
        for dkey in dlist:
            del odata[dkey]
            if "INFO" in odata and dkey in odata["INFO"]:
                del odata["INFO"][dkey]
    elif odata is not None:
        print("Invalid quantity list provided for repackaging JETTO data, returning input data!")

    return odata
