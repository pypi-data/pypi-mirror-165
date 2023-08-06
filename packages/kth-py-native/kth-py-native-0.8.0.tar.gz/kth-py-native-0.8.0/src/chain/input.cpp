#include <kth/py-native/chain/input.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

// kth_input_t kth_chain_input_factory_from_data(uint8_t* data, uint64_t n);
PyObject* kth_py_native_chain_input_factory_from_data(PyObject* self, PyObject* args){
    char* py_data;
    int py_n;

    if ( ! PyArg_ParseTuple(args, "y#", &py_data, &py_n)) {
        return NULL;
    }

    kth_input_t res = kth_chain_input_factory_from_data((uint8_t*)py_data, py_n);
    return to_py_obj(res);
}

// kth_input_t kth_chain_input_construct(kth_outputpoint_t previous_output,
// kth_script_t script,
// uint32_t sequence);
PyObject* kth_py_native_chain_input_construct(PyObject* self, PyObject* args){
    PyObject* py_previous_output;
    PyObject* py_script;
    uint32_t py_sequence;

    if ( ! PyArg_ParseTuple(args, "OOI", &py_previous_output, &py_script, &py_sequence)) {
        return NULL;
    }

    kth_outputpoint_t previous_output = (kth_outputpoint_t)get_ptr(py_previous_output);
    kth_script_t script = (kth_script_t)get_ptr(py_script);

    kth_input_t res = kth_chain_input_construct(previous_output, script, py_sequence);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_input_is_valid(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    int res = kth_chain_input_is_valid(input);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_input_is_final(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    int res = kth_chain_input_is_final(input);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_input_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_input;
    int py_wire;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_input, &py_wire)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    uint64_t res = kth_chain_input_serialized_size(input, py_wire);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_input_sequence(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    uint32_t res = kth_chain_input_sequence(input);
    return Py_BuildValue("I", res);
}

PyObject* kth_py_native_chain_input_signature_operations(PyObject* self, PyObject* args){
    PyObject* py_input;
    int py_bip16_active;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_input, &py_bip16_active)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    uint64_t res = kth_chain_input_signature_operations(input, py_bip16_active);
    return Py_BuildValue("K", res);
}

PyObject* kth_py_native_chain_input_destruct(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    kth_chain_input_destruct(input);
    Py_RETURN_NONE;
}


PyObject* kth_py_native_chain_input_script(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    kth_script_t script = kth_chain_input_script(input);
    return to_py_obj(script);
}

PyObject* kth_py_native_chain_input_previous_output(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    kth_outputpoint_t res = kth_chain_input_previous_output(input);
    return to_py_obj(res);
}

/*
PyObject* kth_py_native_chain_input_hash(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
     kth_hash_t res = kth_chain_input_hash(input);
    return PyByteArray_FromStringAndSize(res.hash, 32);

}
*/

/*
PyObject* kth_py_native_chain_input_index(PyObject* self, PyObject* args){
    PyObject* py_input;

    if ( ! PyArg_ParseTuple(args, "O", &py_input)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    uint32_t res = kth_chain_input_index(input);
    return Py_BuildValue("L", res);

}
*/



// uint8_t const* kth_chain_input_to_data(kth_input_t input, kth_bool_t wire, kth_size_t* out_size) {
//     auto input_data = kth_chain_input_const_cpp(input).to_data(wire);
//     auto* ret = (uint8_t*)malloc((input_data.size()) * sizeof(uint8_t)); // NOLINT
//     std::copy_n(input_data.begin(), input_data.size(), ret);
//     *out_size = input_data.size();
//     return ret;
// }

PyObject* kth_py_native_chain_input_to_data(PyObject* self, PyObject* args) {
    PyObject* py_input;
    int py_wire;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_input, &py_wire)) {
        return NULL;
    }

    kth_input_t input = (kth_input_t)get_ptr(py_input);
    kth_size_t out_n;
    uint8_t* data = (uint8_t*)kth_chain_input_to_data(input, py_wire, &out_n);

    return Py_BuildValue("y#", data, out_n);
}


#ifdef __cplusplus
} //extern "C"
#endif
