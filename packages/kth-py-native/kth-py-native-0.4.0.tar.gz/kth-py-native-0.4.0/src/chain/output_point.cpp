#include <kth/py-native/chain/output_point.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

PyObject* kth_py_native_chain_output_point_get_hash(PyObject* self, PyObject* args){
    PyObject* py_output_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_output_point)) {
        return NULL;
    }

    kth_outputpoint_t p = (kth_outputpoint_t)get_ptr(py_output_point);
    kth_hash_t res = kth_chain_output_point_get_hash(p);
    return Py_BuildValue("y#", res.hash, 32);    //TODO: warning, hardcoded hash size!
}

PyObject* kth_py_native_chain_output_point_get_index(PyObject* self, PyObject* args){
    PyObject* py_output_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_output_point)) {
        return NULL;
    }

    kth_outputpoint_t p = (kth_outputpoint_t)get_ptr(py_output_point);
    uint32_t res = kth_chain_output_point_get_index(p);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_output_point_construct(PyObject* self, PyObject* args){
    return to_py_obj(kth_chain_output_point_construct());
}

PyObject* kth_py_native_chain_output_point_construct_from_hash_index(PyObject* self, PyObject* args){
    char* py_hash;
    size_t py_size;
    uint32_t py_index;

    if ( ! PyArg_ParseTuple(args, "y#I", &py_hash, &py_size, &py_index)) {
        return NULL;
    }

    kth_hash_t hash;
    memcpy(hash.hash, py_hash, 32);
    kth_outputpoint_t res = kth_chain_output_point_construct_from_hash_index(hash, py_index);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_output_point_destruct(PyObject* self, PyObject* args){
    PyObject* py_output_point;
    if ( ! PyArg_ParseTuple(args, "O", &py_output_point)) {
        return NULL;
    }
    kth_outputpoint_t output_point = (kth_outputpoint_t)get_ptr(py_output_point);
    kth_chain_output_point_destruct(output_point);
    Py_RETURN_NONE;
}

/*
PyObject* kth_py_native_point_is_valid(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    // kth_point_t p = (kth_point_t)PyCObject_AsVoidPtr(py_point);
    kth_point_t p = (kth_point_t)PyCapsule_GetPointer(py_point, NULL);
    int res = point_is_valid(p);

    if (res == 0) {
        Py_RETURN_FALSE;
    }

    Py_RETURN_TRUE;
}


PyObject* kth_py_native_point_get_checksum(PyObject* self, PyObject* args) {
    PyObject* py_point;

    if ( ! PyArg_ParseTuple(args, "O", &py_point)) {
        return NULL;
    }

    // kth_point_t p = (kth_point_t)PyCObject_AsVoidPtr(py_point);
    kth_point_t p = (kth_point_t)PyCapsule_GetPointer(py_point, NULL);
    uint64_t res = point_get_checksum(p);

    return Py_BuildValue("K", res);
}
*/

#ifdef __cplusplus
} //extern "C"
#endif
