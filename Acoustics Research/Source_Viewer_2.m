%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%DESCRIPTION: F-22 MEASUREMENT - FIGURES
%AUTHOR: ALAN WALL/BYU (alantwall@gmail.com)
%            Modified for David Hart/BYU (davidhart100@gmail.com)
%INPUT:
%OUTPUT:
%SUBROUTINES:
%PROJECT: F-22 Measurement Publication
%DATE: 02-04-11
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc; clear all; close all;

%FIGURE SCALING FOR SCREEN SIZE
scaling = 1.5;

%Number of planes on graph
num_parts = 10;

%set nozzle location
x=0;
y=2.1;

%set reference mics pressure
Pref = 20 * 10^(-6);

%set Speed of Sound in m/s
c = 343;

%number of monopole sources
n = 400; 

%set the low and high frequency bounds in the third octave band in Hz
fc = 315;
flow = fc/(2^(1/6));
fhigh = fc*2^(1/6);
%These values are for a 315 center frequency 

angle = 130 * pi/180;

%Set the number of frequencies in the third octave band
nf = 10;

%Calculate the third octave band based on a logarithmic spacing.
freqs = logspace(log10(flow), log10(fhigh), nf);

%calculate wavenumber
k = 2 * pi * freqs/c;

%set initial guesses for sources
zpU = 6.9274;
zpC = 1.7407;
sdU = 5.5103;
sdC = 1.7892;
AmaxU = 1;
AmaxC = .6296;
%the distance between monopole sources in meters 
dist = .0888;

%initialize monopole sources
[sourcesU,sourcesC] = initSources(x,y,zpU,sdU,AmaxU,zpC,sdC,AmaxC,n,...
                                            dist,angle,freqs,c);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%3D OASPL MAPS

[resolution,small_marker,large_marker,...
    minor_line,green,minor_fontsize,major_line,colors,...
    lines,markers] = FigureDefaults(scaling,'JASA','JASA');

figure

%INITIALIZE OASPL MAP
subplot(1,2,1)

%Load Locations
load('viewer_planes.mat');

%LOOP THROUGH PLANES
for cas = 1:num_parts;
    
    micPositions = planes{1,cas};
    
    %simulate measurement
    solution = simulation(sourcesU,sourcesC,micPositions,k);

    %Calculate Sound Pressure Levels
    SPL = takeSPL(solution,Pref);
    
    %PLOT COLOR MAPS
    surf(micPositions(:,:,3),micPositions(:,:,1),micPositions(:,:,2),SPL);
    hold on
    
    %         %PLOT LINES ON GROUND
    %         plot3(data.OASPL.Z{cas}(1,:),data.OASPL.X{cas}(1,:),zeros(1,length(data.OASPL.Z{cas}(1,:))),'--k')
    
end

%     %JET CENTERLINE
%     plot3([-55 120]*0.3048,[0 0]*0.3048,[0 0]*0.3048,'k');

%     %PLOT JET EXHAUST ILLUSTRATION
%     for i = 0:20
%         plot3(i*0.5,0,75/12*0.3048,'o','MarkerSize',(21-i)*0.3*scaling,'Color',[(i+10)/30 i/20 1],'LineWidth',major_line)
%     end

%FORMATTING
shading interp
axis image
AX = caxis;
caxis([AX(2)-20 AX(2)])       %Forcing this prevents alteration when 3D jet is inserted.
xlabel('{\itz} (m)')
ylabel('{\itx} (m)')
zlabel('{\ity} (m)')
set(gca,'XTick',[-25:5:50],'YTick',[-25:5:50],'ZTick',[-25:5:50])
set(gca,'GridLineStyle','--','LineWidth',minor_line)

%ADD COLORBAR WITH WHITE BACKGROUND
subplot 122
h_cb = colorbar('FontSize',minor_fontsize);
caxis([AX(2)-20 AX(2)])
ylabel(h_cb,'OASPL (dB re 20 \muPa)','FontSize',minor_fontsize)
set(gca,'Position',[2.83 0 1 5]*scaling)
set(h_cb,'OuterPosition',[0.83 0.05 (1-0.83) .85])
set(gca,'YTick',[],'XTick',[],'XColor','w','YColor','w')
set(gca,'LineWidth',1*scaling)

%RETURN TO OASPL MAPS
subplot(1,2,1)

%ADD 3D JET
%plot_3ds_model_empty;%(h_fig,'MeasSchematic_20110429.fig');

%ARTIFICIAL 'ZOOM IN' AND VIEW PROPERTIES
a=2;  %Constant for the artificial 'zoom'
set(subplot(1,2,1),'Position',[-a 0.4 3.375*5/6+2*a 3.375]*scaling)
view([-50 35])
axis([-15 28 -5 23 0 5])

%RELOCATE AXES LABELS
ylabh = get(gca,'YLabel');
set(ylabh,'Units','inches')
set(ylabh,'Position',[1.5 0]*scaling)
xlabh = get(gca,'XLabel');
set(xlabh,'Units','inches')
set(xlabh,'Position',[3.3 .1]*scaling)



