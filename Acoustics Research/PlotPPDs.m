
freq = 315;
eng = 4;
plane = 3;

load(['BOA Results\BOA_Results_plane_',num2str(plane),'_engcond_',num2str(eng),...
    '_freq_',num2str(freq),'.mat']);

scaling = 1;

numbins = 15;
%{
[resolution,small_marker,large_marker,...
    minor_line,green,minor_fontsize,major_line,colors,...
    lines,markers] = FigureDefaults(scaling,'full','custom',9);
%}
% 
% set(0,'DefaultFigureUnits','inches');
% set(0,'DefaultAxesUnits','inches');

%Make half screen
screen_size = get(0, 'ScreenSize');

half_screen = floor(screen_size(3)./2);

figure1 = figure;
set(figure1, 'Position', [0 0 half_screen screen_size(4) ]);

%ZPu PPD
subplot(3,2,1), hist(values(:,1),numbins)
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
title(['ZPu = ',num2str(start(1))])
xlabel('location (m)')

%ZPc PPD
subplot(3,2,2), hist(values(:,2),numbins)
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
title(['ZPc = ',num2str(start(2))])
xlabel('location (m)')

%SDu PPD
subplot(3,2,3), hist(values(:,4),numbins)
title(['SDu = ',num2str(start(4))])
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
xlabel('width (m)')

%SDc PPD
subplot(3,2,4), hist(values(:,5),numbins)
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
title(['SDc = ',num2str(start(5))])
xlabel('width (m)')

%Amax PPD
subplot(3,2,5), hist(values(:,3),numbins)
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
title(['Amax = ',num2str(start(3))])
xlabel('Ac/Au')

%Angle PPD
subplot(3,2,6), hist(values(:,6) * 180/pi,numbins)
h = findobj(gca,'Type','patch');
set(h,'FaceColor','g','EdgeColor','k');
title(['Angle = ',num2str(start(6)*180/pi)])
xlabel('degrees')

clear h numbars;