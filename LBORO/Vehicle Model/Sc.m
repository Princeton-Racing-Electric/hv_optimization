classdef Sc
    %UNTITLED Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        distribution_in;
        res;
        t = [0];
        v_cc = [0.0];
        my_distribution;
        pascalOrd;
        model;
        soc;
        farads;
        nSeries;
        pascalTri;
        simOut;
        hSurface=1;
    end
    
    properties (Constant)
        vPeak = 8.0;
    end
    
    methods
        function obj = Sc(order, nSeries, vStart, farads, res, model)
            %Sc Construct an instance of this class
            %   Detailed explanation goes here
            
            if nargin < 6
                if nSeries == 1
                    model = 'single';
                else
                    model = 'stack';
                end
            end
            
            if ( strcmp(model, 'single') && nSeries > 1 ) || ...
                    ( strcmp(model, 'stack') && nSeries == 1 )
                error('Wrong model selected for number of caps')
            end
            
            if ~( nSeries == 1 || nSeries == 3 )
                error('Unimplimented model required');
            end
            
            if strcmp(model, 'single')
                obj.model       = 'cap_eq_circuit_pascal5_single_shot';
            elseif strcmp(model, 'stack')
                obj.model       = 'cap_eq_circuit_pascal5_single_shot_stack';
            end

            disp(obj.model);
            
            obj.res             = res;
            obj.pascalOrd       = order;
            obj.pascalTri       = Sc.pascal_triangle(order);
            obj.nSeries         = nSeries;
            obj.farads          = farads;
            
            obj.distribution_in = ones(1, order, nSeries) .* vStart;           
            obj.my_distribution = obj.distribution_in;
            obj.soc             = mean(obj.my_distribution) / obj.vPeak;
            
        end
        
        function obj = run(obj, t, ampsIn)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            [ t, v_end, amps_delivered, soc, distribution_out ] = ...
                obj.sc_model_single_shot( t, obj.res, ampsIn, obj.distribution_in );
            
            obj.distribution_in = distribution_out;
            obj.my_distribution = Sc.appendDistribution(...
                                    obj.my_distribution, obj.distribution_in, obj.nSeries);
            obj                 = obj.updateVcc(v_end);
            obj                 = obj.updateT(t+obj.t(end)+obj.res);
                                    % TODO duplicate timestamp
            obj.soc             = [obj.soc , soc];
            
        end
        
        function obj = updateVcc(obj, vcc)
            obj.v_cc = [ obj.v_cc ; vcc ];
        end
        
        function obj = updateT(obj, t)
            obj.t = [ obj.t ; t ];
        end
        
        function [ t, v_end, amps_delivered, soc, distribution_out ] ...
                = sc_model_single_shot(obj, t, resolution, amps_in, distribution_in)
            %sc_model_single_shot Summary of this function goes here
            %   Detailed explanation goes here

            invert_order        = false;

            % Define simulation variables
            sim_time            = double(t);
            distribution_in     = double(distribution_in);
            amps_in             = double(amps_in);
            capacitance         = double(obj.farads); % F
            
            if resolution <= 0.0
                resolution      = 0.1;
                warning('Overriding resolution');
            end
            
            resolution = double(resolution);
            tStep      = resolution;
            
            %fprintf(sprintf('sim_time=%.1f\tres=%.1f\n', sim_time, resolution));
            
            %v_init              = Sc.createInputArray(...
            %                        obj.pascalTri, obj.nSeries, distribution_in);

            v_init = distribution_in(end, :, :);
            
            disp(v_init);
            
            % Run Simulation
            warning('off');
            obj.simOut          = sim(obj.model,...
                'SrcWorkspace', 'current', 'ReturnWorkspaceOutputs', 'on');
            warning('on');

            % Get output variables
            v_end               = obj.simOut.get('v_cc');
            v_dist              = obj.simOut.get('v_cap');
            amps_delivered      = obj.simOut.get('i_cc');
            t                   = obj.simOut.get('t');
            
            fprintf('%.2f %.2f %.2f %.2f %.2f\n',...
                v_dist(1), v_dist(2), v_dist(6), v_dist(12), v_dist(16));
            
            distribution_out    = Sc.createOutputArray(obj.pascalTri, obj.nSeries, v_dist);
            soc                 = mean(distribution_out)./obj.vPeak;
            
            disp(distribution_out(end, :));
        end

        function [x y z] = get3d(obj, idCap)
            if nargin < 2
                idCap = 0;
            end
            
            x=0;y=0;z=0;
            
            if idCap == 1
                x = 1:obj.pascalOrd;
                
                y = obj.t;

                z = obj.my_distribution(:,:,1);
            end
            
        end
        
        function handle = plotSurface(obj)
            disp('...Plotting Surface...');

            [x, y, z] = obj.get3d(1);
            
            if length(y) > 3*60*60
                y = y ./ 3600.0;
                yUnits = 'hrs';
            elseif length(y) > 3*60
                y = y ./ 60.0;
                yUnits = 'mins';
            else
                yUnits = 'secs';
            end

            obj.hSurface = figure(obj.hSurface);
            surf(x, y, z,...
                'edgecolor','none'); hold all;

            grid on;
            
            ylabel(sprintf('Time /%s', yUnits));
            
            xlabel('Pascal rungs 1 to 5');
            zlabel('Voltage');
            %title('5th order pascal eq circuit, starting at 1V across each cap.  Apply load and see the fast states discharge.  Then open circuit and see the redistribution aka self balancing');
            hold off;

            disp('...done');
        end
        
        function obj = plotMovie(obj, filename, res)
            if nargin < 3
                res          = 1;
            end
            
            disp('...Plotting movie...');

            handle = figure();
            axis([0 6 0 8], 'manual');
            grid on;

            counter = 1;

            for i=1:res:size(obj.my_distribution, 1)
                %bar(mySc.my_distribution(i,:,1));

                bar( obj.my_distribution(i, 1:size(obj.my_distribution, 2)));

                axis([0 6 0 8], 'manual');
                grid on;
                M(counter) = getframe(handle);

                counter = counter + 1;
            end

            close(handle);

            v = VideoWriter(sprintf('%s.mp4', filename), 'MPEG-4');
            v.FrameRate = 5;
            open(v);
            writeVideo(v,M);
            close(v);

            disp('...done');
        end
        
    end
    
    methods (Static)
        
        function distribution   = appendDistribution(distributionSrc, distributionNew, nSeries)
            distribution = zeros( size(distributionSrc, 1)+size(distributionNew, 1), size(distributionSrc, 2), nSeries );
            if nSeries == 1
                distribution = [ distributionSrc ; distributionNew ];
            else
                for i=1:nSeries
                    distribution(:,:,i) = [ distributionSrc(:,:,i) ; distributionNew(:,:,i) ];
                end
            end
            
        end
        
        function str            = getDistributionString(distribution)
            str                 = '';
            
            for i=1:length(distribution)
                str             = [str, sprintf('%.2f\t', distribution(i))];
            end
        end
        
        function v_init         = createInputArray(pascalTri, nSeries, distribution, invert)
            
            if nargin < 4
                invert          = false;
            end
            
            x                   = size(distribution);
            
            % Do some checks
            if x(2) ~= size(pascalTri, 2)
                error('Wrong array size for pascal order in input');
            else
                if size(x, 3) == 1
                    % Only a single cap so all ok
                elseif x(3) ~= nSeries
                    error('Not enough caps defined in input array');
                end
            end
            
            v_init              = ones(x(1), 1, nSeries);

            if ~invert
                for i=1:x(1)
                    for j=1:nSeries
                        v_init(i, 1, j) = v_init(i, 1, j)...
                                    .* distribution((x(1)+1) - i, j);
                    end
                end
            else
                for i=1:x(1)
                    for j=1:nSeries
                        v_init(i, 1, j) = v_init(i, 1, j) .* distribution(i, end, j);
                    end
                end
            end
        end
        
        function v_out          = createOutputArray(pascalTri, nSeries, distribution, invert)
            % TODO, but in this code
            % in      = 6.0000    6.0000    6.0000    6.0000    6.0000
            % mdl_out = 6.00 6.00 5.99 5.99 5.98
            % fn_out  = 5.7810    5.3742    5.3742    5.3742    5.3742
            
            
            if nargin < 4
                invert          = false; % TODO
            end
            
            x                   = size(distribution);
            
            % Do some checks
            if x(2) ~= sum(pascalTri) * nSeries
                error('Wrong array size for in output');
            end
            
            ptrVout         = 1;
            
            for i=1:nSeries
                ptrDistribution = 1;
                for j=1:size(pascalTri, 2)
                    counter = 1;

                    ptrEndDistribution = ptrDistribution + pascalTri(1, j) - 1;

                    for k=ptrDistribution:ptrEndDistribution
                        for m=1:size(distribution,1)
                            thisArray(m, counter) = distribution(m, i*j);
                        end
                        counter = counter + 1;
                    end

                    v_out(:, ptrVout) = mean(thisArray, 2);

                    ptrVout = ptrVout + 1;
                    ptrDistribution = ptrEndDistribution + 1;
                end
                temp(:,:,i)  = [v_out(:, (5*i-4):(5*i))];
            end
            
            v_out = temp;
        end
    
        function pt             = pascal_triangle(n) 

            % The first two rows are constant
            pt(1, 1) = 1;
            pt(2, 1 : 2) = [1 1]; 

            % If only two rows are requested, then exit
            if n < 3
                return
            end 

            for r = 3 : n
                % The first element of every row is always 1
                pt(r, 1) = 1;   

                % Every element is the addition of the two elements
                % on top of it. That means the previous row.
                for c = 2 : r-1
                    pt(r, c) = pt(r-1, c-1) + pt(r-1, c);
                end   

                % The last element of every row is always 1
                pt(r, r) = 1;
            end
            
            pt = pt(n,:);
        end
    end
end

