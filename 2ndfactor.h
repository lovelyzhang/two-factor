//
// Created by 张裕 on 2019-03-28.
//

#ifndef INC_2NDFACTOR_VERIFY_H
#define INC_2NDFACTOR_VERIFY_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#define ERROR 1
#define SUCCESS 0

static char BASE_URL[] = "http://localhost:8080";

struct MemoryStruct {
    char *memory;
    size_t size;
};

static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    // contents是libcurl获得的内容，不是用户分配的
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *) userp;

    // 已有内容+新内容+\0
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (ptr == NULL) {
        /* out of memory! */
        printf("not enough memory to realloc\n");
        /*release malloced memory*/
        free(mem->memory);
        return 0;
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

int send_code(const char *username) {
    CURL *curl_handle;
    CURLcode res;
    char url[256];
    struct MemoryStruct chunk;
    int ret = SUCCESS;

    sprintf(url, "%s/login?username=%s", BASE_URL, username);
    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_handle = curl_easy_init();
    curl_easy_setopt(curl_handle, CURLOPT_URL, url);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *) &chunk);
    res = curl_easy_perform(curl_handle);

    if (res != CURLE_OK) {
        ret = ERROR;
    }
    if (strcmp(chunk.memory, "0") != 0) {
        ret = ERROR;
    }
    free(chunk.memory);
    curl_easy_cleanup(curl_handle);
    return ret;
}

int verify_code(const char *username, const char *code) {
    CURL *curl_handle;
    CURLcode res;
    char url[256];
    struct MemoryStruct chunk;
    int ret = SUCCESS;

    sprintf(url, "%s/auth?username=%s&code=%s", BASE_URL, username, code);
    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_handle = curl_easy_init();
    curl_easy_setopt(curl_handle, CURLOPT_URL, url);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *) &chunk);
    res = curl_easy_perform(curl_handle);

    if (res != CURLE_OK) {
        ret = ERROR;
    }
    if (strcmp(chunk.memory, "0") != 0) {
        ret = ERROR;
    }
    curl_easy_cleanup(curl_handle);
    free(chunk.memory);
    return ret;
}

#endif //INC_2NDFACTOR_VERIFY_H
