function plotDistribution(sourcesU,sourcesC)
%plotDistribution Use to plot Rayleigh Distibutions

X1 = sourcesU(:,3);
X2 = sourcesC(:,3);
Y1 = sourcesU(:,4);
Y2 = abs(sourcesC(:,4));

% Create figure
figure1 = figure('Color',[1 1 1]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.193894110275688 0.17374213084708 0.618135964912282 0.595920790501235],...
    'FontWeight','bold',...
    'FontSize',18,...
    'FontName','Times New Roman');
% Uncomment the following line to preserve the X-limits of the axes
% xlim(axes1,[0 8]);
% Uncomment the following line to preserve the Y-limits of the axes
% ylim(axes1,[0 1]);
box(axes1,'on');
hold(axes1,'all');

% Create multiple lines using matrix input to plot
plot1 = plot(X1,Y1,X2,Y2,'Parent',axes1,'LineWidth',3);
set(plot1(1),'DisplayName','Uncorrelated');
set(plot1(2),'LineStyle','-.','Color',[1 0 0],'DisplayName','Correlated');

% Create title
title('Sources','FontSize',36,'FontName','Times New Roman');

% Create xlabel
xlabel({'z (meters)'},'FontSize',24,'FontName','Times New Roman');

% Create ylabel
ylabel({'Amplitude'},'FontSize',24,'FontName','Times New Roman');

% Create legend
legend1 = legend(axes1,'show');
set(legend1,'LineWidth',2);

