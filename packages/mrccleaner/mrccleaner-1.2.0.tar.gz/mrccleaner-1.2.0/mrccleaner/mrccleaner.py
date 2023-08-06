__author__ = "Thibault TUBIANA"
__license__ = "MIT"
__date__ = "2022/08"
__version__ = "1.0"

DESCRIPTION = """\
Simple script to recenter and symmetrize MRC file.
Example: mrccleaner -f INPUT.mrc -o OUTPUT.mrc
"""

import sys
import subprocess


def try_import_and_install(package:str, shortname=""):
    """
    Homemade function to try to import packages, and if they don't exist,
    they will be automatically installed with pypi.
    Args:
        package (str): package name (example 'numpy')
        shortname (str): shortname of the package (example : 'np' as for 'import numpy as np')
    """
    if shortname == "":
        importname = package
    else:
        importname = shortname
        
        
    try:
        globals()[importname] = __import__(package)
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        globals()[importname] = __import__(package)






def parseArg():
    """
    Parse Arguments
    @return: dictionnary of arguments
    """
    arguments = argparse.ArgumentParser(description=DESCRIPTION)
    arguments.add_argument('-f', "--file", help="Input MRC file", required=True, type=str)
    arguments.add_argument('-o', '--output', help="Output file (mrc)", default="output.mrc")
    
    args = vars(arguments.parse_args())

    return (args)


def make_it_square(mrcArray):
    """
    Calculate the size and make it square...
    """
    x = mrcArray.shape[0]
    y = mrcArray.shape[1]
    maxsize = np.min([x,y])
    #Only on X now. Patch will come later if needed....
    if y>maxsize:
        diffX = np.abs(maxsize - y)
        remove = int(diffX/2)
        mrcArray = mrcArray[:,remove:-remove]

    print(mrcArray.shape)
    1/0

    return mrcArray
    


def transform_mrc(inputFile:str, outputFile:str):
    """
    Read MRC files and transform them with 
    - fftshift
    - mirror + inversion
    Args:
        inputFile (str): input mrc file path
        outputFile (str): Ouput mrc file path
    """

    with mrcfile.open(inputFile) as mrc:
        im = mrc.data


    #Cut this fucking middle line
    x=im.shape[0]
    halfx = int(x/2)
    #im = np.delete(im, halfx, axis=0)
    #shifted_mrc = np.fft.fftshift(im[:-1,:], axes=0)
    shifted_mrc = np.fft.fftshift(im, axes=0)

    #Now we flipp the centered shifted MRC file, and we invert it (because after A LOT of tries... This has to be done....)

    
    #This line FLIP the shifted mrc AND reverse it vertically AND remove the first pixel column.
    correctMRC = np.concatenate((np.flip(shifted_mrc[::-1,1::]), shifted_mrc), axis=1)
    

    
    #Make it square again...
    correctMRC = correctMRC[:,:-1]
    print(correctMRC.shape)
    with mrcfile.new(outputFile, overwrite=True) as mrc:
        mrc.set_data(correctMRC, )


def main():
    """
    Just the main function
    """

    if len(sys.argv) < 2 :
        print(DESCRIPTION)
        sys.exit(1)
    #Importing packages
    try_import_and_install("mrcfile")
    try_import_and_install("numpy","np")
    try_import_and_install("argparse")

    args = parseArg()

    inputFile = args["file"]
    outputFile = args["output"]

    print("== Transforming output mrc ==")
    print(f"---- Input file: {inputFile}")
    print(f"---- Output file: {outputFile}")
    transform_mrc(inputFile, outputFile)

if __name__ == "__main__":

    main()

