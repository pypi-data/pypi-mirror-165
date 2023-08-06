#ifndef KTH_PY_NATIVE_UTILS_H_
#define KTH_PY_NATIVE_UTILS_H_


#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <kth/capi.h>

#ifdef __cplusplus
extern "C" {
#endif

void* get_ptr(PyObject* obj);
kth_node_t cast_node(PyObject* obj);
int char2int(char input);
void hex2bin(const char* src, uint8_t* target);
PyObject* to_py_obj(void*);

// PyObject* to_py_str(char const* str, size_t n);
PyObject* to_py_str(char const* str);

// return Py_BuildValue("s#", blocks, out_n);

#ifdef __cplusplus
} //extern "C"
#endif

#endif
