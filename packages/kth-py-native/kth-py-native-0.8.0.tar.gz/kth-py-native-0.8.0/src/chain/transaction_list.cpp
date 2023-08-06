#include <kth/py-native/chain/transaction_list.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_transaction_list_construct_default(PyObject* self, PyObject* args){
    kth_transaction_list_t res = (kth_transaction_list_t)kth_chain_transaction_list_construct_default();
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_transaction_list_push_back(PyObject* self, PyObject* args){
    PyObject* py_transaction_list;
    PyObject* py_transaction;

    if ( ! PyArg_ParseTuple(args, "OO", &py_transaction_list, &py_transaction)) {
        return NULL;
    }

    kth_transaction_list_t transaction_list = (kth_transaction_list_t)get_ptr(py_transaction_list);
    kth_transaction_t transaction = (kth_transaction_t)get_ptr(py_transaction);
    kth_chain_transaction_list_push_back(transaction_list, transaction);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_transaction_list_destruct(PyObject* self, PyObject* args){
   PyObject* py_transaction_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction_list)) {
        return NULL;
    }

    kth_transaction_list_t transaction_list = (kth_transaction_list_t)get_ptr(py_transaction_list);
    kth_chain_transaction_list_destruct(transaction_list);
    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_transaction_list_count(PyObject* self, PyObject* args){
    PyObject* py_transaction_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_transaction_list)) {
        return NULL;
    }

    kth_transaction_list_t transaction_list = (kth_transaction_list_t)get_ptr(py_transaction_list);
    uint64_t res = kth_chain_transaction_list_count(transaction_list);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_transaction_list_nth(PyObject* self, PyObject* args){
    PyObject* py_transaction_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_transaction_list, &py_n)) {
        return NULL;
    }
    kth_transaction_list_t transaction_list = (kth_transaction_list_t)get_ptr(py_transaction_list);
    kth_transaction_t res = kth_chain_transaction_list_nth(transaction_list, py_n);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
