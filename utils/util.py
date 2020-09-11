import matplotlib.pyplot as plt

""" Generic API
"""


def draw_acc_loss(START_EPOCH: int, END_EPOCH: int, train_acc: list, train_loss: list, test_acc: list, savedir: str):
    """
    Description: 
    ------------
        Draw pie according to the acc and loss;

    Output:
    -------
        Two pictures
            One of them shows the accuracy of train and test; the other shows the loss of train

    Problems:
    ---------
        The output pictures is not fine grained
    """
    X_axis = range(START_EPOCH, END_EPOCH)
    Y_acc = [train_acc, test_acc]
    Y_loss = train_loss

    plt.figure()
    if train_acc is not None and test_acc is not None:
        plt.plot(X_axis, Y_acc[0], '-', c='blue')
        plt.plot(X_axis, Y_acc[1], '-', c='green')
        plt.title('Accuracy vs. epoches')
        plt.ylabel('Accuracy')
        plt.legend(['Train', 'Test'])
        plt.savefig(savedir + "/accuracy.jpg")

    plt.figure()
    if Y_loss is not None:
        plt.plot(X_axis, Y_loss, '.-')
        plt.title('Train loss vs. epoches')
        plt.ylabel('Loss')
        plt.savefig(savedir + "/loss.jpg")
