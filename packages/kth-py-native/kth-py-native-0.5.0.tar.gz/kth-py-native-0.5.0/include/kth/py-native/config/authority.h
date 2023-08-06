#ifndef KTH_PY_NATIVE_CONFIG_AUTHORITY_H_
#define KTH_PY_NATIVE_CONFIG_AUTHORITY_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/py-native/config/common.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    PyObject* ip;             // char*
    uint16_t port;
} Authority;

static PyMemberDef Authority_members[] = {
    {"ip", T_OBJECT_EX, offsetof(Authority, ip), 0, "ip"},
    {"port", T_UINT, offsetof(Authority, port), 0, "port"},
    {NULL}  /* Sentinel */
};

inline
kth_authority config_authority_to_c(PyObject* setts) {
    kth_authority res;
    KTH_PY_GETATTR(res, setts, ip, "s");
    KTH_PY_GETATTR(res, setts, port, "i");
    return res;
}

inline
kth_authority* config_authorities_to_c(PyObject* setts, size_t* out_size) {
    size_t const n = PyList_Size(setts);
    *out_size = n;
    kth_authority* res = kth_config_authority_allocate_n(*out_size);
    kth_authority* it = res;
    for (size_t i = 0; i < n; ++i) {
        *it = config_authority_to_c(PyList_GetItem(setts, i));
        ++it;
    }
    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_AUTHORITY_H_
