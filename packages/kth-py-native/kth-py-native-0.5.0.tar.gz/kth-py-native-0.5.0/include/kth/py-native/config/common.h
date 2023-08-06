#ifndef KTH_PY_NATIVE_CONFIG_COMMON_H_
#define KTH_PY_NATIVE_CONFIG_COMMON_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <kth/capi/platform.h>

#define KTH_PY_GETATTR(to, from, var, fmt) PyArg_ParseTuple(Py_BuildValue("(O)", PyObject_GetAttrString(from, #var)), fmt, &to.var)

#ifdef __cplusplus
extern "C" {
#endif

inline
char** config_strings_to_c(PyObject* setts, size_t* out_size) {
    size_t const n = PyList_Size(setts);
    *out_size = n;
    char** buffer = kth_platform_allocate_array_of_strings(*out_size);
    for (size_t i = 0; i < n; ++i) {
        PyObject* str_py = PyList_GetItem(setts, i);

        char const* str;
        if ( ! PyArg_ParseTuple(Py_BuildValue("(O)", str_py), "s", &str)) {
            return NULL;
        }

        kth_platform_allocate_and_copy_string_at(buffer, i, str);
    }
    return buffer;
}

#ifdef __cplusplus
} //extern "C"
#endif

#endif // KTH_PY_NATIVE_CONFIG_COMMON_H_


