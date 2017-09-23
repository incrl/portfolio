close all;
clear all;

freq = 1250;

eng = 4;

numbins = 15;

colors = {'k','r','b'};

%Make half screen
screen_size = get(0, 'ScreenSize');

half_screen = floor(screen_size(3)./2);

figure1 = figure;
set(figure1, 'Position', [0 0 half_screen screen_size(4) ]);

%Create variable ranges for plotting purposes
zpUmin = 0;
zpUmax = 8;
zpCmin = 0;
zpCmax = 8;
sdUmin = 0;
sdUmax = 8;
sdCmin = 0;
sdCmax = 8;
AmaxMin = 0;
AmaxMax = 1;
angleMin = 115;
angleMax = 140;
zpUrange = zpUmin:(zpUmax-zpUmin)/numbins:zpUmax;
zpCrange = zpCmin:(zpCmax-zpCmin)/numbins:zpCmax;
sdUrange = sdUmin:(sdUmax-sdUmin)/numbins:sdUmax;
sdCrange = sdCmin:(sdCmax-sdCmin)/numbins:sdCmax;
AmaxRange = AmaxMin:(AmaxMax-AmaxMin)/numbins:AmaxMax;
angleRange = angleMin:(angleMax-angleMin)/numbins:angleMax;

for plane = 1:3
   load(['BOA Results\BOA_Results_plane_',num2str(plane),'_engcond_',num2str(eng),'_freq_',num2str(freq),'.mat']);

   subplot(3,2,1), h(plane) = plot(zpUrange,hist(values(:,1),zpUrange),'Color',colors{plane});
   title('ZPu')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('location (m)')
  
   
   %ZPc PPD
   subplot(3,2,2), plot(zpCrange,hist(values(:,2),zpCrange),'Color',colors{plane})
   title('ZPc')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('location (m)')
   
   
   %SDu PPD
   subplot(3,2,3), plot(sdUrange,hist(values(:,4),sdUrange),'Color',colors{plane})
   title('SDu')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('width (m)')
   
   
   %SDc PPD
   subplot(3,2,4), plot(sdCrange,hist(values(:,5),sdCrange),'Color',colors{plane})
   title('SDc')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('width (m)')
   
   
   %Amax PPD
   subplot(3,2,5), plot(AmaxRange,hist(values(:,3),AmaxRange),'Color',colors{plane})
   title('Amax')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('Ac/Au')
   
   
   %Angle PPD
   subplot(3,2,6), plot(angleRange, hist(values(:,6) * 180/pi,angleRange),'Color',colors{plane})
   title('Angle')
   hold on
   h = findobj(gca,'Type','patch');
   set(h,'FaceColor','g','EdgeColor','k');
   xlabel('degrees')
   
   
end

h2 = legend(h,{'Plane 1','Plane 2','Plane 3'});
set(h2,...
    'Position',[0.833509090909088 0.911349956933678 0.144886363636363 0.078380706287683])
annotation('textbox',...
    [0.40625 0.948320413436693 0.231534090909091 0.0413436692506464],...
    'String',{['freq=',num2str(freq),'Hz engcond=',num2str(eng)]},...
    'FitBoxToText','off');
hold off

set(gcf,'PaperPositionMode','auto')
print('-dtiff',['Figures\PPD_Compare_freq_',num2str(freq),...
                        '_engcond_',num2str(eng)])
