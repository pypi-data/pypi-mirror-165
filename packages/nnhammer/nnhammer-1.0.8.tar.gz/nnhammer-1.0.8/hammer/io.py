import nibabel as nib
import numpy as np
import scipy.io


def read_mat(input_file, key='scene'):
    data = scipy.io.loadmat(input_file)[key]
    return data


def save_mat(output_file, data, key="scene"):
    scipy.io.savemat(output_file, {key: data})


def read_file(input_file):
    with open(input_file, "r") as input_file:
        return [each.strip("\n") for each in input_file.readlines()]


def write_list_2_file(output_file, data_lst):
    with open(output_file, 'w') as file:
        for i in range(len(data_lst)):
            file.write(data_lst[i])
            if i != len(data_lst) - 1:
                file.write('\n')


def read_nii(input_file):
    data = nib.load(input_file)
    return data.get_fdata()


def save_nii(output_file, data):
    """
    Convert and save as nii.
    Note that nii format needs a shape of WHD
    :param output_file:
    :param data: ndarray image
    """
    # [-1, -1, 1, 1] for RAI, default is LPI
    nii_file = nib.Nifti1Image(data, np.diag((-1, -1, 1, 1)))
    nib.save(nii_file, output_file)
