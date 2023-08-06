#include <kth/py-native/chain/output_list.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_output_list_push_back(PyObject* self, PyObject* args){
    PyObject* py_output_list;
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "OO", &py_output_list, &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    kth_output_list_t output_list = (kth_output_list_t)get_ptr(py_output_list);
    kth_chain_output_list_push_back(output_list, output);
    //return Py_BuildValue("O", res);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_output_list_count(PyObject* self, PyObject* args){
    PyObject* py_output_list;

    if ( ! PyArg_ParseTuple(args, "O", &py_output_list)) {
        return NULL;
    }

    kth_output_list_t output_list = (kth_output_list_t)get_ptr(py_output_list);
    uint64_t res = kth_chain_output_list_count(output_list);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_output_list_nth(PyObject* self, PyObject* args){
    PyObject* py_output_list;
    uint64_t py_n;

    if ( ! PyArg_ParseTuple(args, "OK", &py_output_list, &py_n)) {
        return NULL;
    }
    kth_output_list_t output_list = (kth_output_list_t)get_ptr(py_output_list);
    kth_output_t res = kth_chain_output_list_nth(output_list, py_n);
    return to_py_obj(res);
}

#ifdef __cplusplus
} //extern "C"
#endif
