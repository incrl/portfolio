function [ sourcesU, sourcesC ] = initSources(x,y,zpU,sdU,AmaxU,zpC,...
                                        sdC,AmaxC,n,dist,angle,freqs,c)
%initSources Initialization of the sources using a raleigh distribution

% This function initializes a line of uncorrelated
% sources according to the a raleigh
% distribution with a start position at (x,y) with a peak position zpU
% a standard deviation of sdU, and a peak amplitued of AmaxU
% This distribution creates n sources seperated by a distance 'dist'.

% This function also determines coherent amplitudes at angle 'angle' at the
% frequencie 'freqs' where the speed of sound is c
% zpC is correlated peak position, AmaxC is correlated peak amplitude
% and sdC is correlated standard deviation

[~,numf] = size(freqs);
sourcesU = zeros(n,5);
sourcesC = zeros(n,5,numf);

%initializes the two arrays to a rayleigh distribution
tempU = [0:dist:n*dist];
tempC = [0:dist:n*dist];
raylU = raylpdf(tempU,sdU);
raylC = raylpdf(tempC,sdC);

%Calculates how much shift is neccesary based on the peak position
[~,indexU] = max(raylU);
[~,indexC] = max(raylC);
shiftU = zpU - indexU * dist;
shiftC = zpC - indexC * dist;

%a Q function can be put here if neccesary, but we will assume Q=1
q = 1;

%puts the sources into a list of with x,y,z, ampliture and Q values
for s=1:n
    sourcesU(s,1) = x;
    sourcesU(s,2) = y;
    sourcesU(s,3) = shiftU + s*dist;
    sourcesU(s,4) = AmaxU * raylU(s);
    sourcesU(s,5) = q;
    %Since sourcesC is dependant on frequency, we must calculate each
    %value for each frequency
    for f = 1:numf
        sourcesC(s,1,f) = x;
        sourcesC(s,2,f) = y;
        sourcesC(s,3,f) = shiftC + s*dist;
        %Calculate the complex amplitude with a correlated phase
        sourcesC(s,4,f) = AmaxC * raylC(s)*exp(-1i*(2*pi*freqs(f)*dist*sin(angle))/c * s);
        sourcesC(s,5,f) = q;
    end
end
end

