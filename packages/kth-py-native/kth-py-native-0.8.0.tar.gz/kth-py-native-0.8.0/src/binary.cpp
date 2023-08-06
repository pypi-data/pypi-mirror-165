// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/binary.h>
#include <kth/capi.h>
#include <kth/py-native/utils.h> //TODO(fernando): poner bien el dir del header

#ifdef __cplusplus
extern "C" {
#endif

// -------------------------------------------------------------------
// binary
// -------------------------------------------------------------------

PyObject* kth_py_native_binary_construct(PyObject* self, PyObject* args){
    kth_binary_t binary = binary_construct();
    return to_py_obj(binary);
}

PyObject* kth_py_native_binary_construct_string(PyObject* self, PyObject* args){

    char const* filter;

    if ( ! PyArg_ParseTuple(args, "s", &filter)) {
        return NULL;
    }

    kth_binary_t binary = binary_construct_string(filter);
    return to_py_obj(binary);
}

PyObject* kth_py_native_binary_construct_blocks(PyObject* self, PyObject* args){

    uint64_t bits_size;
    uint64_t lenght;
    PyObject* blocks;

    if ( ! PyArg_ParseTuple(args, "KKO", &bits_size, &lenght, &blocks)) {
        return NULL;
    }

    if (PySequence_Check(blocks)) { //Check if its an array
        size_t size = PySequence_Size(blocks); //get array size
        uint8_t* result = malloc(sizeof(uint8_t) * size); // reserve memory

        for (int i = 0; i < size; ++i) {
            PyObject* item = PySequence_GetItem(blocks, i); //read every item in the array

            //TODO(fernando): this is strange... check it!!
            if (PyLong_Check(item)) { //check if the item its an integer
               result[i] = PyLong_AsLong(item); //extract the value of the pyobject as int
            } else {
               return NULL;
            }
        }

        kth_binary_t binary = binary_construct_blocks(bits_size, result, size);
        return to_py_obj(binary);
    }

    return NULL;
}

PyObject* kth_py_native_binary_blocks(PyObject* self, PyObject* args){

    PyObject* binary;
    if ( ! PyArg_ParseTuple(args, "O", &binary)) {
        return NULL;
    }

    kth_binary_t binary_pointer = (kth_binary_t)get_ptr(binary);
    kth_size_t out_n;
    uint8_t* blocks = (uint8_t*)binary_blocks(binary_pointer, &out_n);

    return Py_BuildValue("y#", blocks, out_n);
}

PyObject* kth_py_native_binary_encoded(PyObject* self, PyObject* args){

    PyObject* binary;
    if ( ! PyArg_ParseTuple(args, "O", &binary)) {
         return NULL;
    }

    kth_binary_t binary_pointer = (kth_binary_t)get_ptr(binary);
    char* str = (char*)binary_encoded(binary_pointer);
    return PyUnicode_FromString(str);
}

#ifdef __cplusplus
} //extern "C"
#endif

