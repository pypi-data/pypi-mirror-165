"""
TiffExtract
-------------

"""
import os


def read_zsensor_retrace(fp):
    """
    Reads the ZSensor Trace from an IBW file

    Parameters
    ----------
    fp: str
        Filepath to ibw

    Returns
    -------
    zsensor_retrace : np.ndarray
        array representing grayscale image of zsensor retrace read from ibw

    """
    zsensor_retrace = __read_retrace(fp, 3)
    return zsensor_retrace


def extract_tiffs(fp, directory):
    """
    Extracts the four images contained within an IBW file, saves them as TIFFs.
    Also saves metadata in associated CSV file.

    Parameters
    ----------
    fp : str
        Filepath to ibw
    directory: str
        Filepath to target directory for output TIFFs

    Returns
    -------
    errors : array
        array of filepaths that could not be extracted for a given ibw
    """
    # print(fp)

    # Split the filepath
    f_base = os.path.basename(fp)
    f_strip = os.path.splitext(f_base)[0]
    f_target = directory + f_strip

    rts = []
    errors = []
    # Read the Height Retrace
    try:
        hrt = read_height_retrace(fp)
        rts.append(hrt)
    except:
        print(f_strip + " has no Height Retrace to extract.")
        errors.append(f_target + "HRT")

    # Read the Amplitude Retrace
    try:
        art = read_amplitude_retrace(fp)
        rts.append(art)
    except:
        print(f_strip + " has no Amplitude Retrace to extract.")
        errors.append(f_target + "ART")

    # Read the Phase Retrace
    try:
        prt = read_phase_retrace(fp)
        rts.append(prt)
    except:
        print(f_strip + " has no Phase Retrace to extract.")
        errors.append(f_target + "PRT")

    # Read the ZSensor Retrace
    try:
        zrt = read_zsensor_retrace(fp)
        rts.append(zrt)
    except:
        print(f_strip + " has no ZSensor Retrace to extract.")
        errors.append(f_target + "ZRT")

    fa = f_target + "A.tiff"
    fb = f_target + "B.tiff"
    fc = f_target + "C.tiff"
    fd = f_target + "D.tiff"
    fps = [fa, fb, fc, fd]

    # Save the retraces as TIFF files
    for (rt, f) in zip(rts, fps):
        save_retrace(rt, f)

    # Metadata extraction
    meta_error = extract_metadata(fp, directory)

    if meta_error:
        errors = errors + meta_error

    print("Saved IBW file: " + f_strip)
    return errors


def extract_metadata(fp, directory):
    """
    Extracts the metadata from the provided ibw file to the specified directory

    Parameters
    ----------
    fp : str
        Filepath to ibw
    directory: str
        Filepath to target directory for output metadata CSV

    Returns
    -------
    errors : array
        array of filepaths that could not be extracted for a given ibw
    """
    f_base = os.path.basename(fp)
    f_strip = os.path.splitext(f_base)[0]
    f_target = directory + f_strip + ".csv"
    errors = []

    try:
        metadata = cio.read_notes(fp)

        # print(type(metadata))
        # print(len(metadata))
        # print(metadata)

        with open(f_target, "w+") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in metadata.items():
                writer.writerow([key, value])
    except:
        print("I/O Error")
        errors.append(f_target + "METADATA")

    return errors


def contains_subdir(directory):
    """
    Checks to see if there are any subdirectories in the specified directory

    Parameters
    ----------
    directory : str
        Path of directory

    Returns
    -------
    all(list_dir) : bool
        True if no files are directories

    """
    list_dir = [os.path.isfile(os.path.join('.', f)) for f in os.listdir(directory)]
    return all(list_dir)


def contains_ibw(directory):
    """
    Checks to see if directory contains an IBW file

    Parameters
    ----------
    dir : str
        Path of directory

    Returns
    -------
    any(...) : bool
        True if there exists an IBW file

    """
    return any(fname.endswith('.ibw') for fname in os.listdir('.'))


def ibw_dirs_all():
    ibw_dirs = []
    ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP-ML-AFM-Data/Movies/200227 G/200227_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/200305 F Start/200305_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/200306 AA/200306_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201209 B/201209_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201211 Q/201211_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201211 Q/__201211 Q/201211_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/210106 H mixed/210106_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP-ML-AFM-Data/Movies/210106 H mixed/__210106 H mixed/210106_raw")
    # ibw_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/210122 G mixed/210122_raw")
    return ibw_dirs


def target_dirs_all():
    target_dirs = []
    target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP-ML-AFM-Data/Movies/200227 G/200227_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/200305 F Start/200305_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/200306 AA/200306_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201209 B/201209_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201211 Q/201211_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/201211 Q/__201211 Q/201211_Q_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/210106 H mixed/210106_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/210106 H mixed/__210106 H mixed/210106_H_mixed_tiff/")
    # target_dirs.append("/home/dcm101/CSE_MSE_RXF131/staging/mdle/A-xtal/FP_ML_AFM_Data/Movies/210122 G mixed/210122_tiff/")
    return target_dirs


def def_dirs():
    ibw_dir = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200227_raw"
    target_dir = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200227_tiff/"
    return ibw_dir, target_dir


def extract():
    ibw_dirs, target_dirs = def_dirs()

    ibws = Path(ibw_dirs).glob('*.ibw')
    for ibw in ibws:
        extract_tiffs(ibw, target_dirs)


def extract_all():
    ibw_dir_1 = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200227_raw"
    ibw_dir_2 = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200306_raw"
    target_dir_1 = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200227_tiff/"
    target_dir_2 = "/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/200306_tiff/"

    ibw_dirs = [ibw_dir_1, ibw_dir_2]
    target_dirs = [target_dir_1, target_dir_2]
    # ibw_dirs = ibw_dirs_all()
    # target_dirs = target_dirs_all()
    all_errors = []

    for ibw_dir, target_dir in zip(ibw_dirs, target_dirs):
        ibws = Path(ibw_dir).glob('*.ibw')
        for ibw in ibws:
            errors = extract_tiffs(ibw, target_dir)
            if errors:
                all_errors.append(errors)

    print("Files with extraction errors: ")
    print(all_errors)

    with open("/home/dcm101/CSE_MSE_RXF131/cradle-members/mdle/dcm101/pra-test/extract_errors_test.csv",
              "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(all_errors)


if __name__ == "__main__":
    extract_all()
