from tdrstyle import *
import tdrstyle as TDR

def list_to_tgraph(x, y):
    if not type(x) == type(y):
        raise ValueError('In \'list_to_tgraph(): Passed two objects of different type.\'')
    if not len(x) == len(y):
        raise ValueError('In \'list_to_tgraph(): Passed two lists with different length.\'')
    from array import array
    x = array('f', x)
    y = array('f', y)
    g = rt.TGraph(len(x), x, y)
    return g

def PlotGraphs(graphs={}, pdfname='ROCs', x_title='Signal efficiency', y_title='Background efficiency', x_range=(-0.1, 1.1), y_range=(1e-04, 1.2), logy=True, writeExtraText = True, extraText  = 'Simulation', extraText2 = 'Work in progress', lumi_text=''):
    TDR.writeExtraText = writeExtraText
    TDR.extraText = extraText
    TDR.extraText2 = extraText2
    TDR.cms_lumi_TeV = lumi_text

    canv = tdrCanvas('graphs', x_range[0], x_range[1], y_range[0], y_range[1], x_title, y_title, kSquare)

    if logy:
        # canv = tdrCanvas('ROCs', -0.1, 1.1, 1e-04, 1.2, x_title, y_title, kSquare)
        # leg = tdrLeg(0.40, 0.2, 0.89, 0.35, 0.03, 42, rt.kBlack)
        leg = tdrLeg(0.30, 0.15, 0.89, 0.15+0.03*(len(graphs)+1), 0.03, 42, rt.kBlack)
    else:
        # canv = tdrCanvas('ROCs', -0.1, 1.1, 0, 1.5, x_title, y_title, kSquare)
        leg = tdrLeg(0.30, 0.65, 0.95, 0.9, 0.035, 42, rt.kBlack)
    canv.SetLogy(logy)
    for graph, info in graphs.items():
        color = info['color'] if 'color' in info else rt.kRed
        lstyle = info['lstyle'] if 'lstyle' in info else rt.kSolid
        graph.SetLineWidth(2)
        tdrDraw(graph, 'L', mcolor=color, lcolor=color, lstyle=lstyle)
        legstring = info['legendtext']
        if 'auc' in info: legstring += ', AUC: %1.3f'%(info['auc'])
        if 'acc' in info: legstring += ', acc: %1.3f'%(info['acc'])
        leg.AddEntry(graph, legstring, 'l')
    canv.SaveAs(pdfname+'.pdf')
    canv.Close()

def GetROC(fname='mlp_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new', swap=False):
    from root_numpy import root2array, rec2array
    mymatrix = rec2array(root2array(filenames=fname, treename=treename, branches=[y_true,y_score]))
    import pandas as pd
    from array import array
    df = pd.DataFrame(mymatrix,columns=['y_true','y_score'])
    from sklearn.metrics import roc_curve, auc, accuracy_score
    acc = accuracy_score(df['y_true'].round().astype(int),df['y_score'].round().astype(int))
    fpr, tpr, thr = roc_curve(df['y_true'], df['y_score'])
    if swap: fpr, tpr = (tpr,fpr)
    auc = auc(fpr, tpr)
    graph = list_to_tgraph(tpr,fpr)
    return (graph,auc,acc)
