%Equivalent Source Method
close all
clear all

%Select plane number,engine condition, and octave band
plane = 2;
eng_cond = 4;
f = 315;

%Load the microphone array
temp = load('F22Holloman2009Geometry7.mat');
micPositions = temp.F22Geometry{1,plane};

%Load the measurements
[measurements,fc] = loadData(eng_cond,plane,f,'data\');

%set reference mics pressure
Pref = 20 * 10^(-6);

%set Speed of Sound in m/s
c = 343;

%number of monopole sources
n = 400;

%error function type. 0 = Jessica Morgans, 1 = Least Squares 
err = 0;

%set the low and high frequency bounds in the third octave band in Hz
flow = fc/(2^(1/6));
fhigh = fc*2^(1/6);
%These values are for a 315 center frequency 

%Set the number of frequencies in the third octave band
nf = 10;

%Calculate the third octave band based on a logarithmic spacing.
freqs = logspace(log10(flow), log10(fhigh), nf);

%calculate wavenumber
k = 2 * pi * freqs/c;

%set initial guesses for sources
zpU = 2.2;
zpC = 2.2;
Amax = .6; %The ratio of AmaxC/AmaxU
sdU = 1.7;
sdC = 1.7;
angle = 130 * pi/180;

%the distance between monopole sources in meters 
dist = .02;

%initialize monopole sources
[sourcesU,sourcesC] = initSources(0,2.1,zpU,sdU,1,zpC,sdC,Amax,n,...
                                            dist,angle,freqs,c);

%Plot the Rayleigh Distrbutions
plotDistribution(sourcesU,sourcesC);

%simulate measurement
solution = simulation(sourcesU,sourcesC,micPositions,k);

%Calculate Sound Pressure Levels
SPLc = takeSPL(solution,Pref);

%Match the two SPL's to each other according to the 100th percentile
SPL = matchSPL(SPLc, measurements, 1);
          

[errorMap, errorTotal] = errorFunction(SPL,measurements,Pref,15,err);

errorTotal

plotSPL(SPL,micPositions,'Caculated SPL')

plotSPL(measurements,micPositions,'Measured SPL')

figure('Color',[1,1,1])
pcolor(micPositions(:,:,3),micPositions(:,:,2),errorMap);
shading interp
axis image
caxis([0,10])
colorbar
title('Error Map')

clear c freq n dist angle k zpU sdU AmaxU zpC sdC AmaxC Pref temp plane top...
           peak1 peak2 temp2 SPLm adjustment min1 peak1 highValue SPLmax ...
           flow fhigh nf freqs temp2;