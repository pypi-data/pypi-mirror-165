from ctypes import ArgumentError
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score


def error_decomposition(y_true, y_pred_train, y_pred_test, scoring_function, 
                        unavoidable_error=0.0, maximize=True):
    """
    Create a pandas dataframe of the error decomposition values

    @param: y_true - ground truth
    @type: array like
    @param: y_pred_train - predictions on training data
    @type: array like
    @param: y_true - predictions on test data
    @type: array like
    @param: scoring_function - a function that takes (y_true, y_pred) and returns a single float
    @type: func
    @param: unavoidable_error - error if our model is a good as possible under the circumstances
    @type: float
    @param: maximize - True if the model tries to Maximize the scoreing function, i.e. Accuracy
                        False otherwise, i.e. MSE
                        If Maximize, it is assumed that the score range is (0,1)
    @type: bool
    """
    if not hasattr(scoring_function, '__call__'):
        raise ArgumentError(f"Scoring function must be type function, but was {type(scoring_function)}")
    
    train_score = scoring_function(y_true, y_pred_train)
    test_score = scoring_function(y_true, y_pred_test)

    if maximize:
        if not ((0 <= train_score <= 1) and (0 <= test_score <= 1)):
            print("Warning: Scoring function output outside range (0,1)")
        errors = [unavoidable_error, 1 - train_score - unavoidable_error, 1 - train_score,
                  (1 - test_score) - (1 - train_score), 1 - test_score]
    else:
        errors = [unavoidable_error, train_score - unavoidable_error, train_score,
                  test_score - train_score, test_score]

    errors_types = ["unavoidable error", "underfitting", "train error", "overfitting ", "test error"]
    error_df = pd.DataFrame(errors, index=errors_types, columns=['value'])
    error_df['bottom'] = [0.0, errors[0], 0.0, errors[2], 0.0]
    
    return error_df


def plot_error_decomposition(y_true, y_pred_train, y_pred_test, scoring_function, unavoidable_error=0.0,
                             title="Error Decomposition"):
    """
    Plot error decomposition from pandas dataframe
    Designed for scoring metrics that scale between 0 -> 1

    @param: y_true - ground truth
    @type: array like
    @param: y_pred_train - predictions on training data
    @type: array like
    @param: y_true - predictions on test data
    @type: array like
    @param: scoring_function - a function that takes (y_true, y_pred) and returns a single float
    @type: func
    @param: unavoidable_error - error if our model is a good as possible under the circumstances
    @type: float
    """
    error_df = error_decomposition(y_true, y_pred_train, y_pred_test, scoring_function, unavoidable_error)
    fig, ax = plt.subplots()
    x_values = np.arange(error_df.shape[0])
    ax.set_xticks(x_values)
    ax.set_xticklabels(error_df.index, rotation=45)
    for i in range(error_df.shape[0]):
        value = error_df.iloc[i]['value']
        bottom = error_df.iloc[i]['bottom']
        label = f"{value:.2f}"
        # rect = ax.bar(x=x_values[i], height=value, bottom=bottom, width=0.5, label=label)
        ax.bar(x=x_values[i], height=value, bottom=bottom, width=0.5, label=label)
    ax.grid()
    ax.legend()
    ax.set_title(title)
    return fig


def plot_roc_curve(y_true, y_pred, title=None):
    """
    Convenience function for plotting roc curve

    @param: y_true - ground truth
    @type: array like
    @param: y_pred_train - predictions
    @type: array like

    """
    fpr, tpr, _ = roc_curve(y_true, y_pred.ravel())
    roc_auc = roc_auc_score(y_true, y_pred)
    fig, ax = plt.subplots()
    lw = 2
    ax.plot(fpr, tpr, color='darkorange',
            lw=lw, label='AUC = %0.9f' % roc_auc)
    ax.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.legend(loc="lower right")
    ax.grid()
    if title:
        ax.set_title(title)
    else:
        ax.set_title('ROC Curve')
    return fig


def plot_pr_curve(y_true, y_pred, title=None):
    """
    Convenience function for plotting precision recall curve

    @param: y_true - ground truth
    @type: array like
    @param: y_pred_train - predictions
    @type: array like
    """
    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    avg_precision = average_precision_score(y_true, y_pred)
    fig, ax = plt.subplots()
    lw = 2
    ax.plot(recall[::-1], precision[::-1], color='navy', lw=lw)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ax.axhline(y=avg_precision)
    if title:
        ax.set_title(title)
    else:
        ax.set_title('Precision - Recall Curve\nAvg Precision: {}'.format(avg_precision))
    ax.grid()
    return fig


def plot_prt_curve(y_true, y_pred, title=None):
    """
    Convenience function for plotting precision recall across thresholds

    @param: y_true - ground truth
    @type: array like
    @param: y_pred_train - predictions
    @type: array like
    """
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
    avg_precision = average_precision_score(y_true, y_pred)
    fig, ax = plt.subplots()
    lw = 2
    ax.plot(thresholds, precision[1:], color='darkorange', lw=lw, label='Precision')
    ax.plot(thresholds, recall[1:], color='navy', lw=lw, label='Recall')
    ax.grid()
    ax.legend()
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Precision - Recall')
    if title:
        ax.set_title(title)
    else:
        ax.set_title(
            f'Precision - Recall \nAvg Precision = {avg_precision}\nPositive Class Frequency = {np.mean(y_true)}')
    return fig