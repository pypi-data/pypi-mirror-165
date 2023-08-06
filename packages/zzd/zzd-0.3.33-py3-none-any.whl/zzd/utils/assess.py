import numpy as np
from sklearn import metrics
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import pandas as pd
#(1) scores
def multi_scores(y_true:int, y_pred:float, threshold=0.5, show=False, show_index=True,abbr=True):
    """
    y_true:true label
    y_prob:pred label with probility
    threshold:Negative if y_pred < threshold, positive if y_pred > threshold.

    multi scores of binnary class:
    (1) first layer score
        TP : true positive
        TN : true negative
        FP : false positive
        FN : false engative

    (2) second layer score
        precision   = TP/(TP+FP)
        recall      = TP/(TP+FN)   
        sensitivity = TP/(TP+FN)   
        specificity = TN/(TN+FP)
        Accuracy    = (TP+TN)/(TP+TN+FP+FN)  

    (3) third layer score
         mcc = (TP*TN - FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
         f1 = 2*(precision*recall)/(precision+recall)

    (4) area score
        auc : Area under the curve of ROC(receipt operator curve) 
        auprc:Area under the precision recall curve
        ap:   Average precision-recall score

    more info:
        TPR = TP/(TP+FN) :true positive rate 
        TNR = TN/(TN+FP) :true negative rate
        FPR = FP/(TN+FP) :false positive rate
        FNR = FN/(TP+FN) :false negative rate

        PPV = TP/(TP+FP):positive predictive value
        NPV = TN/(TN+FN):negative predictive value
 
        PPV=precision
        TPR=Recall=sensitivity
        TNR=specificity

    example:

    test = scores(
            y_true = [0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1  ],
            y_pred = [0., 0.2, 0.4, 0.6, 0.8, 1., 0., 0.2, 0.4, 0.6, 0.8, 1],show=True)

    """
    y_true = np.array(y_true,float).ravel()
    y_pred = np.array(y_pred,float).ravel()

    if max(y_true) > 1 or min(y_true)< 0 :
        raise Exception("label not in range (0, 1)!")
    
    if max(y_pred) > 1 or min(y_pred) <0:
        raise Exception("y_prob value not in range (0, 1)!")

    y_true_label = np.round(y_true)
    y_pred_label = np.round(y_pred)
    
    TP = sum((y_true >  threshold) & (y_pred >  threshold ))
    TN = sum((y_true <= threshold) & (y_pred <= threshold ))
    FP = sum((y_true <= threshold) & (y_pred >  threshold ))
    FN = sum((y_true >  threshold) & (y_pred <= threshold ))
    
    #precision =     np.round(metrics.precision_score(y_true_label, y_pred_label),5)
    #recall =        np.round(metrics.recall_score(y_true_label, y_pred_label),5)
    #specificity =   np.round(TN/(TN+FP+1e-6),5)
    PPV = np.round(metrics.precision_score(y_true_label, y_pred_label),5)
    TPR = np.round(metrics.recall_score(y_true_label, y_pred_label),5)
    TNR = np.round(TN/(TN+FP+1e-6),5)
    
    acc =      np.round(metrics.accuracy_score(y_true_label, y_pred_label),5)
    mcc =           np.round(metrics.matthews_corrcoef(y_true_label, y_pred_label),5)
    f1 =            np.round(metrics.f1_score(y_true_label, y_pred_label),5)
    
    precisions, recalls,_ = metrics.precision_recall_curve(y_true, y_pred)
    auroc =         np.round(metrics.roc_auc_score(y_true, y_pred),5)
    auprc =         np.round(metrics.auc(recalls, precisions),5)
    ap =            np.round(metrics.average_precision_score(y_true, y_pred),5)
    
    scores = (TP, TN, FP, FN, PPV, TPR, TNR, acc, mcc, f1, auroc, auprc, ap)
    
    np.set_printoptions(suppress=True)
    if show:
        if not  abbr and show_index:
            print("TP\tTN\tFP\tFN\tprecision\trecall\tspecificity\taccuracy\tmcc\tf1-score\tAUROC\tAUPRC\tAP")
        elif abbr and show_index:
            print("TP\tTN\tFP\tFN\tPPV\tTPR\tTNR\tAcc\tmcc\tf1\tAUROC\tAUPRC\tAP")
        print("\t".join([str(_) for _ in scores]))
    return scores

def mean_accuray(y_true,y_pred):
	y_true = np.array(y_true,float)
	y_pred = np.array(y_pred,float)
    
	if max(y_true) > 1 or min(y_true)< 0 :
		raise Exception("label not in range (0, 1)!")
    
	if max(y_pred) > 1 or min(y_pred) <0:
		raise Exception("y_prob value not in range (0, 1)!")
    
	y_true_label = np.round(y_true)
	y_pred_label = np.round(y_pred)
	accuracy =      np.round(metrics.accuracy_score(y_true_label, y_pred_label),5)
	return accuracy

