def get_sqs_url(aws_account_number: str, region_name: str, s3_bucket: str, folder: str = 'input') -> str:
    return f'https://sqs.{region_name}.amazonaws.com/{str(aws_account_number)}/{s3_bucket}_{folder}_notifications'


def get_multi_bucket_sqs_url(
        aws_account_number: str,
        region_name: str,
        environment: str,
        sub_component: str,
        folder: str = 'input'
) -> str:
    suffix = f'{environment}-etl-{sub_component}_{folder}_notifications'
    return f'https://sqs.{region_name}.amazonaws.com/{str(aws_account_number)}/{suffix}'
