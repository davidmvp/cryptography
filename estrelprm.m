function [ empirprob ] = estrelprm( M,numsim )


% [ empirprob ] = estrelprm( M,numsim )
% estimates the probability that two discrete-uniformly-selected 
% integers between 1 and M (inclusive) are relatively prime.
% Based on numsim number of simulations
% ready mar 20, 2013

empirprob=0;
for i=1:numsim
    a=ceil(M*rand);
    b=ceil(M*rand);
    if gcd(a,b)==1
        empirprob=empirprob+1/numsim;
    end
end


end

