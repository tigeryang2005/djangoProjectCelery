from celery import Task, shared_task
import time
import random
import logging
logger = logging.getLogger('log')



class MyHookTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # print('on success')
        logger.info(f'task id:{task_id} , arg:{args} , retval:{retval}, successful !')
        # return super(MyHookTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print('on failure')
        logger.info(f'task id:{task_id} , arg:{args} , failed ! erros: {exc}')
        # return super(MyHookTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # print('on retry')
        logger.info(f'task id:{task_id} , arg:{args} , retry !  erros: {exc}')
        # return super(MyHookTask, self).after_return(task_id, args, kwargs, einfo)


# 在对应的task函数的装饰器中，通过 base=MyHookTask 指定
# @shared_task(base=MyHookTask, bind=True)
@shared_task(base=MyHookTask)
def add(x, y):
    try:
        n = random.randint(1, 5)
        time.sleep(n)
        # # task_id:{self.task_id},
        logger.info(f'任务延迟{n}秒')
        # raise Exception
    except Exception as e:
        # 出错每4秒尝试一次，总共尝试4次
        # self.retry(exc=e, countdown=4, max_retries=4)
        logger.error(str(e))
    return x + y