##########################
#(1) plot curve of roc and prc

def roc_curve(data_list,labels=None,title=None,colors=None,save_file=False):
    """
    data_list:list of k array with shape(n_example,2) or two columns(y_trues,y_preds).
    """
    #empty plot
    _, ax = plt.subplots(1, 1, figsize=(8, 6)) 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=18)
    ax.set_xlabel("FPR", fontdict={"fontsize": 18})
    ax.set_ylabel("TPR", fontdict={"fontsize": 18})
    ax.set_title(title if title else "ROC Curve", fontdict={"fontsize": 15}, y=1.05)
    
    
    #compute
    rank = {score:index for index,score in enumerate([metrics.roc_auc_score(i[:,0],i[:,1]) for i in data_list])}
    for score ,index_i in sorted(rank.items(),reverse=True):
        y_true,y_pred = data_list[index_i][:,0], data_list[index_i][:,1]
        auc_score = metrics.roc_auc_score(y_true,y_pred)
        fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
        ax.plot(fpr, tpr, 
            label=f"{labels[index_i]}:{auc_score:.3f}" if labels else f"{auc_score:.3f}" ,
            color = colors[index_i] if colors else None, 
            linewidth=2.0)  
    plt.legend(fontsize=15, shadow=False, framealpha=0 )
    plt.savefig(save_file, dpi=600) if save_file else None
    plt.show()    
        
        
def pr_curve(data_list,labels=None,title=None,colors=None,save_file=False):
    """
    data_list:list of k array with shape(n_example,2) or two columns(y_trues,y_preds).
    """
    #empty plot
    _, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=18)
    ax.set_xlabel("Recall", fontdict={"fontsize": 18})
    ax.set_ylabel("Precision", fontdict={"fontsize": 18})
    ax.set_title(label=title if title else "PR Curve", fontdict={"fontsize": 15}, y=1.05)
    
    #compute
    def auprc(y_true,y_pred):
        precision, recall, _ = metrics.precision_recall_curve(y_true, y_pred)
        return metrics.auc(recall, precision)
        
    rank = {score:index for index,score in enumerate([auprc(i[:,0],i[:,1]) for i in data_list])}
    for score ,index_i in sorted(rank.items(),reverse=True):
        y_true,y_pred = data_list[index_i][:,0], data_list[index_i][:,1]
        precision, recall, _ = metrics.precision_recall_curve(y_true, y_pred)
        auprc_socre = metrics.auc(recall, precision)
        
        ax.plot(recall, 
            precision, 
            label = f"{labels[index_i]}:{auprc_socre:.3f}" if labels else f"{auprc_socre:.3f}",
            color = colors[index_i] if colors else None ,
            linewidth=2.0)
        
    plt.legend(fontsize=15, shadow=False, framealpha=0 )
    plt.savefig(save_file, dpi=600) if save_file else None
    plt.show()   




