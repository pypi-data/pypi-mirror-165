#ifndef KTH_PY_NATIVE_CONFIG_CHECKPOINT_H_
#define KTH_PY_NATIVE_CONFIG_CHECKPOINT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/common.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    PyObject* hash;        // kth_hash_t
    uint64_t height;       // size_t
} Checkpoint;

static PyMemberDef Checkpoint_members[] = {
    {"hash", T_OBJECT_EX, offsetof(Checkpoint, hash), 0, "hash"},
    {"height", T_ULONGLONG, offsetof(Checkpoint, height), 0, "height"},
    {NULL}  /* Sentinel */
};

inline
kth_checkpoint config_checkpoint_to_c(PyObject* setts) {
    kth_checkpoint res;
    Py_ssize_t py_size;

    PyArg_ParseTuple(
        Py_BuildValue("(O)", PyObject_GetAttrString(setts, "hash"))
        , "y#", &res.hash.hash, &py_size);

    KTH_PY_GETATTR(res, setts, height, "i");
    return res;
}

inline
kth_checkpoint* config_checkpoints_to_c(PyObject* setts, kth_size_t* out_size) {
    size_t const n = PyList_Size(setts);
    *out_size = n;
    kth_checkpoint* res = kth_config_checkpoint_allocate_n(*out_size);
    kth_checkpoint* it = res;
    for (size_t i = 0; i < n; ++i) {
        *it = config_checkpoint_to_c(PyList_GetItem(setts, i));
        ++it;
    }
    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_CHECKPOINT_H_
