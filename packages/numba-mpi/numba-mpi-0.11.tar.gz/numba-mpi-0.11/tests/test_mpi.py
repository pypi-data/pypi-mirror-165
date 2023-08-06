# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring
from mpi4py.MPI import COMM_WORLD
import numpy as np
import pytest
import numba_mpi as mpi


class TestMPI:

    data_types = [
        int, np.int32, np.int64,
        float, np.float64, np.double,
        complex, np.complex64, np.complex128
    ]

    @staticmethod
    @pytest.mark.parametrize("sut", [mpi.initialized, mpi.initialized.py_func])
    def test_init(sut):
        assert sut()

    @staticmethod
    @pytest.mark.parametrize("sut", [mpi.size, mpi.size.py_func])
    def test_size(sut):
        size = sut()
        assert size == COMM_WORLD.Get_size()

    @staticmethod
    @pytest.mark.parametrize("sut", [mpi.rank, mpi.rank.py_func])
    def test_rank(sut):
        rank = sut()
        assert rank == COMM_WORLD.Get_rank()

    @staticmethod
    @pytest.mark.parametrize("snd, rcv", [
        (mpi.send, mpi.recv),
        (mpi.send.py_func, mpi.recv.py_func)
    ])
    @pytest.mark.parametrize("fortran_order", [True, False])
    @pytest.mark.parametrize("data_type", data_types)
    def test_send_recv(snd, rcv, fortran_order, data_type):
        rng = np.random.default_rng(0)
        if np.issubdtype(data_type, np.complexfloating):
            src = rng.random((3, 3)) + rng.random((3, 3)) * 1j
        elif np.issubdtype(data_type, np.integer):
            src = rng.integers(0, 10, size=(3, 3))
        else:
            src = rng.random((3, 3))

        if fortran_order:
            src = np.asfortranarray(src, dtype=data_type)
        else:
            src = src.astype(dtype=data_type)

        dst_exp = np.empty_like(src)
        dst_tst = np.empty_like(src)

        if mpi.rank() == 0:
            snd(src, dest=1, tag=11)
            COMM_WORLD.Send(src, dest=1, tag=22)
        elif mpi.rank() == 1:
            rcv(dst_tst, source=0, tag=11)
            COMM_WORLD.Recv(dst_exp, source=0, tag=22)

            np.testing.assert_equal(dst_tst, src)
            np.testing.assert_equal(dst_exp, src)

    @staticmethod
    @pytest.mark.parametrize("snd, rcv", [
        (mpi.send, mpi.recv),
        (mpi.send.py_func, mpi.recv.py_func)
    ])
    @pytest.mark.parametrize("data_type", data_types)
    def test_send_recv_noncontiguous(snd, rcv, data_type):
        src = np.array([1, 2, 3, 4, 5], dtype=data_type)
        dst_tst = np.zeros_like(src)

        if mpi.rank() == 0:
            snd(src[::2], dest=1, tag=11)
        elif mpi.rank() == 1:
            rcv(dst_tst[::2], source=0, tag=11)

            np.testing.assert_equal(dst_tst[1::2], 0)
            np.testing.assert_equal(dst_tst[::2], src[::2])

    @staticmethod
    @pytest.mark.parametrize("snd, rcv", [
        (mpi.send, mpi.recv),
        (mpi.send.py_func, mpi.recv.py_func)
    ])
    @pytest.mark.parametrize("data_type", data_types)
    def test_send_0d_arrays(snd, rcv, data_type):
        src = np.array(1, dtype=data_type)
        dst_tst = np.empty_like(src)

        if mpi.rank() == 0:
            snd(src, dest=1, tag=11)
        elif mpi.rank() == 1:
            rcv(dst_tst, source=0, tag=11)

            np.testing.assert_equal(dst_tst, src)
