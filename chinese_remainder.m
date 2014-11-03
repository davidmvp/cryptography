function [x] = chinese_remainder(n,b)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
leng = length(n);
product = prod(n);
x = 0;
for i = 1:leng
    p = product/n(i);
    [g,y,z] = gcd(p,n(i));
    x= x + b(i) * p * y;

end
x = mod(x,product)
end

