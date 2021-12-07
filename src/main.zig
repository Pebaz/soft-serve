const std = @import("std");

// TODO(pbz): How to get the float value from the user?
// TODO(pbz): Specifically, how to specifiy the fraction part?
// TODO(pbz): 1.05 == "1.05" as string or ?
// https://www.youtube.com/watch?v=tx-M_rqhuUA

const Float = struct
{
    value: f32,

    pub fn init(value: f32) Float
    {
        return Float
        {
            .value = value,
        };
    }

    pub fn sign(self: Float) bool
    {
        return self.value >> 31 & 1 > 1;
    }
};

pub fn print_digits(num: u32) void
{
    var digits = [10]u32;
    var n = num;
    var index = 0;
    while (n > 0)
    {
        var digit = n % 10;
        digits[digits.length - index] = digit;
        std.debug.print("{}", .{digit});
        n = n / 10;
        index += 1;
    }
}

pub fn main() !void
{
    std.debug.print("Hello World!\n", .{});
    var f = Float.init(3.14);
    std.debug.print("VALUE: {}\n", .{f});

    print_digits(123);
}
