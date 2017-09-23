
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

%FIGURE SCALING FOR SCREEN SIZE
scaling = 1.5;

num_planes = 9;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%3D OASPL MAPS

addpath('\\Kirchhoff\Acoustics\Students\Alan Wall\HollomanF22_2009\model3d_for_BYU\model3d_for_BYU')

[resolution,small_marker,large_marker,...
    minor_line,green,minor_fontsize,major_line,colors,...
    lines,markers] = FigureDefaults(scaling,'JASA','JASA');

figure

% %INITIALIZE OASPL MAP
subplot(1,2,1)

%Load Locations
load('viewer_planes.mat');

%LOOP THROUGH PLANES
for cas = 1:num_planes;
    
    micPositionsTemp = planes{1,cas};
    
    %simulate measurement
    solution = simulation(sourcesU,sourcesC,micPositionsTemp,k);

    %Calculate Sound Pressure Levels
    SPLtemp = takeSPL(solution,Pref) + shift;
    
    %PLOT COLOR MAPS
    surf(micPositionsTemp(:,:,3),micPositionsTemp(:,:,1),micPositionsTemp(:,:,2),SPLtemp);
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

% %ADD COLORBAR WITH WHITE BACKGROUND
subplot 122
h_cb = colorbar('FontSize',minor_fontsize);
caxis([AX(2)-20 AX(2)])
ylabel(h_cb,'SPL (dB re 20 \muPa)','FontSize',minor_fontsize)
set(gca,'Position',[2.83 0 1 5]*scaling)
set(h_cb,'OuterPosition',[0.83 0.05 (1-0.83) .85])
set(gca,'YTick',[],'XTick',[],'XColor','w','YColor','w')
set(gca,'LineWidth',1*scaling)

% %RETURN TO OASPL MAPS
subplot(1,2,1)

% ADD 3D JET
plot_3ds_model_empty;%(h_fig,'MeasSchematic_20110429.fig');

%ARTIFICIAL 'ZOOM IN' AND VIEW PROPERTIES
a=2;  %Constant for the artificial 'zoom'
set(subplot(1,2,1),'Position',[-a 0.4 3.375*5/6+2*a 3.375]*scaling)
view([-50 35])
axis([-15 28 -5 23 0 5])

% %RELOCATE AXES LABELS
ylabh = get(gca,'YLabel');
set(ylabh,'Units','inches')
set(ylabh,'Position',[1.5 0]*scaling)
xlabh = get(gca,'XLabel');
set(xlabh,'Units','inches')
set(xlabh,'Position',[3.3 .1]*scaling)

set(gcf,'PaperPositionMode','auto')
print('-dtiff',['-r',num2str(resolution/2)],['Figures\freq_',num2str(fc),...
                        '_engcond_',num2str(eng_cond),'_plane_',num2str(plane)])


clear scaling a ylabh xlabh h_cb AX micPositionsTemp SPLtemp solution resolution ...
    small_marker large_marker minor_line green minor_fontsize major_line colors...
    lines markers num_planes


