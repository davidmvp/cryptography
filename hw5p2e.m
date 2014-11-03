function [ p ] = hw5p2e( input_args )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

 a=primes(10000); 
 p=1; 
 for i=1:1229
     p=p*(1-(1/a(i))^2);
     
 end
p

