function [ SPL ] = matchSPL( SPLc, SPLm, percentile )
%matchSPL Makes the max of the SPLc within the percentile of the SPLm

perc = 1-percentile;
peak1 = max(max(SPLm));
min1 = min(min(SPLm));
highValue = peak1 - perc*(peak1 - min1);
SPLmax = max(max(SPLc));

adjustment = highValue - SPLmax;

SPL = SPLc + adjustment;

end

