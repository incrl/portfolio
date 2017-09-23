function [ sourcesU, sourcesC ] = initSources_opt(x,y,zpU,sdU,AmaxU,zpC,...
    sdC,AmaxC,dist,zMin,zMax,angle,freqs,c)
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

%Build a line of sources
sources = zMin:dist:zMax;

% This version has a set of source locations called "sources"
[~,n] = size(sources);
[~,numf] = size(freqs);
sourcesU = zeros(n,5);
sourcesC = zeros(n,5,numf);

%initializes the two arrays to a rayleigh distribution
raylU = raylpdf(sources,sdU);
raylC = raylpdf(sources,sdC);

%Calculates how much shift is neccesary based on the peak position
[~,indexU] = max(raylU);
[~,indexC] = max(raylC);
shiftU = zpU - indexU * dist - zMin;
shiftC = zpC - indexC * dist - zMin;

tempU = sources - shiftU;
tempC = sources - shiftC;

%a Q function can be put here if neccesary, but we will assume Q=1
q = 1;

ind = 1:length(sources);

%puts the sources into a list of with x,y,z, ampliture and Q values
sourcesU(:,1) = x;
sourcesU(:,2) = y;
sourcesU(:,3) = sources;
sourcesU(:,4) = AmaxU * raylpdf(tempU,sdU);
sourcesU(:,5) = q;
%Since sourcesC is dependant on frequency, we must calculate each
%value for each frequencies
sourcesC(:,1,:) = x;
sourcesC(:,2,:) = y;
for f = 1:numf;
    sourcesC(:,3,f) = sources;
    %Calculate the complex amplitude with a correlated phase
    sourcesC(:,4,f) = AmaxC .* raylpdf(tempC,sdC).*exp(-1i*(2*pi*freqs(f)*dist*sin(angle))/c .* ind); 
end
sourcesC(:,5,:) = q;
end

