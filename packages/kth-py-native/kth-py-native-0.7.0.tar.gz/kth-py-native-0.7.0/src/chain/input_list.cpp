#include <kth/py-native/chain/input_list.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_input_list_push_back(PyObject* self, PyObject* args){
    PyObject* py_input_list;
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "OO", &py_input_list, &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    kth_input_list_t input_list = (kth_input_list_t)get_ptr(py_input_list);
    kth_chain_input_list_push_back(input_list, input);
    //return Py_BuildValue("O", res);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_input_list_count(PyObject* self, PyObject* args){
    PyObject* py_input_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_input_list)) {
        return NULL;
    }

    kth_input_list_t input_list = (kth_input_list_t)get_ptr(py_input_list);
    uint64_t res = kth_chain_input_list_count(input_list);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_input_list_nth(PyObject* self, PyObject* args){
    PyObject* py_input_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_input_list, &py_n)) {
        return NULL;
    }
    kth_input_list_t input_list = (kth_input_list_t)get_ptr(py_input_list);
    kth_input_t res = kth_chain_input_list_nth(input_list, py_n);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
