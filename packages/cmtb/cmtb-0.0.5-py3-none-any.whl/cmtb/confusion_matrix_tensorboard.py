import tensorflow as tf
from tensorflow import keras
import numpy as np
import sklearn.metrics
import io
import matplotlib.pyplot as plt
import os


class BalancedAccuracy(tf.keras.metrics.Metric):
    """
    Compute balanced accuracy score.
    Store a confusion matrix of prediction and true labels whenever calling reset_state().
    """

    def __init__(self, num_targets, cm_dir, name='bal_acc', **kwargs):
        super(BalancedAccuracy, self).__init__(name=name, **kwargs)
        self.num_targets = num_targets
        self.cm_dir = cm_dir
        self.count = 0
        self.cm = self.add_weight(name="cm_matrix", shape=[num_targets, num_targets], initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.cm.assign_add(self.compute_cm(y_true, y_pred))

    def result(self):
        balanced_acc = self.compute_balanced_acc()
        return balanced_acc

    def compute_cm(self, y_true, y_pred):
        labels = tf.math.argmax(y_true, axis=1)
        predictions = tf.math.argmax(y_pred, axis=1)
        current_cm = tf.math.confusion_matrix(labels=labels, predictions=predictions, dtype="float32",
                                              num_classes=self.num_targets)
        current_cm = tf.transpose(current_cm)
        return current_cm

    def compute_balanced_acc(self):
        diag = tf.linalg.diag_part(self.cm)
        col_sums = tf.math.reduce_sum(self.cm, axis=0)
        average_per_class = tf.math.divide(diag, col_sums)
        nan_index = tf.math.logical_not(tf.math.is_nan(average_per_class))
        average_per_class = tf.boolean_mask(average_per_class, nan_index)
        acc_sum = tf.math.reduce_sum(average_per_class)
        balanced_acc = tf.math.divide(acc_sum, tf.math.count_nonzero(col_sums, dtype=acc_sum.dtype))
        return balanced_acc

    def reset_state(self):
        self.store_cm()
        self.count = self.count + 1
        self.cm.assign_sub(self.cm)

    def store_cm(self):
        if self.count % 2 != 0:
            file_name = self.cm_dir.name + "/" + "cm_val_" + str(int(self.count / 2))
        else:
            file_name = self.cm_dir.name + "/" + "cm_train_" + str(int(self.count / 2))
        np.save(file_name, self.cm.numpy())


class ConfMatrixCb(tf.keras.callbacks.Callback):
    """
    Read confusion matrices from directory and write plot to tensorboard images.
    """

    def __init__(self, cm_dir, path_tensorboard, run_name, label_names, cm_display_percentage=True, plot_size=10):

        super(ConfMatrixCb, self).__init__()
        self.cm_dir = cm_dir
        self.path_tensorboard = path_tensorboard
        self.run_name = run_name
        self.label_names = label_names
        self.epoch = 0
        self.train_images = None
        self.val_images = None
        self.plot_size = plot_size
        self.cm_display_percentage = cm_display_percentage

    def on_epoch_begin(self, epoch, logs):

        if (epoch > 0):

            # load confusion matrix stored with BalancedAccuracy metric
            cm_train = np.load(self.cm_dir + "/cm_train_" + str(epoch - 1) + ".npy")
            cm_val = np.load(self.cm_dir + "/cm_val_" + str(epoch - 1) + ".npy")

            if (self.cm_display_percentage):
                cm_train = cm_count_to_perc(cm_train)
                cm_val = cm_count_to_perc(cm_val)

            fig, ax = plt.subplots(figsize=(self.plot_size, self.plot_size))
            cm_train_plot = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm_train,
                                                                   display_labels=self.label_names).plot(cmap="Blues", ax=ax)
            self.train_images = plot_to_image(cm_train_plot)

            fig, ax = plt.subplots(figsize=(self.plot_size, self.plot_size))
            cm_val_plot = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm_val,
                                                                 display_labels=self.label_names).plot(cmap="Blues", ax=ax)
            self.val_images = plot_to_image(cm_val_plot)

            file_writer = tf.summary.create_file_writer(self.path_tensorboard + "/" + self.run_name)
            file_writer.set_as_default()
            tf.summary.image(name="confusion matrix train", data=self.train_images, step=int(epoch - 1))
            tf.summary.image(name="confusion matrix validation", data=self.val_images, step=int(epoch - 1))
            file_writer.flush()
            self.epoch = epoch

    def on_train_end(self, logs):

        epoch = self.epoch
        cm_train = np.load(self.cm_dir + "/cm_train_" + str(epoch - 1) + ".npy")

        for i in range(len(self.model.metrics)):
            if (self.model.metrics[i].name == "bal_acc"):
                bal_acc_index = i
                break

        # create confusion matrix for last val step manually (storing cm when calling reset_state)
        self.model.metrics[bal_acc_index].reset_state()
        cm_val = np.load(self.cm_dir + "/cm_val_" + str(epoch - 1) + ".npy")

        if (self.cm_display_percentage):
            cm_train = cm_count_to_perc(cm_train)
            cm_val = cm_count_to_perc(cm_val)

        fig, ax = plt.subplots(figsize=(self.plot_size, self.plot_size))
        cm_train_plot = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm_train,
                                                               display_labels=self.label_names).plot(cmap="Blues", ax=ax)
        self.train_images = plot_to_image(cm_train_plot)

        fig, ax = plt.subplots(figsize=(self.plot_size, self.plot_size))
        cm_val_plot = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix=cm_val,
                                                             display_labels=self.label_names).plot(cmap="Blues", ax=ax)
        self.val_images = plot_to_image(cm_val_plot)

        file_writer = tf.summary.create_file_writer(self.path_tensorboard + "/" + self.run_name)
        file_writer.set_as_default()
        tf.summary.image(name="confusion matrix train", data=self.train_images, step=int(epoch))
        tf.summary.image(name="confusion matrix validation", data=self.val_images, step=int(epoch))
        file_writer.flush()


def cm_count_to_perc(cm):
    """
    Normalize confusion matrix by rows (true labels).
    """
    row_sum = np.sum(cm, axis=1)
    cm_perc = np.zeros(shape=cm.shape)
    for i in range(cm.shape[0]):
        if row_sum[i] != 0:
            cm_perc[i, :] = cm[i,] / row_sum[i, None]
    return cm_perc


# code from: https://www.tensorflow.org/tensorboard/image_summaries
def plot_to_image(figure):
    """Converts the matplotlib plot specified by 'figure' to a PNG image and
    returns it. The supplied figure is closed and inaccessible after this call."""
    # Save the plot to a PNG in memory.
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    image = tf.expand_dims(image, 0)
    return image
