import pytest
import numpy as np
from pysimrel.utilities import *

@pytest.fixture
def rotation_matrix():
    n_pred = 10
    n_relpred = [5, 3]
    pos_relcomp = [[0, 1, 2], [3, 4]]
    rel_irrel = get_relpred(n_pred, n_relpred, pos_relcomp)
    rot_mat = get_rotation(rel_irrel)
    return n_pred, n_relpred, pos_relcomp, rel_irrel, rot_mat
    
def test_rotmat_shape(rotation_matrix):
    p, relpred, relcomp, rel_irrel, rot_mat = rotation_matrix
    rel = [x for y in rel_irrel['rel'] for x  in y]
    irrel = list(rel_irrel['irrel'])
    assert rot_mat.shape == (p, p)

def test_rotmat_properties(rotation_matrix):
   p, relpred, relcomp, rel_irrel, rot_mat = rotation_matrix
   AtA = np.dot(rot_mat.T, rot_mat)
   AAt = np.dot(rot_mat, rot_mat.T)
   eye = np.eye(rot_mat.shape[0])
   # Test if Square
   assert rot_mat.shape[0] == rot_mat.shape[1]
   # Test if Orthogonal
   assert np.allclose(AtA, eye, atol=1e-15, rtol=1e-15)
   assert np.allclose(AAt, eye, atol=1e-15, rtol=1e-15)

def test_rotmat_values(rotation_matrix):
    p, relpred, relcomp, rel_irrel, rot_mat = rotation_matrix
    rel = [x for y in rel_irrel['rel'] for x  in y]
    irrel = list(rel_irrel['irrel'])
    assert np.all(rot_mat[irrel][:,rel] == 0)
    assert np.all(rot_mat[rel][:,irrel] == 0)