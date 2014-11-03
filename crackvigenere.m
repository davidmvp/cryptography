function [key]=crackvigenere(ciphertext)

n=length(ciphertext);
stop=0;
iter=0;
while stop<.055*n
    iter=iter+1;
    stop=coinc(ciphertext,iter);
end
key=zeros(1,iter);
for j=1:iter
    caesar=choose(ciphertext,iter,j);
    [fr rel]=zfrequency(caesar);
    cr=corr(rel);
    [val,pos]=max(cr);
    key(j)=pos-1;
end
