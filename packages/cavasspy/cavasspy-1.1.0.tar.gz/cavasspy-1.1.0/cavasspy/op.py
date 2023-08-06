import os
import subprocess
import time
import uuid
from typing import Optional, Iterable

from hammer.io import read_mat, save_mat

# CAVASS build path, default in installation is ~/cavass-build
CAVASS_PROFILE_PATH = None


class CAVASSPyError(Exception):
    ...


def env():
    if CAVASS_PROFILE_PATH is not None:
        PATH = f'{os.environ["PATH"]}:{os.path.expanduser(CAVASS_PROFILE_PATH)}'
        VIEWNIX_ENV = os.path.expanduser(CAVASS_PROFILE_PATH)
        return {'PATH': PATH, 'VIEWNIX_ENV': VIEWNIX_ENV}
    return None


def execute_cmd(cavass_cmd):
    p = subprocess.Popen(cavass_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env())
    r, e = p.communicate()
    try:
        r = r.decode()
    except UnicodeDecodeError:
        r = r.decode('gbk')
    e = e.decode().strip()
    if e:
        print(e)
    r = r.strip()
    return r


def get_ct_resolution(input_file):
    """
    Get (H,W,D) resolution of input_file.
    """
    cmd = f'get_slicenumber {input_file} -s'
    r = execute_cmd(cmd)
    if r:
        r = r.split('\n')[2]
        r = r.split(' ')
        r = tuple(map(lambda x: int(x), r))
        return r
    else:
        raise CAVASSPyError(f'Result of command \"{cmd}\" is None.')


def read_cavass_file(input_file, first_slice=None, last_slice=None, sleep_time=1, ):
    """
    Load data of input_file.
    Use the assigned slice indices if both the first slice and the last slice are given.
    Args:
        sleep_time: set a sleep_time between saving and loading temp mat to avoid system IO error.
        first_slice: Loading from the first slice (included). Load from the inferior slice to the superior slice if first_slice is None.
        last_slice: Loading end at the last_slice (included). Load from the inferior slice to the superior slice if last_slice is None.
    """
    tmp_path = '/tmp/cavass'
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path, exist_ok=True)

    output_file = os.path.join(tmp_path, f'{uuid.uuid1()}.mat')
    if first_slice is None or last_slice is None:
        cvt2mat = f"exportMath {input_file} matlab {output_file} `get_slicenumber {input_file}`"
    else:
        cvt2mat = f"exportMath {input_file} matlab {output_file} {first_slice} {last_slice}"
    execute_cmd(cvt2mat)
    time.sleep(sleep_time)
    ct = read_mat(output_file)
    os.remove(output_file)
    return ct


def copy_pose(skew_file, good_file, output_file):
    execute_cmd(f"copy_pose {skew_file} {good_file} {output_file}")


def save_cavass_file(output_file, data, binary=False, size: Optional[Iterable] = None,
                     spacing: Optional[Iterable] = None,
                     reference_file=None):
    """
    Save data as CAVASS format. Do not provide spacing and reference_file at the same time.
    Recommend to use binary for mask files and reference_file to copy all properties.
    Args:
        binary: Save as binary data if True.
        size: Size for converting with dimensions of (H,W,D), default: the size of input data.
        spacing: Spacing for converted CAVASS file with dimensions of (H,W,D), default: 1mm.
        reference_file: Copy pose from the given file.
    """
    assert spacing is None or reference_file is None

    if size is None:
        size = data.shape
    size = ' '.join(list(map(lambda x: str(x), size)))

    spacing = ' '.join(list(map(lambda x: str(x), spacing))) if spacing is not None else ''

    tmp_files = []
    output_path = os.path.split(output_file)[0]
    tmp_mat = os.path.join(output_path, f"tmp_{uuid.uuid1()}.mat")
    tmp_files.append(tmp_mat)
    save_mat(tmp_mat, data)

    if not binary:
        if reference_file is None:
            execute_cmd(f"importMath {tmp_mat} matlab {output_file} {size} {spacing}")
        else:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size}")
            copy_pose(tmp_file, reference_file, output_file)
    if binary:
        if reference_file is None:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size} {spacing}")
            execute_cmd(f"ndthreshold {tmp_file} {output_file} 0 1 1")
        else:
            tmp_file = os.path.join(output_path, f"tmp_{uuid.uuid1()}.IM0")
            tmp_files.append(tmp_file)
            execute_cmd(f"importMath {tmp_mat} matlab {tmp_file} {size}")

            tmp_file1 = os.path.join(output_path, f"tmp_{uuid.uuid1()}.BIM")
            tmp_files.append(tmp_file1)
            execute_cmd(f"ndthreshold {tmp_file} {tmp_file1} 0 1 1")
            copy_pose(tmp_file1, reference_file, output_file)

    for each in tmp_files:
        os.remove(each)


def bin_ops(input_file_1, input_file_2, output_file, op):
    """
    Execute binary operations.
    Args:
        op: Supported options: or, nor, xor, xnor, and, nand, a-b
    """
    cmd_str = f'bin_ops {input_file_1} {input_file_2} {output_file} {op}'
    execute_cmd(cmd_str)


def median2d(input_file, output_path, mode=0):
    """
    Perform median filter.
    Args:
        mode: 0 for foreground, 1 for background, default is 0
    """
    execute_cmd(f"median2d {input_file} {output_path} {mode}")


def dicom2cavass(input_dicom_path, output_file):
    execute_cmd(f'from_dicom {input_dicom_path}/* {output_file}')


def export_math(input_file, output_file, output_file_type='matlab', first_slice=None, last_slice=None):
    """
    Export CAVASS format file to other formats.
    Args:
        input_file:
        output_file:
        output_file_type: Support export format: mathematica, mathlab, r, vtk.
        first_slice:
        last_slice: Export all slices if first slice or last slice is None
    """
    if first_slice or last_slice is None:
        resolution = get_ct_resolution(input_file)
        first_slice, last_slice = 0, resolution[2] - 1

    execute_cmd(f'exportMath {input_file} {output_file_type} {output_file} {first_slice} {last_slice}')
