function [ errorMap, errorTotal  ] = errorFunction( SPLc, SPLm, Pref, range, type )
%ERRORFUNCTION Calculate the error map and the total error.
%   This function calculates the differences between SPLm and SPLc and
%   returns a map of the this calculation. It also calculates the total
%   error according to the error equation in the Jessica Morgan's paper.
%   Pref is the reference microphone pressure
%   Only the values that are within a value 'range' of the maximum of SPLc
%   are considered in the total error calculation.
%   Use type to determine which error function is used:
%   If type = 0, use Log type; Else, use least squares

% If type is not provided, assume it is log error function
if nargin < 5
    type = 0;
end

errorMap = abs(SPLm - SPLc);

%Set some initial values
[rows, columns] = size(SPLc);
max1 = max(max(SPLm));
lowerbound = max1 - range;
count = 1;
errorList = [0,0];

for y = 1:rows
    for x = 1:columns
        
        %If SPLm(y,x) is greater than max1 - range, then add it to the list
        if SPLm(y,x) > lowerbound
            errorList(count,1) = SPLm(y,x);
            errorList(count,2) = SPLc(y,x);
            count = count + 1;
        end
    end
end

%Convert the errorlist into P^2
errorList = 10 .^ (errorList/10) * Pref^2;

%If type = 0, use Log error function
if type == 0
    numerator = sum(abs(errorList(:,1) - errorList(:,2)));
    denominator = sum(errorList(:,1));

    errorTotal = 10* log(numerator/denominator)/log(10);
else
%Calculate total error using least squares
numerator = abs(errorList(:,1)- errorList(:,2));
denominator = max(errorList(:,1));

errorTotal = sum((numerator/denominator).^2)/(count-1);
end

end

