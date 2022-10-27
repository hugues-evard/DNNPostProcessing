import os, ROOT
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

def PlotSingleROC(path, y_true, pdfname, fname='pred.root'):
    graphs = OrderedDict()
    graph,auc,acc = GetROC(fname=os.path.join(path,fname), treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kRed+1, 'legendtext': 'mlp', 'auc': auc, 'acc': acc}
    PlotGraphs(graphs,pdfname=pdfname)


def CompareROCS_VBF(pdfname,y_true):
    graphs = OrderedDict()
    path = '/afs/cern.ch/work/a/anmalara/WorkingArea/DNN/DNNPostProcessing/trainings/'
    graph,auc,acc = GetROC(fname=path+'mlp_pf/20221003-164214_mlp_pf_ranger_lr0.001_batch128/predict_output/pred.root', treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kRed+1, 'legendtext': 'mlp', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'deepak8_pf/20221003-164213_deepak8_pf_ranger_lr0.001_batch128/predict_output/pred.root', treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kOrange+1, 'legendtext': 'deepAK8', 'auc': auc, 'acc': acc}
    graph,auc,acc = GetROC(fname=path+'particlenet_pf/20221003-164212_particlenet_pf_ranger_lr0.001_batch128/predict_output/pred.root', treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kAzure+2, 'legendtext': 'PN', 'auc': auc, 'acc': acc}

    graph,auc,acc = GetROC(fname=path+'mlp_pf/20221003-225801_mlp_pf_ranger_lr0.001_batch128/predict_output/pred.root', treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kRed+1, 'lstyle':ROOT.kDashed, 'legendtext': 'mlp-partial', 'auc': auc, 'acc': acc}

    graph,auc,acc = GetROC(fname=path+'deepak8_pf/20221003-225651_deepak8_pf_ranger_lr0.001_batch128/predict_output/pred.root', treename='Events', y_true = y_true, y_score = 'score_'+y_true)
    graphs[graph] = {'color': ROOT.kOrange+1, 'lstyle':ROOT.kDashed, 'legendtext': 'deepAK8-partial', 'auc': auc, 'acc': acc}

    PlotGraphs(graphs,pdfname=pdfname)




def main():
    # CompareROCS()
    # path='/afs/cern.ch/work/a/anmalara/WorkingArea/DNN/DNNPostProcessing/weaver-benchmark/weaver/output/predict_output/'
    # PlotSingleROC(path=path, y_true='m_is_VBF', pdfname='test1')
    CompareROCS_VBF(y_true='m_is_VBF', pdfname='VBF_short')

if __name__ == '__main__':
    main()
