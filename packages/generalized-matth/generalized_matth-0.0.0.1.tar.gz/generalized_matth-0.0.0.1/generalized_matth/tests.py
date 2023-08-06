import numpy as np

from sklearn.utils._testing import assert_almost_equal
from sklearn.utils._testing import assert_array_almost_equal
from matthew_Coef_MultiClass.matt_funct import generalized_matthew,matthew_multiclass

# y_true = [0] * 13 + [1] * 21 + [2] * 20
# y_pred = [0] * 5 + [1] * 6 + [2] * 2 + [0] * 2 + [1] * 8 + [2] * 11 + [0] * 8 + [1] * 2 + [2] * 10
# mm= matthew_multiclass(y_true,y_pred,avg_type=3)
# print (mm.main_matthew_mult_class())
# mm= matthew_multiclass(y_true,y_pred)
# print (mm.main_matthew_mult_class())
# y_true = [0] * 5 + [1] * 8 + [2] * 2 + [3] * 13
# mm= matthew_multiclass(y_true,y_true,avg_type=3)
# print (mm.main_matthew_mult_class())
#
# exit(11)
def test_general_matt():
    y_true = [0]*13+[1]*21+[2]*20
    y_pred = [0] * 5 + [1] * 6 + [2] * 2 + [0] * 2 + [1] * 8 + [2] * 11 + [0] * 8 + [1] * 2 + [2] * 10
    f1_correl = generalized_matthew(y_true, y_pred,ave_type="f1")

    assert_array_almost_equal(f1_correl, 0.413, decimal=3)
    mcc_score = generalized_matthew(y_true, y_pred)
    assert_array_almost_equal(mcc_score, 0.031, decimal=3)
    y_true = [0] * 5 + [1] * 8 + [2] * 2 + [3] * 13
    f1_unit = generalized_matthew(y_true, y_true, ave_type="f1")

    assert_array_almost_equal(f1_unit, 1.0, decimal=1)

    mc_unit = generalized_matthew(y_true, y_true)

    assert_array_almost_equal(mc_unit, 1.0, decimal=1)

#
def test_general_mat_against_numpy_corrcoef():
    rng = np.random.RandomState(0)
    y_true = rng.randint(0, 2, size=20)
    y_pred = rng.randint(0, 2, size=20)
    print (y_true)
    print (y_pred)
    assert_almost_equal(
        generalized_matthew(y_true, y_pred), np.corrcoef(y_true, y_pred)[0, 1], 10
    )
def test_general_matthews_corrcoef_multiclass():
    rng = np.random.RandomState(0)
    ord_a = ord("a")
    n_classes = 4
    y_true = [chr(ord_a + i) for i in rng.randint(0, n_classes, size=20)]

    # corrcoef of same vectors must be 1
    assert_almost_equal(generalized_matthew(y_true, y_true), 1.0)

    # with multiclass > 2 it is not possible to achieve -1
    y_true = [0, 0, 4, 4, 3, 3]
    y_pred_bad = [3, 3, 0, 0, 4, 4]
    assert_almost_equal(generalized_matthew(y_true, y_pred_bad), 0.0)

    # Maximizing false positives and negatives minimizes the MCC
    # The minimum will be different for depending on the input
    y_true = [0, 0, 1, 1, 2, 2]
    y_pred_min = [1, 1, 0, 0, 0, 0]
    assert_almost_equal(generalized_matthew(y_true, y_pred_min), 0.0)

    # Zero variance will result in an mcc of zero
    y_true = [0, 1, 2]
    y_pred = [3, 3, 3]
    assert_almost_equal(generalized_matthew(y_true, y_pred), 0.0)

    # Also for ground truth with zero variance
    y_true = [3, 3, 3]
    y_pred = [0, 1, 2]
    assert_almost_equal(generalized_matthew(y_true, y_pred), 0.0)

    # These two vectors have 0 correlation and hence mcc should be 0
    y_1 = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    y_2 = [1, 1, 1, 2, 2, 2, 0, 0, 0]
    assert_almost_equal(generalized_matthew(y_1, y_2), 0.0)

    # We can test that binary assumptions hold using the multiclass computation
    # by masking the weight of samples not in the first two classes

    # Masking the last label should let us get an MCC of -1
    y_true = [0, 0, 1, 1, 2]
    y_pred = [1, 1, 0, 0, 2]
    sample_weight = [1, 1, 1, 1, 0]
    assert_almost_equal(
        generalized_matthew(y_true, y_pred, sample_weight=sample_weight), 0.0
    )
