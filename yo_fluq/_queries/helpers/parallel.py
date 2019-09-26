from multiprocessing import Process, Queue, Pipe, Pool
from ..._common import ForkContext


class _QueueEnd:
    pass


class _QueueAsIterable:
    def __init__(self, queue: Queue):
        self.queue = queue

    def __iter__(self):
        while(True): # actually covered, but not recognized due to being executed in anoher process # pragma: no cover
            e = self.queue.get()
            if isinstance(e,_QueueEnd):
                break
            yield e




def _fork_process(selector, fork_enum, context, pipe): # actually covered, but not recognized due to being executed in anoher process # pragma: no cover
    result = selector(fork_enum,context)
    pipe.send(context)
    pipe.send(result)



def fork(en, context, selector):
    queue = Queue()
    fork_enum = _QueueAsIterable(queue)
    parent_conn, child_conn = Pipe()
    process = Process(target=_fork_process, args=(selector, fork_enum, context.sent, child_conn))
    process.start()
    for e in en:
        queue.put(e)
        yield e
    queue.put(_QueueEnd())
    context.received = parent_conn.recv()
    context.result = parent_conn.recv()
    process.join()


def parallel_select(q,selector, workers_count, buffer_size):
    pool = Pool(workers_count)
    for r in pool.imap(selector,q, buffer_size):
        yield r
    pool.close()