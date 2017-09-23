%The Bayesian Optimization Algorithm
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
[measurements,fc,angle] = loadData(eng_cond,plane,f,'data\');

%Set nozzle position
x = 0;
y = 2.1;

%set reference mics pressure
Pref = 20 * 10^(-6);

%set Speed of Sound in m/s
c = 343;

%number of monopole sources
n = 400;

%set the low and high frequency bounds in the third octave band in Hz
flow = fc/(2^(1/6));
fhigh = fc*2^(1/6);
%These values are for a 315 center frequency 

%Set the number of frequencies in the third octave band
nf =10;

%Calculate the third octave band based on a logarithmic spacing.
freqs = logspace(log10(flow), log10(fhigh), nf);

%Ranges
zpUmin = 0;
zpUmax = 8;
zpCmin = 0;
zpCmax = 8;
AmaxMin = 0;
AmaxMax = 1;
sdUmin = .1;
sdUmax = 8;
sdCmin = .1;
sdCmax = 8;
distMin = .005;
distMax = .1;

tic;
%Put all boundary conditions into one container called boundaries for
%passing into the Simulated Annealing
boundaries = [zpUmin,zpUmax,zpCmin,zpCmax,AmaxMin,AmaxMax,...
                        sdUmin,sdUmax,sdCmin,sdCmax,distMin,distMax];
                    
%Put all of the physical description into a container called geometry
geometry = [x,y,angle,c,Pref,n];

%Grab the starting position for the FGS from the Simulated Annealing
start = simAnnealing(boundaries,geometry,freqs,micPositions,measurements);

%Temporary for testing
%start = [7,2.2,.6,1.7,1.7,.02,.006];

%Grab information for the PPDs from the Fast Gibbs Sampler
values = FGS(boundaries,geometry,start,freqs,micPositions,measurements);
toc
                   
