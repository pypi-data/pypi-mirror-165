// Copyright (c) 2016-2022 Knuth Project developers.
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <kth/py-native/tools.h>

#include <thread>

void print_thread_id() {
    auto this_id = std::this_thread::get_id();
    printf("thread %d\n", this_id);
}


void sleep_for_30() {
    std::this_thread::sleep_for(std::chrono::seconds(30));
}
