function [ probability ] = probability_prime(M, N)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
counter = 0;
for i= 1:N
    a = ceil(rand * M);
    b = ceil(rand * M);
    if (gcd(a,b) == 1)
        counter = counter + 1;
    end
end
counter
probability = counter / N

