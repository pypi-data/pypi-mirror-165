#ifndef KTH_PY_NATIVE_CONFIG_ENDPOINT_H_
#define KTH_PY_NATIVE_CONFIG_ENDPOINT_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    PyObject_HEAD
    PyObject* scheme;       // char*
    PyObject* host;         // char*
    uint16_t port;
} Endpoint;

static PyMemberDef Endpoint_members[] = {
    {"scheme", T_OBJECT_EX, offsetof(Endpoint, scheme), 0, "scheme"},
    {"host", T_OBJECT_EX, offsetof(Endpoint, host), 0, "host"},
    {"port", T_UINT, offsetof(Endpoint, port), 0, "port"},
    {NULL}  /* Sentinel */
};

inline
kth_endpoint config_endpoint_to_c(PyObject* setts) {
    kth_endpoint res;


    // auto res2 = PyObject_SetAttrString(obj, "scheme", Py_BuildValue("s", endpoint.scheme));
    //      res2 = PyObject_SetAttrString(obj, "host", Py_BuildValue("s", endpoint.host));
    //      res2 = KTH_PY_SETATTR(obj, endpoint, port, "i");

    KTH_PY_GETATTR(res, setts, scheme, "s");
    KTH_PY_GETATTR(res, setts, host, "s");
    KTH_PY_GETATTR(res, setts, port, "i");
    return res;
}

inline
kth_endpoint* config_endpoints_to_c(PyObject* setts, size_t* out_size) {
    size_t const n = PyList_Size(setts);
    *out_size = n;
    kth_endpoint* res = kth_config_endpoint_allocate_n(*out_size);
    kth_endpoint* it = res;
    for (size_t i = 0; i < n; ++i) {
        *it = config_endpoint_to_c(PyList_GetItem(setts, i));
        ++it;
    }
    return res;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_ENDPOINT_H_
