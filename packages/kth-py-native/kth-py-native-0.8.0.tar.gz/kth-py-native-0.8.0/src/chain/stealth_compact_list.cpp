#include <kth/py-native/chain/stealth_compact_list.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif


/*
PyObject* kth_py_native_chain_stealth_compact_list_construct_default(PyObject* self, PyObject* args){
    kth_stealth_compact_list_t res = (kth_stealth_compact_list_t)chain_stealth_compact_list_construct_default();
    return to_py_obj(res);
}


PyObject* kth_py_native_chain_stealth_compact_list_push_back(PyObject* self, PyObject* args){
    PyObject* py_stealth_compact_list;
    PyObject* py_stealth_compact;

    if ( ! PyArg_ParseTuple(args, "OO", &py_stealth_compact_list, &py_stealth_compact)) {
        return NULL;
    }

    kth_stealth_compact_list_t list = (kth_stealth_compact_list_t)get_ptr(py_stealth_compact_list);
    kth_stealth_compact_t stealth_compact = (list)get_ptr(py_stealth_compact);
    kth_chain_stealth_compact_list_push_back(kth_stealth_compact_list, stealth_compact);
    Py_RETURN_NONE;
}
*/

PyObject* kth_py_native_chain_stealth_compact_list_destruct(PyObject* self, PyObject* args){
   PyObject* py_stealth_compact_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_stealth_compact_list)) {
        return NULL;
    }

    kth_stealth_compact_list_t list = (kth_stealth_compact_list_t)get_ptr(py_stealth_compact_list);
    kth_chain_stealth_compact_list_destruct(list);
    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_stealth_compact_list_count(PyObject* self, PyObject* args){
    PyObject* py_stealth_compact_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_stealth_compact_list)) {
        return NULL;
    }

    kth_stealth_compact_list_t list = (kth_stealth_compact_list_t)get_ptr(py_stealth_compact_list);
    uint64_t res = kth_chain_stealth_compact_list_count(list);
    return Py_BuildValue("K", res);
}


PyObject* kth_py_native_chain_stealth_compact_list_nth(PyObject* self, PyObject* args){
    PyObject* py_stealth_compact_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_stealth_compact_list, &py_n)) {
        return NULL;
    }
    kth_stealth_compact_list_t list = (kth_stealth_compact_list_t)get_ptr(py_stealth_compact_list);
    kth_stealth_compact_t res = kth_chain_stealth_compact_list_nth(list, py_n);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
