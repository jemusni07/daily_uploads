import boto3
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION', 'us-east-1')
)

def upload_today_files(local_folder, bucket_name, prefix):
    """
    Upload CSV files for today's date only
    """
    today = datetime.now().strftime('%Y-%m-%d')
    logger.info(f"Looking for files with date: {today}")
    
    files_found = False
    for filename in os.listdir(local_folder):
        if filename.endswith('.csv') and filename.startswith(today):
            files_found = True
            # Extract date from filename (everything before the first underscore)
            date_part = filename.split('_')[0]
            s3_key = f"{prefix}/{date_part}/{filename}"
            local_path = os.path.join(local_folder, filename)
            
            logger.info(f"Processing file: {filename}")
            
            with open(local_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            try:
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=file_content
                )
                logger.info(f"Successfully uploaded {filename} to {s3_key}")
            except Exception as e:
                logger.error(f"Error uploading {filename}: {str(e)}")
    
    if not files_found:
        logger.warning(f"No files found for today's date: {today}")

def main():
    local_folder = 'daily_data'
    bucket_name = 'raw-retail-jmusni'
    prefix = 'daily_sales'
    
    logger.info("Starting automated upload for today's files...")
    upload_today_files(local_folder, bucket_name, prefix)
    logger.info("Upload process completed!")

if __name__ == "__main__":
    main() 