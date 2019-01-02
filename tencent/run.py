from .tencent import Tencent
from .pipelines import TencentPipeline

def run():
    TencentPipeline().open_spider()
    Tencent().first_requests()
    for item in Tencent().second_requests():
        TencentPipeline().process_item(item)
        TencentPipeline().upload_item(item)
        TencentPipeline().close_spider()

run()
