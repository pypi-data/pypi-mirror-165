import os, boto3
os.environ['AWS_ACCESS_KEY_ID'] = "AKIASRWSDKBGDAZEF6C7"
os.environ['AWS_SECRET_ACCESS_KEY'] = "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"

applicable_licenses = ['os','hc','fin']

def download_file_from_s3(
        file_name ='',
        license='fin',
        store_folder = os.getcwd() ,
):
    os.environ['AWS_ACCESS_KEY_ID'] = "AKIASRWSDKBGDAZEF6C7"
    os.environ['AWS_SECRET_ACCESS_KEY'] = "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"

    # TODO CREATE PATH IF NOT EXIST
    start_dir = os.getcwd()
    os.chdir(store_folder)

    bucket="auxdata.johnsnowlabs.com"

    if license == 'fin':
        remote_path = 'finance/models'
    if license == 'os':
        remote_path = 'finance/models'
    if license == 'hc':
        remote_path = 'finance/models'

    remote_path = f"{remote_path}/{file_name}"
    if os.path.exists(file_name.split('.zip')[0]):
        print(f"File already exists in {remote_path}")
        os.chdir(start_dir)
        return
    print(f'Downloading {remote_path} to {store_folder}')
    s3 = boto3.client('s3')
    s3.download_file(bucket, remote_path,file_name)
    os.system(f'unzip {file_name} -d {file_name.split(".zip")[0]}')
    os.system(f'rm {file_name}r ')
    os.chdir(start_dir)
