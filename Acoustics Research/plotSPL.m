function plotSPL(SPL,micPositions, name, colorType)
%plotSPL

%If colorType <= 0, then use default colormap, if colorType>0, use Alan's colormap 
if nargin < 4
    colorType = 0;
end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Color Map Generator%%%%%%%%%%%%%%%%%%%%%%%%%%
%Code Written By Alan Wall
a=20; b=30; c=45; d=60; e = 75;
greenshift = -5;
blueshift = 5;

p_hot(1:a,1) = linspace(0,0.4,a);
p_hot(a:b,1) = linspace(0.4,1,b-a+1);
p_hot(b+1:e,1) = 1;

p_hot(1:b+greenshift,2) = 0;
p_hot(b+1+greenshift:c,2) = linspace(0,.4,c-b-greenshift);
p_hot(c:d,2) = linspace(0.4,1,d-c+1);
p_hot(d+1:e,2) = 1;

% W = -0.4/((b+blueshift)/2)^2*((1:b+blueshift)-(b+blueshift)/2).^2+0.4;
% p_hot(1:b+blueshift,3) = W;
p_hot(1:a,3) = linspace(0,0.5,a);
p_hot(a:b+blueshift,3) = linspace(0.5,0,b-a+1+blueshift);
p_hot(b+1+blueshift:d,3) = 0;
p_hot(d+1:e,3) = linspace(0,1,e-d);
%%%%%%%%%%%%%%%%%%%%%%%%%%End  Color Map Generator%%%%%%%%%%%%%%%%%%%%%%%%
                                               

% Create figure
figure('Color',[1 1 1]);

%create plot
top = max(max(SPL));
pcolor( micPositions(:,:,3),micPositions(:,:,2),SPL);

%Check for colormap type
if colorType > 0
    colormap(p_hot)
end
shading interp
axis image
caxis([top - 20,top])

% Create ylabel
ylabel({'y (m)'},'FontWeight','bold','FontSize',18,...
    'FontName','Times New Roman');

% Create title
title(name,'FontWeight','bold','FontSize',24,...
    'FontName','Times New Roman');

% Create xlabel
xlabel({'z (m)'},'FontWeight','bold','FontSize',18,...
    'FontName','Times New Roman');

% Create colorbar
colorbar('FontWeight','bold','FontSize',18,...
    'FontName','Times New Roman');





