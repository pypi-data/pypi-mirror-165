#include <kth/py-native/chain/block_list.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_block_list_construct_default(PyObject* self, PyObject* args){
    kth_block_list_t res = (kth_block_list_t)kth_chain_block_list_construct_default();
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_block_list_push_back(PyObject* self, PyObject* args){
    PyObject* py_block_list;
    PyObject* py_block;

    if ( ! PyArg_ParseTuple(args, "OO", &py_block_list, &py_block)) {
        return NULL;
    }

    kth_block_list_t block_list = (kth_block_list_t)get_ptr(py_block_list);
    kth_block_t block = (kth_block_t)get_ptr(py_block);
    kth_chain_block_list_push_back(block_list, block);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_block_list_destruct(PyObject* self, PyObject* args){
   PyObject* py_block_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_block_list)) {
        return NULL;
    }

    kth_block_list_t block_list = (kth_block_list_t)get_ptr(py_block_list);
    kth_chain_block_list_destruct(block_list);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_block_list_count(PyObject* self, PyObject* args){
    PyObject* py_block_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_block_list)) {
        return NULL;
    }

    kth_block_list_t block_list = (kth_block_list_t)get_ptr(py_block_list);
    uint64_t res = kth_chain_block_list_count(block_list);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_block_list_nth(PyObject* self, PyObject* args){
    PyObject* py_block_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_block_list, &py_n)) {
        return NULL;
    }
    kth_block_list_t block_list = (kth_block_list_t)get_ptr(py_block_list);
    kth_block_t res = kth_chain_block_list_nth(block_list, py_n);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
