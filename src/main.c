// WSL2: gcc src/main.c -I ../berkeley-softfloat-3/source/include -L ../berkeley-softfloat-3/build/Linux-x86_64-GCC -l softfloat -o soft-serve

#include "softfloat.h"
#include <stdlib.h>
#include <memory.h>
#include <stdio.h>
#include "pbz_types.h"

enum txt_to_f32_result
{
    txt_to_f32_result_OK,
    txt_to_f32_result_PARSE_ERROR,
};

// TODO(pbz): Needs to return error if there was a parse error
// TODO(pbz): Needs to take in a buffer size

enum txt_to_f32_result txt_to_f32(
    txt buffer,
    usize buffer_length,
    f32 * out_result
) {
    // TODO(pbz): Implement string parsing here

    // ! Invalid string causes undefined behavior per C spec but GCC does 0.0
    *out_result = atof(buffer);

    return txt_to_f32_result_OK;
}

zed f32_to_txt(f32 number, txt buffer, usize buffer_length)
{
    // TODO(pbz): Convert the float to string here
}

i32 main(i32 argc, char ** argv)
{
    // float32_t a;
    // float a_value = 0.1;
    // memcpy(&a, &a_value, sizeof(float32_t));

    // float32_t b;
    // float b_value = 0.2;
    // memcpy(&b, &b_value, sizeof(float32_t));

    // float32_t c = f32_add(a, b);

    // float result;
    // memcpy(&result, &c, sizeof(float));
    // printf("a: %01.10f\n", result);

    printf("Enter a floating point number: ");

    byte input_buffer[256];
    txt input = input_buffer;
    fgets(input, sizeof(input), stdin);

    f32 f32_result;
    enum txt_to_f32_result result = txt_to_f32(input, 256, &f32_result);

    if (result == txt_to_f32_result_OK)
    {
        printf("You entered: %f\n", f32_result);
    }
    else
    {
        printf("Parse error: %s\n", input);
    }

    return 0;
}
