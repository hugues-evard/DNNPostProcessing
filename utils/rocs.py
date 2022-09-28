import ROOT
from collections import OrderedDict
from plotting_utils import GetROC, PlotGraphs

def CompareROCS_sig_bkg():
    graphs = OrderedDict()
    path = '/afs/cern.ch/work/a/anmalara/WorkingArea/DNN/weaver-benchmark/condor/test/output/'
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new')
    graphs[graph] = {'color': ROOT.kRed+1, 'legendtext': 'sig-sig', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_bkg', y_score = 'score_is_bkg')
    graphs[graph] = {'color': ROOT.kBlue+1, 'legendtext': 'bkg-bkg', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_bkg')
    graphs[graph] = {'color': ROOT.kOrange+1, 'legendtext': 'sig-bkg', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_bkg', y_score = 'score_is_signal_new')
    graphs[graph] = {'color': ROOT.kGreen+1, 'legendtext': 'bkg-sig', 'auc': auc, 'acc': acc}

    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new', swap=True)
    graphs[graph] = {'lstyle':ROOT.kDashed, 'color': ROOT.kRed+1, 'legendtext': 'sig-sig-swap', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_bkg', y_score = 'score_is_bkg', swap=True)
    graphs[graph] = {'lstyle':ROOT.kDashed, 'color': ROOT.kBlue+1, 'legendtext': 'bkg-bkg-swap', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_bkg', swap=True)
    graphs[graph] = {'lstyle':ROOT.kDashed, 'color': ROOT.kOrange+1, 'legendtext': 'sig-bkg-swap', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_bkg', y_score = 'score_is_signal_new', swap=True)
    graphs[graph] = {'lstyle':ROOT.kDashed, 'color': ROOT.kGreen+1, 'legendtext': 'bkg-sig-swap', 'auc': auc, 'acc': acc}
    PlotGraphs(graphs, pdfname='ROCs_sig_bkg')

def CompareROCS():
    graphs = OrderedDict()
    path = '/afs/cern.ch/work/a/anmalara/WorkingArea/DNN/weaver-benchmark/condor/output/'
    graph,auc,acc = GetROC(fname=path+'mlp_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new')
    graphs[graph] = {'color': ROOT.kRed+1, 'legendtext': 'mlp', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new')
    graphs[graph] = {'color': ROOT.kOrange+1, 'legendtext': 'deepAK8', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'particlenet_predict.root', treename='Events', y_true = 'is_signal_new', y_score = 'score_is_signal_new')
    graphs[graph] = {'color': ROOT.kAzure+2, 'legendtext': 'PN', 'auc': auc, 'acc': acc}
    PlotGraphs(graphs)


def main():
    CompareROCS()

if __name__ == '__main__':
    main()
