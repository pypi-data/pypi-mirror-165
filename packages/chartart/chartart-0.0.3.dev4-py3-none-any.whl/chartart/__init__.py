from IPython import get_ipython
from .plot import Publish


def target_func(comm, open_msg):
    # comm is the kernel Comm instance
    # msg is the comm_open message

    # Register handler for later messages
    @comm.on_msg
    def _recv(msg):
        # Use msg['content']['data'] for the data in the message
        #comm.send({'echo': msg['content']['data']})
        Publish(msg['content']['data'])


try:
    get_ipython().kernel.comm_manager.register_target('my_comm_target', target_func)
except AttributeError:
    print('Comms with Jupyter frontend not established.')