def roc_curve_kfold(data_list,labels=None,title=None,colors=None,save_file=False,alpha=0.1):
    """
    data_list:list of fold_list that contain k array with shape(n_example,2) or two column(y_trues,y_pred)
    """
    #empty plot
    _, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=18)
    ax.set_xlabel("FPR", fontdict={"fontsize": 18})
    ax.set_ylabel("TPR", fontdict={"fontsize": 18})
    ax.set_title(label=title if title else "ROC Curve", fontdict={"fontsize": 15}, y=1.05)
    default_color=['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

    #(1) rank
    score_index_ranked = sorted(zip( [np.mean([metrics.roc_auc_score(j[:,0],j[:,1])for j in i]) for i in data_list], np.arange(len(data_list))) ,reverse=True)
    index_ranked =  [i[1] for i in score_index_ranked]  

    for rank_i in index_ranked:
        fold_list = data_list[rank_i]

        auroc_score_list = []
        fpr_list= []
        tpr_list = []
        for sub_arr in fold_list:
            y_true = sub_arr[:,0]
            y_pred = sub_arr[:,1]
            fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
            auroc_score = metrics.roc_auc_score(y_true,y_pred)
            fpr_list.append(fpr)
            tpr_list.append(tpr)
            auroc_score_list.append(auroc_score)

        x_tick = fpr_list[np.argmax([len(i) for i in fpr_list])]
        y_ticks = np.zeros((len(fold_list), len(x_tick)))
        for i in range(len(fold_list)):
            for idx_j,j in enumerate(x_tick):
                y_ticks[i][idx_j] = np.interp(j,fpr_list[i], tpr_list[i]) #insert_value(j,fpr_list[i], tpr_list[i])

        #plot
        ax.plot(x_tick,
                y_ticks.mean(0),
                label = f"{labels[rank_i]} {np.mean(auroc_score_list):.3f}±{np.std(auroc_score_list):.3f}"
                        if labels else f"{np.mean(auroc_score_list):.3f}±{np.std(auroc_score_list):.3f}",
                color = colors[rank_i] if colors else default_color[rank_i])

        ax.fill_between(x_tick,
            y_ticks.mean(0)+y_ticks.std(0),
            y_ticks.mean(0)-y_ticks.std(0),
            facecolor=colors[rank_i] if colors else default_color[rank_i],
            alpha=alpha)

    plt.legend(fontsize=15, shadow=False, framealpha=0 )
    plt.savefig(save_file, dpi=600) if save_file else None
    plt.show()

    
def pr_curve_kfold(data_list,labels=None,title=None,colors=None,save_file=False,alpha=0.1):
    """
    data_list:list of fold_list that contain k array with shape(n_example,2) or two column(y_trues,y_pred)
    """
    #empty plot
    _, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.tick_params(labelsize=18)
    ax.set_xlabel("Recall", fontdict={"fontsize": 18})
    ax.set_ylabel("Precision", fontdict={"fontsize": 18})
    ax.set_title(label=title if title else "PR Curve", fontdict={"fontsize": 15}, y=1.05)
    default_color=['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

    #compute
    def auprc(ta):
        precision, recall, _ = metrics.precision_recall_curve(ta[:,0], ta[:,1])
        return metrics.auc(recall, precision)

    #(1) rank
    score_index_ranked = sorted(zip( [np.mean([auprc(j) for j in i]) for i in data_list], np.arange(len(data_list))) ,reverse=True)
    index_ranked =  [i[1] for i in score_index_ranked]  
    
    #(3) compute y lim of precision
    for rank_i  in index_ranked:
        
        fold_list = data_list[rank_i]
        auprc_score_list = []
        precision_list = []
        recall_list = []
        
        for sub_arr in fold_list:
            y_true = sub_arr[:,0]
            y_pred = sub_arr[:,1]
            precision, recall, _ = metrics.precision_recall_curve(y_true, y_pred)
            auprc_score = metrics.auc(recall, precision)

            precision_list.append(precision)
            recall_list.append(recall)
            auprc_score_list.append(auprc_score)
        
        x_tick = recall_list[np.argmax([len(i) for i in precision_list])]
        y_ticks = np.zeros((len(fold_list),len(x_tick)))
        for i_fold in range(len(fold_list)):
            for idx_j,j in enumerate(x_tick):
                if idx_j == 0.:
                    y_ticks[i_fold][idx_j] = 0
                elif idx_j == len(x_tick)-1.:
                    y_ticks[i_fold][idx_j] = 1.
                else:
                    y_ticks[i_fold][idx_j] = np.interp(j, precision_list[i_fold], recall_list[i_fold])
        #plot
        ax.plot(x_tick,
                y_ticks.mean(0),
                label = f"{labels[rank_i]} {np.mean(auprc_score_list):.3f}±{np.std(auprc_score_list):.3f}"
                        if labels else f"{np.mean(auprc_score_list):.3f}±{np.std(auprc_score_list):.3f}",
                color = colors[rank_i-1] if colors else default_color[rank_i])

        ax.fill_between(x_tick,
            y_ticks.mean(0)+y_ticks.std(0),
            y_ticks.mean(0)-y_ticks.std(0),
            facecolor=colors[rank_i-1] if colors else default_color[rank_i],
            alpha=alpha)

    plt.legend(fontsize=15, shadow=False, framealpha=0 )
    plt.savefig(save_file, dpi=600) if save_file else None
    plt.show()
    







if __name__ == "__main__":
    test = multi_scores(
            [0,   0,   0,   0,   0,   0,   1,   1,   1,   1,   1,   1  ],
            [0.001, 0.2, 0.4, 0.6, 0.8, 0.999, 0.001, 0.2, 0.4, 0.6, 0.8, 0.999],show=True)
    #TP,TN,FP,FN, precision, recall, sensitivity, specificity, accuracy, mcc, f1, auroc, auprc,ap = test
    #print(f"TP, TN, FP, FN: {TP}\t{TN}\t{FP}\t{FN}")
    #print(f"precision, recall,sensitivity, specificity: {precision}\t{recall}\t{sensitivity}\t{specificity}")
    #print(f"accuracy, mcc, f1: {accuracy}\t{mcc}\t{f1}" )
    #print(f"auroc, auprc, ap: {auroc}\t{auprc}\t{ap}")

