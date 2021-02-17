import argparse
import glob
import logging
import os
import zipfile

logging_fmt = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(format=logging_fmt)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def add_directory_to_zip(zipf:zipfile.ZipFile,path:str):
    for root,_,files in os.walk(path):
        for file in files:
            zipf.write(
                os.path.join(root,file),
                os.path.relpath(os.path.join(root,file),os.path.join(path,".."))
            )

def main(args):
    input_root_dir:str=args.input_root_dir
    output_dir:str=args.output_dir
    num_subdirs_per_archive:int=args.num_subdirs_per_archive
    index_lower_bound:int=args.index_lower_bound
    index_upper_bound:int=args.index_upper_bound
    filename_start_index:int=args.filename_start_index

    logger.info(args)

    os.makedirs(output_dir,exist_ok=True)

    pathname=os.path.join(input_root_dir,"*")
    subdirs=glob.glob(pathname)

    num_archives,mod=divmod(len(subdirs),num_subdirs_per_archive)
    if mod!=0:
        num_archives+=1

    filename_index=filename_start_index
    for idx in range(num_archives):
        if idx<index_lower_bound:
            continue
        if index_upper_bound>=0 and idx>=index_upper_bound:
            break

        logger.info("===== Archive #{} =====".format(idx))

        start_index=idx*num_subdirs_per_archive
        end_index=(idx+1)*num_subdirs_per_archive
        input_dirs=subdirs[start_index:end_index]

        archive_filepath=os.path.join(output_dir,str(filename_index)+".zip")
        with zipfile.ZipFile(archive_filepath,"w",zipfile.ZIP_DEFLATED) as zipf:
            for input_dir in input_dirs:
                add_directory_to_zip(zipf,input_dir)

        logger.info("Created an archive file {}".format(archive_filepath))
        filename_index+=1

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input_root_dir",type=str,default="./Image")
    parser.add_argument("-o","--output_dir",type=str,default="./Archive")
    parser.add_argument("-n","--num_subdirs_per_archive",type=int,default=500)
    parser.add_argument("-l","--index_lower_bound",type=int,default=0)
    parser.add_argument("-u","--index_upper_bound",type=int,default=-1)
    parser.add_argument("-f","--filename_start_index",type=int,default=0)
    args=parser.parse_args()

    main(args)
