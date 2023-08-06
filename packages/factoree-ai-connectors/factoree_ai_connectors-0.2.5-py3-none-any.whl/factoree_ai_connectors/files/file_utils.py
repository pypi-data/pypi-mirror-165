from datetime import datetime


def get_silver_file_name(
        data_type: str,
        facility: str,
        sensor_type: str,
        first_sample: datetime,
        last_sample: datetime
) -> str:
    file_base_name = f'{facility}-{sensor_type}'
    first_sample_display = first_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    last_sample_display = last_sample.strftime("%Y_%m_%dT%H_%M_%S%z").replace("+", "_")
    return f'input/{data_type}/{file_base_name}.{first_sample_display}-{last_sample_display}.json'
