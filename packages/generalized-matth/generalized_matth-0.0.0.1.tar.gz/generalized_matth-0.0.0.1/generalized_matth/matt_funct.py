import numpy as np

from scipy import stats as st
from sklearn.metrics._classification import _check_targets,check_consistent_length,confusion_matrix
from sklearn.preprocessing._label import LabelEncoder
# An exterior function hopefully to be added to scikitlearn
from enum import Enum
class AVERAG_TYPE(Enum):
    MATTHEW_GEN = 2
    F1_GEN = 3

def generalized_matthew(y_true, y_pred,ave_type="matthew",sample_weight=None):
    """Compute the generalized Matthews coefficient.

    The gneneralized Matthews coefficieint is (as one may expected) a gnerlization of MCC for higher
    dimensions : namely multiclass problems. While in binary problems, errors have a natural defionions:
    False Postiove and Flase negative , this is not the status in multiclass problems. Morover these probelms can
    suffer from  imbalance data issues.
    For more theoretical details one can read check in the references below

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        Ground truth (correct) target values.

    y_pred : array, shape = [n_samples]
        Estimated targets as returned by a classifier.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

        .. versionadded:: 0.18

    ave_type : string that fan be either matthew (as the defalut) or "f1" I mainly detects whether we use
        harmoninc mean (f1) or geometric with determinant (Matthew)
    Returns
    -------
    generalized_score : float
        The genelaized Matthew score (+1 represents a perfect
        prediction, 0 an average random prediction and -1 and inverse
        prediction).

    References
    ----------
    .. [1] :Jafar Tanha et al. “Boosting methods for multi-class imbalanced
    data classification: an experimental review”. In: Journal of Big Data
    7.1 (2020), pp. 1–47

    .. [2] `Davide Chicco and Giuseppe Jurman. “The advantages of the Matthews
    correlation coefficient (MCC) over F1 score and accuracy in binary
    classification evaluation”. In: BMC genomics 21.1 (2020), pp. 1–13.
    15

    .. [3] `Cathy O’neil. Weapons of math destruction: How big data increases
    inequality and threatens democracy. Broadway Books, 2016.

    .. [4] `Nir Sharon and Uri Itai. “Approximation schemes for functions of
    positive-definite matrix values”. In: IMA Journal of Numerical Anal-
    ysis 33.4 (2013), pp. 1436–1468.

    .. [5] Brian W Matthews. “Comparison of the predicted and observed sec-
    ondary structure of T4 phage lysozyme”. In: Biochimica et Biophys-
    ica Acta (BBA)-Protein Structure 405.2 (1975), pp. 442–451.

    .. [6] Alan C Acock and Gordon R Stavig. “A measure of association for
    nonparametric statistics”. In: Social Forces 57.4 (1979), pp. 1381–
    1386


    Examples
       y_true = [0] * 13 + [1] * 21 + [2] * 20
       y_pred = [0] * 5 + [1] * 6 + [2] * 2 + [0] * 2 + [1] * 8 + [2] * 11 + [0] * 8 + [1] * 2 + [2] * 10
       print("gen   F1 ",
                   generalized_matthew(y_true, y_pred,ave_type=3))
       print("gen     ",
       .    generalized_matthew(y_true, y_pred))

       y_true= [0]*5+[1]*8+[2]*2+[3]*13
       print("gen   ",
          generalized_matthew(y_true, y_true ))
       print("gen f1 ",
          generalized_matthew(y_true, y_true, ave_type=3))

       Results
       gen  F1  0.41308089500860584
       gen     0.03132735561190867
       gen   1.0
       gen  F1  1.0
    """

    y_type, y_true, y_pred = _check_targets(y_true, y_pred)
    check_consistent_length(y_true, y_pred, sample_weight)
    if y_type not in {"binary", "multiclass"}:
        raise ValueError("%s is not supported" % y_type)

    lb = LabelEncoder()
    lb.fit(np.hstack([y_true, y_pred]))
    y_true = lb.transform(y_true)
    y_pred = lb.transform(y_pred)

    conf_m = confusion_matrix(y_true, y_pred, sample_weight=sample_weight)

    dimension_size = conf_m.shape[0]

    total_col = conf_m.sum(axis=1)
    total_row = conf_m.sum(axis=0)
    if min(min(total_row),min(total_col)) <= 0:
        return 0.0
    m1 = conf_m / conf_m.sum(axis=1)
    m2 = conf_m / conf_m.sum(axis=0)
    if ave_type == "f1":

        g_mat = [[st.mstats.hmean([m1[i, j], m2[j][i]])
            for i in range(dimension_size)] for j in range(dimension_size)]
        return st.mstats.hmean([g_mat[i][i] for i in range(dimension_size)])
    elif ave_type == "matthew":

        g_mat = [[st.mstats.gmean([m1[i, j]+0.000000001, m2[j,i]+0.00000000001])
            for i in range(dimension_size)] for j in range(dimension_size)]

        return np.linalg.det(g_mat)
    return 0.0


class matthew_multiclass:
    #Matthew - avg_type =2  (default)
    # F1 avh_type =3
    def __init__(self,y_true,y_pred,avg_type=AVERAG_TYPE.MATTHEW_GEN.value,sample_weight=None):
        # self.hm = st.mstats.hmean
        # self.gm = st.mstats.gmean
        self.conf_m  = confusion_matrix(y_true, y_pred, sample_weight=sample_weight)
        self.dimension_size = self.conf_m.shape[0]
        if avg_type == AVERAG_TYPE.MATTHEW_GEN.value:
            self.av_func = st.mstats.gmean
            self.scalar_op = np.linalg.det
        elif avg_type == AVERAG_TYPE.F1_GEN.value:
            self.av_func = st.mstats.hmean
            self.scalar_op = self.gen_f1_scalar_op
        return
    def gen_f1_scalar_op(self, h_conf_mat):
            l_mat = len(h_conf_mat)
            return st.mstats.hmean([h_conf_mat[i][i] for i in range(l_mat)])

    def norm_confusion_mat(self):

        m1 = self.conf_m / self.conf_m.sum( axis=1)
        m2 = self.conf_m / self.conf_m.sum( axis=0)
        return [[self.av_func([m1[i, j], m2[j,i]])
                 for i in range(self.dimension_size)] for j in range(self.dimension_size)]
    def main_matthew_mult_class(self):
        G_mat = self.norm_confusion_mat()
        return self.scalar_op(G_mat)


if __name__ =='__main__':

    y_true = [0] * 13 + [1] * 21 + [2] * 20
    y_pred = [0] * 5 + [1] * 6 + [2] * 2 + [0] * 2 + [1] * 8 + [2] * 11 + [0] * 8 + [1] * 2 + [2] * 10
    mm= matthew_multiclass(y_true,y_pred,avg_type=3)
    print (mm.main_matthew_mult_class())
    mm= matthew_multiclass(y_true,y_pred)
    print (mm.main_matthew_mult_class())
    y_true = [0] * 5 + [1] * 8 + [2] * 2 + [3] * 13
    mm= matthew_multiclass(y_true,y_true,avg_type=3)
    print (mm.main_matthew_mult_class())

