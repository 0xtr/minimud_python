from asyncio import Queue


class MessageQueue:
    queued = {}

    @staticmethod
    def initQueue(socket):
        MessageQueue.queued[socket] = Queue()

    @staticmethod
    def queue(player, data):
        MessageQueue.queued[player.socket].put(data)

    @staticmethod
    def queueMultiple(multiple):
        for player, data in multiple:
            MessageQueue.queued[player.socket].put(data)

    @staticmethod
    def hasPending():
        return len(MessageQueue.queued)
